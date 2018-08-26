#!/usr/bin/env python

from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue



from setup import *
import os
import transcribe_streaming_mic
import collections
import google.api_core.exceptions as exceptions

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] \
    = '../ted_gcloud_service_credentials.json'

class ResumableMicrophoneStream(transcribe_streaming_mic.MicrophoneStream):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk_size, max_replay_secs=5):
        super(ResumableMicrophoneStream, self).__init__(rate, chunk_size)
        self._max_replay_secs = max_replay_secs

        # Some useful numbers
        # 2 bytes in 16 bit samples
        self._bytes_per_sample = 2 * self._num_channels
        self._bytes_per_second = self._rate * self._bytes_per_sample

        self._bytes_per_chunk = (self._chunk_size * self._bytes_per_sample)
        self._chunks_per_second = (
                self._bytes_per_second // self._bytes_per_chunk)
        self._untranscribed = collections.deque(
                maxlen=self._max_replay_secs * self._chunks_per_second)

    def on_transcribe(self, end_time):
        while self._untranscribed and end_time > self._untranscribed[0][1]:
            self._untranscribed.popleft()

    def generator(self, resume=False):
        total_bytes_sent = 0
        if resume:
            # Make a copy, in case on_transcribe is called while yielding them
            catchup = list(self._untranscribed)
            # Yield all the untranscribed chunks first
            for chunk, _ in catchup:
                yield chunk

        for byte_data in super(ResumableMicrophoneStream, self).generator():
            # Populate the replay buffer of untranscribed audio bytes
            total_bytes_sent += len(byte_data)
            chunk_end_time = total_bytes_sent / self._bytes_per_second
            self._untranscribed.append((byte_data, chunk_end_time))

            yield byte_data


def duration_to_secs(duration):
    return duration.seconds + (duration.nanos / float(1e9))

def _record_keeper(responses, stream):
    """Calls the stream's on_transcribe callback for each final response.
    Args:
        responses - a generator of responses. The responses must already be
            filtered for ones with results and alternatives.
        stream - a ResumableMicrophoneStream.
    """
    for r in responses:
        result = r.results[0]
        if result.is_final:
            top_alternative = result.alternatives[0]
            # Keep track of what transcripts we've received, so we can resume
            # intelligently when we hit the deadline
            stream.on_transcribe(duration_to_secs(
                    top_alternative.words[-1].end_time))
        yield r


class GCloudThread(threading.Thread):
    def __init__(self, thread_ID, stats):
      threading.Thread.__init__(self)
      self.thread_ID = thread_ID
      self.stats = stats
      self.exitflag = False
      self.num_cycles = 0
      self.first = True
      print "Starting thread ID : " + str(self.thread_ID)

    def run(self):
        self.transcribe_mic_stream()
        print('Thread {0} exiting...'.format(self.thread_ID))
    
    def transcribe_mic_stream(self):
        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code,
            max_alternatives=1,
            enable_word_time_offsets=True)
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        mic_manager = ResumableMicrophoneStream(
                RATE, int(RATE / 10))

        with mic_manager as stream:
            resume = False
            while True:
                audio_generator = stream.generator(resume=resume)
                requests = (types.StreamingRecognizeRequest(audio_content=content)
                            for content in audio_generator)

                responses = client.streaming_recognize(streaming_config, requests)

                try:
                    # Now, put the transcription responses to use.
                    if self.exitflag:
                        return
                    self.start_print_loop(responses, stream)
                    if self.exitflag:
                        return
                    break
                except (exceptions.OutOfRange, exceptions.InvalidArgument) as e:
                    if not ('maximum allowed stream duration' in e.message or
                            'deadline too short' in e.message):
                        raise
                    print('Resuming..')
                    self.num_cycles += 1
                    if self.exitflag:
                        return
                    resume = True
                    self.first = True


    def start_print_loop(self, responses, stream):
        """Iterates through server responses and prints them.
        Same as in transcribe_streaming_mic, but keeps track of when a sent
        audio_chunk has been transcribed.
        """
        time_zero = time.time()
        with_results = (r for r in responses if (
                r.results and r.results[0].alternatives))
        self.listen_print_loop(
                _record_keeper(with_results, stream), time_zero)


    def listen_print_loop(self, responses, time_zero):
     
        num_chars_printed = 0
        prev_sentence = []
        for response in responses:
            if self.exitflag:
                return

            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            interim_time = time.time()

            # print(transcript)
            full_dict = transcript.split()
            print (prev_sentence, full_dict)
            print (len(prev_sentence), len(full_dict))
            print (not self.first and len(prev_sentence) > len(full_dict))
            print ('')

            if not self.first and len(prev_sentence) > len(full_dict):
                self.first = False
                for word in prev_sentence:
                    if word in self.stats.pword_count:
                        self.stats.pword_count[word] += 1
            if self.first:
                self.first = False
            prev_sentence = full_dict

            prev_sentence = full_dict
            wpm = int(len(full_dict) / (interim_time - time_zero) * 60)

            real_elapsed_time = interim_time - time_zero \
                                + self.num_cycles * GCLOUD_TIMEOUT
            self.stats.wpm_list.append((wpm, real_elapsed_time))

    def set_exit_flag(self):
        self.exitflag = True