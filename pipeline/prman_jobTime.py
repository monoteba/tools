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

	# header
	print("\n%15s %10s %15s" % ("", "h:mm:ss", "seconds"))

	# divider
	print("------------------------------------------")

	# total in h:mm:ss format
	secondsTotal = sum(rendertimes)
	m, s = divmod(secondsTotal, 60)
	h, m = divmod(m, 60)
	print("%-15s|%4d:%02d:%02d|%15.3f" % ("job:", h, m, s, secondsTotal))

	# average in h:mm:ss format
	secondsAvg = secondsTotal / len(rendertimes)
	m, s = divmod(secondsAvg, 60)
	h, m = divmod(m, 60)
	print("%-15s|%4d:%02d:%02d|%15.3f" % ("average:", h, m, s, secondsAvg))

	# divider
	print("------------------------------------------")

	# number of images
	print("total images: %d\n" % (len(rendertimes)))
	
