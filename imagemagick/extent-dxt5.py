'''
Resize and extend PNG image to nearest 32 pixels
'''

import glob
import math
import os
from wand.image import Image  # ImageMagick
from wand.color import Color

max_size = 1024
step_size = 32

for file in glob.glob('*.png'):
	img = Image(filename=file)
	changed = False

	# resize
	if img.width > max_size or img.height > max_size:
		if img.width > img.height:
			ratio = img.width / img.height
			img.resize(max_size, round(max_size / ratio))
		else:
			ratio = img.height / img.width
			img.resize(round(max_size / ratio), max_size)

		changed = True

	# extend
	width = math.ceil(img.width / step_size) * step_size
	height = math.ceil(img.height / step_size) * step_size
	
	if img.width != width or img.height != height:
		bw = (width - img.width) // 2
		bh = (height - img.height) // 2
		img.border(color=Color('transparent'), width=bw, height=bh)
		changed = True

	# save?
	if changed:
		print('Saving: %s (%d, %d)... ' % (file, img.width, img.height)),
		img.save(filename=file)
		print('Done!')
	else:
		print('Skipping %s' % file)