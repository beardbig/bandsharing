#!/usr/bin/env python

#:::::::::::::::::::::::::::::::::::::::::::::::::::::
#Author:        Damiano Barboni <damianobarboni@gmail.com>
#Version:       0.1
#Description:   Script used to calculate Band Sharing between individuals from the same lines
#Changelog:     Wed Jun 11 12:07:33 CEST 2014
#               First test version     
#               
#:::::::::::::::::::::::::::::::::::::::::::::::::::::

import traceback

class BandSharing():
    def __init__(self):
        self.input_file = "tests/test_data/test.csv"
        self.output_file = "out.csv"
        
        self.females = {}
        self.males   = {}
    
    #:::::::::::::::::::::::::
    #      read dataset    
    #:::::::::::::::::::::::::
    def read(self):
        f = open( self.input_file, "r" )
        while True:
            line=f.readline()
            if not line: break
            self.parseLine( line )
        f.close()
        self.females[16].sort()
        print self.females[16]
        
    def parseLine( self, line ):
        try:
            cells = line.strip().split(",")
            gender = self.getGender( cells[ -1 ] )
            key = int( cells[ 0 ], 10 )
            if not key in gender: gender[ key ] = [] 
            gender[ key ].append( cells[ 2 ] + "-" + cells[ 1 ]  )
            gender[ key ].append( cells[ 3 ] + "-" + cells[ 1 ]  )
            gender[ key ].append( cells[ 4 ] + "-" + cells[ 1 ]  )
            gender[ key ].append( cells[ 5 ] + "-" + cells[ 1 ]  )
        except:
            print traceback.format_exc()
            #line doesn'tcontain valid data
            pass

    def getGender( self, cell ):
        print cell.lower()
        if cell.lower() == "m":
            gender = self.males
        elif cell.lower() == "f":
            gender = self.females
        else:
            gender = None
        return gender       

   
    def write(self):
        None
    def run( self ):
        self.read()
        
BandSharing().run()
