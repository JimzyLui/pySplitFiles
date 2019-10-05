#!c:\Python\Python36-32\python

import argparse
import os

"""
Split a file into multiple output files.

The first line read from 'filename' is a header line that is copied to every output file.

"""

def split_txt(txtFileName, pattern, maxlinesPerFile):
  txtPartial = None
  filecount=1
  totalLines = getFileLineCount(txtFileName)-1 # -1 for header
  with open(txtFileName,'r') as txt:
    headingRow = txt.readline()
    for index, line in enumerate(txt):
      if index % maxlinesPerFile == 0:
        if txtPartial:
          txtPartial.close()
        # newfile = pattern.format(index)
        newfile = pattern.format(filecount)
        filecount = filecount +1
        txtPartial = open(newfile, "w+")
        txtPartial.write(headingRow)
      elif (index % maxlinesPerFile ==maxlinesPerFile-1) or (index == totalLines -1):
        print('replace....', index, maxlinesPerFile, totalLines)
        line = replaceLast(line,',',';',1)
        print(line)
      txtPartial.write(line)
    if txtPartial:
      txtPartial.close()

def generateNewFilePattern(inputFilepath):
  filename_w_ext = os.path.basename(inputFilepath)
  filebasename, file_extension = os.path.splitext(filename_w_ext)
  pattern = filebasename+'_part_{0:03d}'+file_extension
  return pattern

''' replaces the last occurance of a value'''
def replaceLast(haystack, needle, newNeedle, occurance):
  list = haystack.rsplit(needle, occurance)
  return newNeedle.join(list)

def getFileLineCount(fname):
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog='pySplitFiles',
    description='Splits csv files into smaller ones with headings'
  )

  parser.add_argument("txtFileName", help="the name of the csv file to be split up")

  parser.add_argument("maxlinesPerFile", action='store', type=int, default=5, help="the max number of lines in each new file")

  args = parser.parse_args()

  namingPattern = generateNewFilePattern(args.txtFileName)
  # split_file('data.csv', 'part_{0:03d}.txt', 15)
  # split_txt(args.txtFileName, 'part_{0:03d}.txt', args.maxlinesPerFile)
  split_txt(args.txtFileName, namingPattern, args.maxlinesPerFile)