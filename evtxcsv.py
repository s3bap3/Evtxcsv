#!/usr/bin/python3
# evt/evtx to csv grep type file
# Requires the Evtx library located https://github.com/williballenthin/python-evtx
# To compile, pyinstaller --onefile  C:\Tools\Scripts\evtxcsvwin.py --distpath C:\Tools\Scripts\ --name evtxcsv.exe

from Evtx.Evtx import Evtx
from xml.etree.ElementTree import fromstring
from sys import exit, argv, exit
from glob import glob
from os import path, mkdir

def usage ():
	print ("\n\tUsage:")
	print ("\t\tevtxcsv.py -d <EVTX directory> <destination directory>\n")
	exit(1)

def convertlog(file, outpath):
	head, tail = path.split(file)
	file_name=tail.replace(".","-")+".csv"
	fullpath=path.join(outpath, file_name)
	print ("Converting {}".format(file_name))
	outfile = open(fullpath ,"w+")  
	with Evtx(file) as log:
		for record in log.records():
			root = fromstring(record.xml())
			for item in root[0]:
				if 'Provider' in item.tag:
					pass
				elif 'EventID' in item.tag:
					print_line(item.tag.rsplit('}', 1)[1], item.text, outfile)
				elif 'TimeCreated' in item.tag:
					print_line(item.tag.rsplit('}', 1)[1], item.attrib['SystemTime'], outfile)
				elif bool(item.attrib):
					print_line(item.tag.rsplit('}', 1)[1], item.attrib, outfile)
				else:
					print_line(item.tag.rsplit('}', 1)[1], item.text, outfile)
			for item in root[1]:
				if item.text != None:
					text = item.text.replace("\n"," ").replace("\t","")
				else:
					text = item.text
				if item.attrib.get('Name'):
					if 'LogonGuid' in item.attrib['Name']:
						print_line(item.attrib['Name'], text.strip('{}'), outfile)
					else:
						print_line(item.attrib['Name'], text, outfile)
				else:
					print_line(item.attrib, text, outfile)
			outfile.write("\n")
	outfile.close()

def print_line(tag1, tag2, outfile):
	try:
		outfile.write("{}:{},".format(tag1, tag2))
		#print ("{}:{}".format(tag1, tag2),end=',')
	except:
		try:
			outfile.write("{}:{},".format(tag1.encode('utf8'), tag2.encode('utf8')))
			#print ("{}:{}".format(tag1.encode('utf8'), tag2.encode('utf8')),end=',')
		except:
			outfile.write(str(tag1) + ":" + "".join(i for i in tag2.replace("|","") if ord(i) < 128 ))
		


if __name__ == "__main__":
	if (len(argv) == 4):
		parameter=argv[1] 
		input_path=argv[2]
		output_path=argv[3]+"/Evtxcsv"
		evtx_files = (glob(input_path+"/**/*.evtx", recursive=True))
		evt_files = (glob(input_path+"/**/*.evt", recursive=True))
		try:
			mkdir(output_path)
		except:
			pass
		for line in evtx_files:
			convertlog (line, output_path)
		for line in evt_files:
			convertlog (line, output_path)
	else:
		print ("\n[*] Missing Parameters")
		usage()
		
