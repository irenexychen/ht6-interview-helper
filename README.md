## Inspiration

Elevator pitches, interviews, selling yourself... whether they be for jobs, internships, or university applications - are an inevitable and stressful part of life. While we could always go through practice questions, it's difficult to evaluate key communication skills such as eye contact, smiling, and talking at a reasonable pace. We decided to make an app that would make the interview prep experience more convenient and help a large sector of the population gain confidence and competence heading into interviews.

The name "ElevAIte" incorporates the concepts of _elevator_ pitches, elevating/improving oneself, and AI/technology. 

## What it does / How we built it
The user records themselves talking to the webcam and the app displays the user's amount of eye contact and certain facial emotions in real time, as well as other stats such as average words-per-minute and the number of "strong action verbs" used.
We used OpenCV for facial recognition as well as tracking the movement of the eyes and pupils, deduced from the distances and dimensions between these features whether the person is looking directly at the webcam, and calculated a percentage for how often the person made eye contact. We also used the Indico API to detect facial emotions (anger, fear, neutral, surprise, happy, sad) and Google Cloud speech-to-text API. We compared the text against a list of 200+ recommended "action verbs" and identified which were used and how often. Multithreading was implemented for each of these processes for optimizing realtime detection and simultaneously present the data for the user. 
We used Flask and HTML/Javascript to make the front-end website and Firebase for the login/authentication page. 

## Challenges we ran into
The biggest challenge was integrating the Python/OpenCV back-end with a web app front-end using Flask, as well as dealing with deadlocks in our multithreaded application. Also, it was difficult improve on tracking eye movements in OpenCV since the pupil is small and the API - not being 100% accurate - would often identify nostrils or background objects as eyes.

## Accomplishments that we're proud of
- Not overdosing on caffeine
- Not spilling drinks or getting Cheeto dust on electronics
- Pretty UI for once

## What we learned
- Integration is hard (as expected)
- Always git pull before you git push in order to git out of merge errors
- It is possible to function on 4 hours of sleep for the entire weekend

## What's next for ElevAIte
This app has great potential for expansion: we could market it to both interviewees and recruiters who conduct webcam interviews because it would be useful to obtain quantitative data about the emotion/tone and personality of the candidates. 
We were planning to incorporate more text analysis APIs that determined the mood, personality, and overall positivity of a piece of text. We could also add features such as timed practice interview questions for a more realistic environment, or allow users to track their progress in various metrics over time. 

