import os, sys, getopt, textwrap
import xml.etree.ElementTree as ET

def main(argv):
	in_file = ""
	out_file = ""
	character_count = 32
	
	try:
		opts, args = getopt.getopt(argv, "i:o:c:")  # ":" indicates option requires argument
	except:
		print("\nUsage: itt_convert.py -i <input.itt> -o <output.srt> -c <character count>")
		print("Supported output formats: .srt .stl")
		print("Example: python itt_convert.py -i my_subs.itt -o new_subs.srt -c 32")
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-i"):
			in_file = os.path.abspath(arg)
		elif opt in ("-o"):
			out_file = os.path.abspath(arg)
		elif opt in ("-c"):
			character_count = int(arg)
	
	if not os.path.exists(in_file) or not in_file.endswith(".itt"):
		print("\nError: Input file does not exist or is not of type .itt")
		sys.exit(1)
		
	if not os.path.splitext(out_file)[1] in [".srt", ".stl"]:
		print("\nError: Output file does not end with .srt or .stl")
		sys.exit(1)
		
	tree = ET.parse(in_file)
	root = tree.getroot()
	
	# find frame rate
	frame_rate = None
	for name, value in root.attrib.items():
		if name.endswith("frameRate"):
			frame_rate = float(value)
			
	if frame_rate is None:
		sys.exit("Could not determine frame rate from file.")
		
	# namespaces
	ns = {"default": root.tag.split('}', 1)[0][1:]}
	body = root.find("default:body", ns)
	
	if (out_file.endswith(".srt")):
		output_srt(out_file, body, ns, frame_rate, character_count)
	elif (out_file.endswith(".stl")):
		output_stl(out_file, body, ns, frame_rate, character_count)
	

def output_srt(out_file, body, ns, frame_rate, character_count):
	subs = []	
	for id, p in enumerate(body.findall("./default:div/default:p", ns)):
		dict = {}
		dict["id"] = id + 1
		
		begin = p.get("begin").split(":")
		begin = "{0}:{1}:{2},{3}".format(begin[0], 
		                                 begin[1], 
		                                 begin[2], 
		                                 "{0:.3f}".format(float(begin[3]) / frame_rate).split(".")[1])
		
		end = p.get("end").split(":")
		end = "{0}:{1}:{2},{3}".format(end[0], 
		                               end[1], 
		                               end[2], 
		                               "{0:.3f}".format(float(end[3]) / frame_rate).split(".")[1])
		
		dict["timecode"] = "{0} --> {1}".format(begin, end)
		
		lines = p.findall("default:span", ns)
		text = ""
		for line in lines:
			text += textwrap.fill(textwrap.dedent(line.text).strip(), width=character_count)
			text += "\n"
		
		dict["text"] = text
		
		subs.append(dict)
	
	with open(out_file, "w") as file:
		for item in subs:
			file.write(str(item["id"]) + "\n")
			file.write(item["timecode"] + "\n")
			file.write(item["text"].encode('utf-8') + "\n")
			
			
def output_stl(out_file, body, ns, frame_rate, character_count):
	subs = []	
	for id, p in enumerate(body.findall("./default:div/default:p", ns)):
		dict = {}
		
		begin = p.get("begin")
		end = p.get("end")
		
		lines = p.findall("default:span", ns)
		text = u""
		for i, line in enumerate(lines):
			text += textwrap.fill(textwrap.dedent(line.text).strip(), width=character_count) + "\n"
		
		text = text.replace("\n", " | ")
		text = text[:-3]
		
		dict["entry"] = u"{0} , {1} , {2}".format(begin, end, text)
		subs.append(dict)
		
	with open(out_file, "w") as file:
		for item in subs:
			file.write(item["entry"].encode('utf-8') + "\n")
	
if __name__ == "__main__":
	main(sys.argv[1:])