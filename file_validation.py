#! /usr/bin/python

import os
import datetime
import sys
import math
import ajit
from collections import defaultdict


# define lists for storing metadata in memory
col_name=[]
col_type=[]
col_length=[]
col_format=[]
col_precision=[]
col_signed=[]
col_defaultvalue=[]



# function to read and store metadata
def readMetadata(metadatafile):
        fmeta=open(metadatafile, "r")
        global col_name, col_type, col_length, col_format, col_precision, col_signed, col_defaultvalue
        for line in fmeta:
                if line.startswith("#"): continue
                line = line.rstrip('\n').rsplit('|')
                col_name.append(line[0])
                col_type.append(line[1].lower())
                col_length.append(0) if (line[2] == "") else col_length.append(int(line[2]))
                col_format.append(line[3])
                col_precision.append(0) if (line[4] == "") else col_precision.append(int(line[4]))
                col_signed.append(line[5])
                col_defaultvalue.append(line[6])
        fmeta.close



# function to validate data file using metadata
def validateData(infile, outfile):
        fin=open("/home/edmfalcondev/ajit/"+infile, "r")
        fout=open(outfile, "w")
        for line in fin:
                line = line.rstrip('\n')
                record = line.rsplit('|')
                i=0
                message=""
                for col_val in record:
                        ret_val=ajit.isValid(col_val, col_type[i], col_length[i], col_format[i], \
                        col_precision[i], col_signed[i], col_defaultvalue[i])
                        if (ret_val != 0): message=message + "Invalid " + col_type[i] +  "-[" +  col_val + "];"
                        i+=1
                #if (message == "") : sys.stdout.write(line)
                #else : sys.stdout.write(line + "|" + message)
                if (message != "") : line=line + "|" + message + '\n';
                fout.write(line);
        fin.close()
        fout.close()



# read and process input data file line by line and column by column
def splitFilesAndValidate(infile, outfile, filesplitcount):
        fin=open(infile, "r")
        fins=[]
        finnames=[]
        foutnames=[]

        # create list of file handlers for split parts of input files
        i=0
        for i in range(filesplitcount):
                #f = open(infile + '_' + str(i), 'w')
                fins.append(open(infile + '_' + str(i), 'w'))
                finnames.append(infile + '_' + str(i))
                foutnames.append(outfile + '_' + str(i))

        # split main infile into subfiles
        i=0
        for line in fin:
                fins[i].write(line)
                i=0 if (i == filesplitcount-1) else i + 1

        # close and validate all split files
        for i in range(filesplitcount):
                fins[i].close()
                validateData(finnames[i], foutnames[i])



if __name__=="__main__":
        metadatafilename="metadata"
        infile="datafile.new"
        outfile="outfile"
        filesplitcount=3
        readMetadata(metadatafilename)
        splitFilesAndValidate(infile, outfile, filesplitcount)


#-EOF
