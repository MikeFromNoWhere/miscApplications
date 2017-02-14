#!/usr/bin/env python

"""unusedASA.py: This program finds unused objects within an ASA config. The goal is to reduce clutter within
                 a configuration."""

__author__ = "Mike Bydalek"
__version__ = "0.1"
__email__ = "mibydale@cisco.com"
__status__ = "Development"

import re
import sys
import argparse

parser = argparse.ArgumentParser(description='This app locates unused Object or Object-group items')

# Required argument: ASA Config File
parser.add_argument('asaFile', type=str, metavar='ASA_Config.txt',
                    help='ASA config text file to parse')

args = parser.parse_args()
asaFile = args.asaFile

# Check to see if file exists
try:
    asaConfig = open(asaFile)
except IOError:
        print ("Unable to open file: " + asaFile)
        quit(1)

# Destination lists
asaConfigLines = []
asaObjects = []

# Go through and get all the object and object-group names
objectRegex = re.compile('^(object|object-group) (network|service) (.+) (.+)$')

print ("Parsing File: " + asaFile)

with asaConfig as file:
    for line in file:
        line = line.strip()

        objectMatch = objectRegex.match(line)

        if objectMatch:
            asaObjects.append(objectMatch.group(3))
        else:
            asaConfigLines.append(line)

# Now go through and find any Objects that are *not* in the ASA Config
for object in asaObjects:
    objectRegex = re.compile('.*(' + str(object) + ').*')
    objectsFound = list(filter(objectRegex.match, asaConfigLines))

    if (len(objectsFound) == 0):
        print ("Object Not found: " + str(object))

# Fin
quit(0)
