#!/usr/bin/env python3

import time

class Timing:
	def __init__(self):
		self.start_time = time.time()
	
	def duration(self, title: str):
		end_time = time.time()
		elapsed_time = end_time - self.start_time
		print(f"Elapsed Time for {title} operation: {elapsed_time:.2f} seconds")
