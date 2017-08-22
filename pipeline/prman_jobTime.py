'''
Sums the total elapsed time of all rendered images of a Pixar Renderman batch job. 

It reads the data from the job XML files, so these are required!

Run the command line:
python prman_jobTime.py /path/to/jobFolder
'''

import os, sys
import xml.etree.ElementTree as ET

args = sys.argv[1:]

def readRenderTime(file):
	xml = ET.parse(file)
	root = xml.getroot()
	timers = root.findall(".//*[@name='totaltime']/elapsed")
	for timer in timers:
		return float(timer.text)


if len(args) != 1:
	print('You need to specify path as argument!')
else:
	rendertimes = []
	for root, dirs, files in os.walk(args[0]):
		for file in files:
			if file.endswith(".xml"):
				rendertimes.append(readRenderTime(os.path.join(root, file)))

	secondsTotal = sum(rendertimes)
	m, s = divmod(secondsTotal, 60)
	h, m = divmod(m, 60)
	print("Job time [h:mm:ss]: %d:%02d:%02d" % (h, m, s))
