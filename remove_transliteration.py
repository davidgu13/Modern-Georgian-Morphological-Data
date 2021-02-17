import re
import sys

def remove_transliteration(file_name):
	with open(file_name,'r',encoding='utf8') as f:
		with open(file_name[:-4]+"_raw.txt",'w+',encoding='utf8') as fout:
			for line in f:
				line = re.sub('#\d+ - .+ - .+:','',line)
				line = re.sub('Screeve #\d+:\n','',line)
				line = re.sub(' = .+','',line)
				fout.write(line)

remove_transliteration(sys.argv[1]) # must be a .txt file in the format of the data files.