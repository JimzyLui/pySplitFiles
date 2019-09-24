

# from itertools import chain
import csv
import argparse
import os

def split_file(filename, pattern, size):
    """
    Split a file into multiple output files.

    The first line read from 'filename' is a header line that is copied to every output file. The remaining lines are split into blocks of at least 'size' characters and written to output files whose names are pattern.format(1), pattern.format(2), and so on. The last output file may be short.

    """
    with open(filename, 'r') as f:
        header = next(f)
        for index, line in enumerate(f, start=1):
            with open(pattern.format(index), 'w') as out:
                out.write(header)
                n = 0
                for line in chain([line], f):
                    out.write(line)
                    n += len(line)
                    if n >= size:
                        break

def split_csv(filename, pattern, maxlines):
  arrHeadings = []
  with open(filename, newline='') as f:
    csv_reader = csv.reader(f,delimiter=',')
    arrHeadings = next(csv_reader,None)
    file_counter=1
    # print(arrHeadings)
    for index, line in enumerate(f, start=1):
      print('line #',index)
      newfile = pattern.format(index)
      print('-->new filename:',newfile, index)
      with open(newfile, 'w', newline='') as csv_partialfile:
        rowcount = 1
        csv_writer = csv.writer(csv_partialfile, delimiter=',')
        csv_writer.writerow(arrHeadings)
        for row in csv_reader:
          # print(row)
          csv_writer.writerow(row)

          # print('line: ',line)
          rowcount=rowcount+1
          if rowcount >= maxlines:
            # print('break:',index, row)
            file_counter = file_counter +1
            break


def split_txt(filename, pattern, maxlines):
  txtPartial = None
  filecount=1
  with open(filename,'r') as txt:
    headingRow = txt.readline()
    for index, line in enumerate(txt):
      if index % maxlines == 0:
        if txtPartial:
          txtPartial.close()
        # newfile = pattern.format(index)
        newfile = pattern.format(filecount)
        filecount = filecount +1
        txtPartial = open(newfile, "w")
        txtPartial.write(headingRow)
      txtPartial.write(line)
    if txtPartial:
      txtPartial.close()

def generateNewFilePattern(inputFilepath):
  filename_w_ext = os.path.basename(inputFilepath)
  filebasename, file_extension = os.path.splitext(filename_w_ext)
  pattern = filebasename+'_part_{0:03d}'+'.'+file_extension
  return pattern

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog='pySplitFiles',
    description='Splits csv files into smaller ones with headings'
  )

  parser.add_argument("csvfilename", help="the name of the csv file to be split up")

  parser.add_argument("maxlines", action='store', type=int, default=5, help="the max number of lines in each new file")

  args = parser.parse_args()

  namingPattern = generateNewFilePattern(args.csvfilename)
  # split_file('data.csv', 'part_{0:03d}.txt', 15)
  # split_txt(args.csvfilename, 'part_{0:03d}.txt', args.maxlines)
  split_txt(args.csvfilename, namingPattern, args.maxlines)