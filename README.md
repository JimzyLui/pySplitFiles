# pySplitFiles

Two cli apps to process migration files

## Usage: pyConvertCsvToSql <pipeDelimitedFileName> <insertTableName> 

Takes a pipe (|) delimited file (that contains the columns in the first row) and converts it into an sql file that contains an insert statement

## Usage: pySplitFiles <txtFileName> <maxlinesPerFile>

Splits a file (any text file) into multiple output files.

maxlinesPerFile is the maximum number of lines you want in each new file.

The first line read from 'txtFileName' is a header line that is copied to every output file.
