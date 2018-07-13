import os, sys, getopt, re
import xml.etree.ElementTree as Et


class ITTConvert(object):
    def __init__(self, *args):
        self.in_file = None
        self.out_file = None
        self.character_count = 32
        self.body = None
        self.ns = None
        
        try:
            opts, args = getopt.getopt(args, "i:o:c:")  # ":" indicates option requires argument
        except:
            print("\nUsage: itt_convert.py -i <input.itt> -o <output.srt> -c <character count>")
            print("Supported output formats: .srt .stl")
            print("Example: python itt_convert.py -i my_subs.itt -o new_subs.srt -c 32")
            sys.exit(2)
        
        for opt, arg in opts:
            if opt in "-i":
                self.in_file = os.path.abspath(arg)
            elif opt in "-o":
                self.out_file = os.path.abspath(arg)
            elif opt in "-c":
                self.character_count = int(arg)
        
        if not os.path.exists(self.in_file) or not self.in_file.endswith(".itt"):
            sys.exit("\nError: Input file does not exist or is not of type .itt")
        
        if not os.path.splitext(self.out_file)[1] in [".srt", ".stl"]:
            sys.exit("\nError: Output file does not end with .srt or .stl")
        
        tree = Et.parse(self.in_file)
        root = tree.getroot()
        
        # namespaces
        self.ns = {"default": root.tag.split('}', 1)[0][1:], "tts": "http://www.w3.org/ns/ttml#styling"}
        self.body = root.find("default:body", self.ns)
        
        # find frame rate
        self.frame_rate = None
        for name, value in root.attrib.items():
            if name.endswith("frameRate"):
                self.frame_rate = float(value)
        
        if self.frame_rate is None:
            sys.exit("\nCould not determine frame rate from file.")
        
        if self.out_file.endswith(".srt"):
            self.output_srt()
        elif self.out_file.endswith(".stl"):
            self.output_stl()
    
    def output_srt(self):
        subtitles = []
        
        xml = Et.tostring(self.body, "iso_8859_2", "xml")
        xml = re.sub("(<ns\d:br.*?>)", "\n", xml)
        xml = re.sub("(<br.*?>)", "\n", xml)
        self.body = Et.fromstring(xml)
        
        for i, p in enumerate(self.body.findall("./default:div/default:p", self.ns)):
            subtitle = {"id": i + 1}
            
            begin = p.get("begin").split(":")
            begin = "{0}:{1}:{2},{3}".format(begin[0],
                                             begin[1],
                                             begin[2],
                                             "{0:.3f}".format(float(begin[3]) / self.frame_rate).split(".")[1])
            
            end = p.get("end").split(":")
            end = "{0}:{1}:{2},{3}".format(end[0],
                                           end[1],
                                           end[2],
                                           "{0:.3f}".format(float(end[3]) / self.frame_rate).split(".")[1])
            
            # srt region
            # {\an7} {\an8} {\an9} top
            # {\an4} {\an5} {\an6} middle
            # {\an1} {\an2} {\an3} bottom
            region = p.get("region")
            if "bottom" in region:
                region = ""
            elif "top" in region:
                region = "{\\an8}"  # top-center, escape "\"
            
            subtitle["timecode"] = "{0} --> {1}".format(begin, end)
            
            spans = p.findall("default:span", self.ns)
            text = region
            for span in spans:
                if span.text is None:
                    continue
                
                content = ""
                for t in span.text.split("\n"):
                    t = t.strip()
                    if t:
                        content += t
                    else:
                        content += "\n"
                
                style = span.get("{http://www.w3.org/ns/ttml#styling}fontStyle")
                weight = span.get("{http://www.w3.org/ns/ttml#styling}fontWeight")
                
                if str(style) in "italic":
                    content = "<i>" + content + " </i>"
                if str(weight) in "bold":
                    content = "<b>" + content + " </b>"
                
                text += content
            
            subtitle["text"] = text + "\n"
            
            subtitles.append(subtitle)
        
        with open(self.out_file, "w") as f:
            for item in subtitles:
                f.write(str(item["id"]) + "\n")
                f.write(item["timecode"] + "\n")
                f.write(item["text"].encode("utf-8") + "\n")
    
    def output_stl(self):
        subtitles = []
        
        xml = Et.tostring(self.body, "iso_8859_2", "xml")
        xml = re.sub("(<ns\d:br.*?>)", "\n", xml)
        xml = re.sub("(<br.*?>)", "\n", xml)
        self.body = Et.fromstring(xml)
        
        for j, p in enumerate(self.body.findall("./default:div/default:p", self.ns)):
            subtitle = {}
            
            begin = p.get("begin")
            end = p.get("end")
            
            region = p.get("region")
            if "bottom" in region:
                region = "$VertAlign = bottom"
            elif "top" in region:
                region = "$VertAlign = top"
            
            spans = p.findall("default:span", self.ns)
            text = ""
            for span in spans:
                if span.text is None:
                    continue
                
                content = ""
                for t in span.text.split("\n"):
                    t = t.strip()
                    if t:
                        content += t
                    else:
                        content += " | "
                
                style = span.get("{http://www.w3.org/ns/ttml#styling}fontStyle")
                weight = span.get("{http://www.w3.org/ns/ttml#styling}fontWeight")
                
                if str(style) in "italic":
                    content = "^I" + content + "^I"
                if str(weight) in "bold":
                    content = "^B" + content + "^B"
                
                text += content + " "  # todo: whitespace after each span (check this!)
            
            text = text.replace("\n", " | ")
            
            subtitle["region"] = region
            subtitle["entry"] = u"{0} , {1} , {2}\n".format(begin, end, text)
            
            subtitles.append(subtitle)
        
        with open(self.out_file, "w") as f:
            for item in subtitles:
                f.write(item["region"].encode("utf-8") + "\n")
                f.write(item["entry"].encode("utf-8") + "\n")
    
    @staticmethod
    def wrap_words(text, max_width, breakchar="\n", ignore=[]):
        lines = text.split(breakchar)
        
        for line in lines:
            ignore_count = 0
            for s in ignore:
                ignore_count += line.count(s)
            
            count = 0
            while True:
                last_pos = count
                count = line.find(" ", last_pos)
                
                if count == -1:
                    break
                elif count > max_width:
                    line = line[:last_pos] + breakchar + line[last_pos:]


if __name__ == "__main__":
    m = ITTConvert(*sys.argv[1:])
