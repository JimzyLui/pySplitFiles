#!c:\Python\Python36-32\python

import argparse
import os
import re 

"""
Split a file into multiple output files.

The first line read from 'filename' is a header line that is copied to every output file.

"""
def convertHeadingIntoInsertSQL(tablename, heading):
  # remove double quotes
  heading = heading.rstrip().replace('"','')
  newHeading = f"INSERT INTO {tablename}({heading}) values \n"
  return newHeading

def convertDataToSqlFormat(line):
  line = line.rstrip()
  print('raw: ',line)
  line = line.replace('\n',' ').replace('\r','')
  line= line.strip('\r\n')
  list = line.split('|')
  list[1]=fixDateField(list[1])  # change to YYYY-mm-dd
  list[3]=fixEmptyIntField(list[3], 0)
  list[6]=fixEmptyIntField(list[6], 0)
  print('list[6]',list[6])
  list[7]=fixEmptyIntField(list[7], 0)
  print('list[7]',list[7])
  list[8]=fixMemoField(list[8])
  print('list[8]',list[8])
  list[9]=fixDateField(list[9])  # change to YYYY-mm-dd
  print('list[9]',list[9])
  line = '|'.join(list)
  print('0: ',line)
  sqlLine = f"({line}),"
  print('1: ',sqlLine)
  sqlLine = sqlLine.replace('|)','|"")')
  print('2: ',sqlLine)
  sqlLine = sqlLine.replace('||','|""|')
  print('3: ',sqlLine+'\n')
  return sqlLine+'\n'

def convertCsvToSql(filename, sqlFileName, tablename):
  totalLines = getFileLineCount(filename)-1 # -1 for header
  with open(filename,'r') as txt:
    with open(sqlFileName,'w+') as sql:
      headingRow = txt.readline()
      headingRowSql = convertHeadingIntoInsertSQL(tablename, headingRow)
      headingRowSql = headingRowSql.replace('|',',')  # change over from pipes to comma
      sql.write(headingRowSql)
      for index, line in enumerate(txt):
        print(headingRow)
        line = convertDataToSqlFormat(line)
        line = line.replace('|',',')  # change over from pipes to comma
        if index == totalLines -1:
          print('replace....', index, totalLines)
          line = replaceLast(line,',',';',1)
          print(line)
        sql.write(line)


def generateSqlFileName(inputFilepath):
  filename_w_ext = os.path.basename(inputFilepath)
  filebasename, file_extension = os.path.splitext(filename_w_ext)
  sqlFileName = filebasename+'.sql'
  return sqlFileName

''' replaces the last occurance of a value'''
def replaceLast(haystack, needle, newNeedle, occurance):
  list = haystack.rsplit(needle, occurance)
  return newNeedle.join(list)

def getFileLineCount(fname):
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

def fixEmptyIntField(intVal, defaultVal):
  if not intVal:
    return str(defaultVal)
  return intVal


def fixDateField(strDate):
  if not strDate:
    return ""
  strDate = strDate.split()[0] #strip out the time
  listDate = strDate.strip('"').strip("'").split('/')
  return f'"{listDate[2]}-{listDate[0]}-{listDate[1]}"'

def fixMemoField(strMemo):
  if not strMemo:
    return ""
  # re.sub(needle, newNeedle, haystack, flags=re.IGNORECASE)
  strMemo = re.sub('pp#','PP-',strMemo,flags=re.IGNORECASE)
  strMemo = re.sub('pp# ','PP-',strMemo,flags=re.IGNORECASE)
  strMemo = re.sub('nat #','NAT-',strMemo,flags=re.IGNORECASE)
  strMemo = re.sub('also ','',strMemo,flags=re.IGNORECASE)
  strMemo = re.sub(' also','',strMemo,flags=re.IGNORECASE)
  strMemo = strMemo.replace('- ','-')
  strMemo = strMemo.replace(' -','-')
  return strMemo


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog='pyConvertCsvToSql',
    description='Makes a CSV file with a header row into an sql insert statement'
  )

  parser.add_argument("csvfilename", help="the name of the csv file to be split up")

  parser.add_argument("tablename", help="the name of the table for the resulting query")

  args = parser.parse_args()

  sqlFileName = generateSqlFileName(args.csvfilename)

  convertCsvToSql(args.csvfilename, sqlFileName, args.tablename)