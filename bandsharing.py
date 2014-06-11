#!/usr/bin/env python

#:::::::::::::::::::::::::::::::::::::::::::::::::::::
#Author:        Damiano Barboni <damianobarboni@gmail.com>
#Version:       0.1
#Description:   Script used to calculate Band Sharing between individuals from the same lines
#Changelog:     Wed Jun 11 12:07:33 CEST 2014
#               First test version     
#               
#:::::::::::::::::::::::::::::::::::::::::::::::::::::


class BandSharing():
    def __init__(self):
        self.input_file = "tests/test_data/test.csv"
        self.output_file = "out.csv"
        
        self.females = {}
        self.males   = {}
        
    def read(self):
        f = open( self.input_file, "r" )
        while True:
            line=f.readline()
            if not line: break
            print line.strip()
        f.close()
        
        
        
        None
    def write(self):
        None
    
    def run(self):
        self.read()
        
BandSharing().run()
