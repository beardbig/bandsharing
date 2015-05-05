#!/usr/bin/env python

#:::::::::::::::::::::::::::::::::::::::::::::::::::::
#Author:        Damiano Barboni <damianobarboni@gmail.com>
#Version:       0.1
#Description:   Script used to calculate Band Sharing between individuals from the same lines
#Changelog:     Wed Jun 11 12:07:33 CEST 2014
#               First test version     
#               
#               Fri Jun 13 16:46:22 CEST 2014
#               Ignore incomplete locus
#               Match bands only from same locus
#
#               Fri Jun 13 16:47:34 CEST 2014
#               Commit first working version
#:::::::::::::::::::::::::::::::::::::::::::::::::::::

import traceback
import operator
import sys
from time import gmtime, strftime
import os
import glob

SIGNATURE    = "CSV produced by bandsharing utility.\nhttps://github.com/beardbig/bandsharing\nAuthor: Damiano Barboni <damianobarboni@gmail.com>"
current_path = os.path.realpath( __file__ ).split( os.path.basename(__file__) )[0]
OVERWRITE    = True

class BandSharing():
    def __init__(self):
        self.input_dir = os.path.join( current_path, "input" )
        self.output_dir = os.path.join( current_path, "output" )
        if not os.path.isdir( self.output_dir ):
            os.mkdir( self.output_dir )
            print "create output directory %s...............[ OK ]" %( self.output_dir )
        
        
        #self.females = {} #list of females
        #self.males   = {} #list of males
        #self.bisex   = {} #list of individuals without gender column       
        self.unisex  = {} #unified list --> females + males + bisex  
        #results
        self.bandsharing = []
    
    #:::::::::::::::::::::::::
    #      read dataset    
    #:::::::::::::::::::::::::
    def read(self, input_file ):
        sys.stdout.write( 'Read input file %s' %( input_file ) )                                                                                                                                                                 
        sys.stdout.flush()
        
        f = open( input_file , "r" )
        while True:
            line=f.readline()
            if not line: break
            self.parseLine( line )
        f.close()
        self.ok()
        
        
    def parseLine( self, line ):
        try:
            cells = line.strip().split(",")
            #each line must contains at leas 4 elements
            if cells < 4: raise 
            
            #get gender and id
            gender = self.unisex #self.getGender( cells )
            key = self.getId( cells )
            
            #add new value to dict if not exists
            if not key in gender:
                gender[ key ] = []
                self.running()
            
            #insert Allele
            gender[ key ].extend( self.getBands( cells ) )
            
        except:
            #line doesn'tcontain valid data
            pass
    """
    def getGender( self, cells ):
        cell = cells[ -1 ]
        if cell.lower() == "m":
            gender = self.males
        elif cell.lower() == "f":
            gender = self.females
        else:
            gender = self.bisex
        return gender       
    """

    def getId( self, cells ):
        return int( cells[ 0 ], 10 )
    
    def getBands(self, cells ):
        bands = []
        locus = cells[ 1 ]
        for i in range( 2, len( cells) -1 ):
            #empty cells considered as 0
            if cells[ i ] != "0" and cells[ i ].strip():
                bands.append( cells[ i ] + "-" + locus  )
        return bands
    
    
    
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #      perform bandsharing evaluiation and order vectors    
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def orderVectors(self):
        for el in self.unisex:
            self.unisex[ el ].sort()
        
    def getSharedBands(self, id_1, id_2):
        count_shared = 0
        for band_1 in self.unisex[ id_1 ]:
            for band_2 in self.unisex[ id_2 ]:
                if band_1 == band_2:
                    count_shared += 1
                    break
        return count_shared
    
    def getLocus(self, band_list):
        valid_locus = []
        for b in band_list:
            locus = b.split("-")[1]
            if not locus in valid_locus: valid_locus.append( locus )
        return valid_locus
                
            
    #verify complete lolcus
    def getValidData(self, ind1, ind2 ):
        valid_ind1_locus = self.getLocus( ind1 )
        valid_ind2_locus   = self.getLocus( ind2 )
        tot_ind1 = 0
        tot_ind2 = 0
        incomplete_locus = []
        for b in ind1:
            locus = b.split("-")[1]
            if locus in valid_ind2_locus:
                tot_ind1 += 1
            else:
                if not locus in incomplete_locus: incomplete_locus.append( locus )
        
        for b in ind2:
            locus = b.split("-")[1]
            if locus in valid_ind1_locus:
                tot_ind2 += 1
            else:
                if not locus in incomplete_locus: incomplete_locus.append( locus )
        return tot_ind1, tot_ind2, '_'.join( incomplete_locus )
        
    def matchAll(self):
        sys.stdout.write( 'Compute Band Sharing' )                                                                                                                                                                 
        sys.stdout.flush()
        
        bandsharing = {}
        for individual_1 in self.unisex:
            for individual_2 in self.unisex:
                if individual_1 > individual_2:
                    self.running()
                
                    tot_shared  = self.getSharedBands( individual_1, individual_2 )
                    tot_individual_1, tot_individual_2, incomplete_locus = self.getValidData( self.unisex[ individual_1 ], self.unisex[ individual_2 ] )                  
                    band_sharing = ( 2.0 * tot_shared ) / ( tot_individual_1 + tot_individual_2 )
                    bandsharing[ ( "%d-%d-%d-%d-%d-%s" %( individual_1, individual_2, tot_shared, tot_individual_1, tot_individual_2, incomplete_locus ) ) ] = band_sharing

        self.bandsharing = sorted( bandsharing.iteritems(), key = operator.itemgetter( 1 ) )
        self.ok()
    
    #::::::::::::::::::::::::::
    #      write output     
    #::::::::::::::::::::::::::
    def write( self, output_file, input_file ):
        sys.stdout.write( 'Write output file %s' %( output_file ) )                                                                                                                                                                 
        sys.stdout.flush()
        
        f = open( output_file, "w" )
        
        current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
        f.write( "Band Sharing produced using %s file\n" %( input_file ) )
        f.write( "Producet Time,%s\n\n\n" %( current_time ) )
        
        self.writeBandsharing( f )
        self.writeMatrix( f )
        self.writeDetails( f )
        
        f.write( "\n\n\n%s" %( SIGNATURE ) )
        
        f.close()
        self.ok()
    
    def writeBandsharing( self, f ):
        
        #write bandsharing
        f.write( "Individual 1, Individual 2,Band Sharing,1-BS,N12,N1,N2,Ignored Locus (bacause incomplete)\n" )
        for bs in self.bandsharing:
            ind1_ID       = bs[ 0 ].split( "-" )[ 0 ]
            ind2_ID       = bs[ 0 ].split( "-" )[ 1 ] 
            Band_Sharing  = bs[ 1 ]
            N12           = bs[ 0 ].split( "-" )[ 2 ]
            N1            = bs[ 0 ].split( "-" )[ 3 ]
            N2            = bs[ 0 ].split( "-" )[ 4 ]
            IgnoredLocus  = bs[ 0 ].split( "-" )[ 5 ].replace("_", " ")
            match_string  = "%s,%s,%f,%f,%s,%s,%s,%s\n" %( ind1_ID, ind2_ID, Band_Sharing, 1-Band_Sharing, N12, N1, N2, IgnoredLocus ) 
            f.write( match_string )
    def getBS( self, el1, el2 ):
        key1 = "%s-%s-" %( el1, el2 )
        key2 = "%s-%s-" %( el2, el1 )
        for bs in self.bandsharing:
            if bs[ 0 ].startswith( key1 ) or bs[ 0 ].startswith( key2 ):
                return bs[ 1 ]
            
    def writeMatrix( self, f ):
        f.write( "\n\nBand Sharing summary matrix\n\n" )
        keys = self.unisex.keys()
        keys.sort()
        f.write( "BS \ 1-BS")
        for el in keys:
            f.write( ",%s" %( el ))
        f.write( "\n" )
        for el1 in keys:
            f.write( "%s" %( el1 ) )
            for el2 in keys:
                f.write( ",")
                if el1 > el2:
                    f.write( "%f" %( self.getBS( el1, el2 ) ) )
                elif el1 < el2:
                    f.write( "%f" %( 1 - self.getBS( el1, el2 ) ) )
            f.write( "\n" )
            

    def writeDetails( self, f ):
        #write bandsharing
        f.write( "\n\nBand Sharing details\n\n" )
        for bs in self.bandsharing:
            self.running()
            ind1_ID    = int( bs[ 0 ].split( "-" )[ 0 ], 10 )
            ind2_ID    = int( bs[ 0 ].split( "-" )[ 1 ], 10 )  
            
            ind1_bands = self.unisex[ ind1_ID ]
            ind2_bands = self.unisex[ ind2_ID ]
            bandsharing  = bs[ 1 ]
            ignored_locus = bs[ 0 ].split("-")[-1].split("_")

            f.write( "Love affinity details between individual ID %s an individual ID %s (Band Sharing = %f and Ignored Locus = %s )\n" %( ind1_ID, ind2_ID, bandsharing, ' '.join( ignored_locus ) ) )
                
            #run until left or right is out
            i, j = 0, 0
            while i < len( ind1_bands ) and j < len( ind2_bands ):
                ind1_band_val = ind1_bands[ i ].split("-")[0]
                ind2_band_val = ind2_bands[ j ].split("-")[0]
                
                ind1_band_locus = ind1_bands[ i ].split("-")[1]
                ind2_band_locus = ind2_bands[ j ].split("-")[1]
                
                #if current left val is < current right val; assign to master list
                if ind1_band_val < ind2_band_val:
                    if ind1_band_locus not in ignored_locus:
                        f.write( "%s,\n" %( ind1_bands[ i ]) )
                    i += 1; 
                elif ind1_band_val == ind2_band_val:
                    if ind1_band_locus not in ignored_locus and ind1_band_locus not in ignored_locus:
                        f.write( "%s,%s\n" %( ind1_bands[ i ], ind2_bands[ j ]) )
                    i += 1; j += 1
                else:
                    if ind2_band_locus not in ignored_locus:
                        f.write( ",%s\n" %( ind2_bands[ j ]) )
                    j += 1;
            
            if i < len( ind1_bands ):
                for k in range( i, len( ind1_bands ) ):
                    f.write( "%s,\n" %( ind1_bands[ k ]) )
            elif j < len( ind2_bands ):
                for k in range( j, len( ind2_bands ) ):
                    f.write( ",%s\n" %( ind2_bands[ k ]) )
            
            
            f.write( "\n" )
            
            
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def run( self ):
        for input_filename_complete in glob.glob( os.path.join( self.input_dir, "*.csv" ) ):
            input_filename = os.path.basename( input_filename_complete )
            self.read( input_filename_complete )
            self.orderVectors()
            self.matchAll()
            
            output_filename = "rainbow_bandsharing_" + input_filename
            output_filename_complete = os.path.join( self.output_dir, output_filename )
            if not os.path.isfile( output_filename_complete ) or OVERWRITE:
                self.write( output_filename_complete, input_filename )
            else:    
                query_response = raw_input("A file named %s in the output directory already exists. Overwrite ? [ Enter (y)es or (n)o: ] " %( output_filename ))
                if query_response.lower() == "yes" or query_response.lower() == "y":
                    self.write( output_filename_complete, input_filename )
                else:
                    print "skipp %s" %( output_filename )
            
            #reset variables
            #self.females = {}
            #self.males   = {}
            #self.bisex   = {}
            self.unisex = {}
            self.bandsharing = []
            
                    
    def ok( self ):
        sys.stdout.write( '[ OK ]\n' )                                                                                                                                                                 
        sys.stdout.flush()
    
    def running( self ):
        sys.stdout.write( '.' )                                                                                                                                                                 
        sys.stdout.flush()
    
    

if __name__ == '__main__': 
    BandSharing().run()
