#!/usr/bin/env python

#:::::::::::::::::::::::::::::::::::::::::::::::::::::
#Author:        Damiano Barboni <damianobarboni@gmail.com>
#Version:       0.1
#Description:   Script used to test bandsharing.py
#Changelog:     Wed Jun 11 12:07:33 CEST 2014
#               First test version     
#               
#:::::::::::::::::::::::::::::::::::::::::::::::::::::


import os
import sys
import shutil
import unittest


current_path = os.path.realpath( __file__ ).split( os.path.basename(__file__) )[0]
bandsharing_path = os.path.abspath(os.path.join( current_path, os.pardir))
sys.path.insert(1, bandsharing_path)


class TestBandSharing( unittest.TestCase ):

    def setUp(self):        
        pass
    
    def test_bs( self ):
        pass
        
    def test_csv( self ):
        pass
            

def makeSuite():
    suite = unittest.TestSuite()
    suite.addTest( TestBandSharing( 'test_bs' ) )
    suite.addTest( TestBandSharing( 'test_csv' ) )
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=3).run(makeSuite())
