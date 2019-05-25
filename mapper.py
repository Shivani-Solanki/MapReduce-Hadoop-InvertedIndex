#!/usr/bin/env python

'''
Created on Mar 4, 2019

@author: solan
'''
from sys import stdin
import re
import os

for line in stdin:
  #  doc_id=1
        # Get the file path
    doc_id = os.environ["map_input_file"]

        # Get the name of the file from the path
    doc_id = re.findall(r'\w+', doc_id)[-2]

        # Get an array of all the words inside the document
    words = re.findall(r"[a-zA-Z]+", line.strip())
    new_list = []
    for e in words:
        if e.lower() not in ('and', 'but', 'is', 'the', 'to'):
            new_list.append(e)
    words = new_list

        # Map the words
    for word in words:
        print("%s\t%s:1" % (word.lower(), doc_id))