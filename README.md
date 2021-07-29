# Evtxcsv
The Evtxcsv is a tool that leverages the Python Evtx library to convert Evt/Evtx Windows Log files into CSV format. This repository includes a Python script for both Windows and Linux, plus a compiled standalone version for Windows

The script will recursively search for evt or evtx files and convert those into CSV in the specified output folder

## Requirements
The following package is required for the Python version to work
https://github.com/williballenthin/python-evtx

## Command
	evtxcsv.py -d <EVTX directory> <destination directory>

