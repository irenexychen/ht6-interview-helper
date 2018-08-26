'''

main module

'''
from setup import *
from interviewer import InterviewAI
from stats_collector import StatsCollector
import argparse

def main():

	out_file = 'out.json'
	parser = argparse.ArgumentParser()
	parser.add_argument('--demo', action='store_true')
	parser.add_argument('--eye', action='store_true')
	parser.add_argument('--emo', action='store_true')
	parser.add_argument('--gcloud', action='store_true')
	parser.add_argument('--out_dir', default='../logs/')
	args = parser.parse_args()

	setup()
	stats = StatsCollector()
	interviewer = InterviewAI( stats, 
							   is_demo=args.demo, 
							   run_eye_tracker=args.eye,
							   run_emo_threads=args.emo,
							   run_gcloud_threads=args.gcloud
							 )

	interviewer.begin()
	stats.print_stats()
	stats.to_json(args.out_dir + out_file)
	# return 0s

if __name__ == "__main__":
    main()