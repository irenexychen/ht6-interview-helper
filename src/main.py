'''

main module

'''
from setup import *
from img_analysis import FaceTracker
from stats_collector import StatsCollector

def main():
	setup()
	stats = StatsCollector()
	face_tracker = FaceTracker(stats, is_demo=True)
	face_tracker.begin_tracking()
	# return 0s

if __name__ == "__main__":
    main()