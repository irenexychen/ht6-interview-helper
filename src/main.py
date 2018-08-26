'''

main module

'''
from setup import *
from img_analysis import FaceTracker
from stats_collector import StatsCollector
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--demo', action='store_true')
	parser.add_argument('--run_emo_threads', action='store_true')
	args = parser.parse_args()

	setup()
	stats = StatsCollector()
	face_tracker = FaceTracker(stats, 
							   is_demo=args.demo, 
							   run_emo_threads=args.run_emo_threads)
	face_tracker.begin_tracking()
	stats.dump_stats()
	# return 0s

if __name__ == "__main__":
    main()