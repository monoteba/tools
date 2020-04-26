"""
# Description
Converts all wildcard gitattributes, like "*.3ds" to be case-insensitive like "*.3[Dd][Ss]"

# Usage: 
python case-insensitive-gitattributes.py <input_file> <output_file>

# Example
*.fbx filter=lfs diff=lfs merge=lfs -text

Gets converted to (note the added comment):
# fbx
*.[Ff][Bb][Xx] filter=lfs diff=lfs merge=lfs -text
"""

import sys
import re

def main():
	if (len(sys.argv) != 3):
		print("Exactly 2 arguments must be passed. Example:")
		print("python case-insensitive-gitattributes.py <input_file> <output_file>")
		exit(1)

	in_path = sys.argv[1]
	out_path = sys.argv[2]

	# read file
	try:
		with open(in_path, "r+") as in_file:
			lines = in_file.readlines()
	except Exception as e:
		print("Could not read input file %s" % str(e))
		exit(2)

	# write file
	try:
		with open(out_path, "w+") as out_file:
			pattern = re.compile("(\*\.)(\w+)(.*)")
			for line in lines:
				match = re.match(pattern, line)
				if match:
					groups = match.groups()
					ext = insensitive(groups[1])
					line = "# %s \n%s%s%s\n" % (groups[1], groups[0], ext, groups[2])

				out_file.writelines(line)
	except Exception as e:
		print("Could not write to output file %s" % str(e))
		exit(3)


"""
Converts a string like "3ds" into "3[Dd][Ss]"
"""
def insensitive(s):
	result = ""
	for c in s:
		if c.isalpha():
			result += "[%s%s]" % (c.upper(), c.lower())
		else:
			result += c

	return result


main()