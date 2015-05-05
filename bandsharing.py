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
        
        
        self.females = {} #list of females
        self.males   = {} #list of males
        self.bisex   = {} #list of individuals without gender column       
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
            gender = self.getGender( cells )
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

    def getGender( self, cells ):
        cell = cells[ -1 ]
        if cell.lower() == "m":
            gender = self.males
        elif cell.lower() == "f":
            gender = self.females
        else:
            gender = self.bisex
        return gender       
    
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
        for gender_list in [ self.females, self.males, self.bisex ]:
            for el in gender_list:
                gender_list[ el ].sort()
        
    def getSharedBands(self, female_id, male_id):
        count_shared = 0
        for band_f in self.females[ female_id ]:
            for band_m in self.males[ male_id ]:
                if band_f == band_m:
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
    def getValidData(self, female, male):
        valid_female_locus = self.getLocus( female )
        valid_male_locus   = self.getLocus( male )
        tot_f = 0
        tot_m = 0
        incomplete_locus = []
        for b in female:
            locus = b.split("-")[1]
            if locus in valid_male_locus:
                tot_f += 1
            else:
                if not locus in incomplete_locus: incomplete_locus.append( locus )
        
        for b in male:
            locus = b.split("-")[1]
            if locus in valid_female_locus:
                tot_m += 1
            else:
                if not locus in incomplete_locus: incomplete_locus.append( locus )
        return tot_f, tot_m, '_'.join( incomplete_locus )
        
    def matchAll(self):
        sys.stdout.write( 'Compute Band Sharing' )                                                                                                                                                                 
        sys.stdout.flush()
        
        bandsharing = {}
        for f in self.females:
            for m in self.males:
                self.running()
                
                tot_shared  = self.getSharedBands( f, m )
                tot_f, tot_m, incomplete_locus = self.getValidData( self.females[ f ], self.males[ m ] )                  
                band_sharing = ( 2.0 * tot_shared ) / ( tot_f + tot_m )
                bandsharing[ ( "%d-%d-%d-%d-%d-%s" %( f, m, tot_shared, tot_f, tot_m, incomplete_locus ) ) ] = band_sharing
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
        self.writeDetails( f )
        
        f.write( "\n\n\n%s" %( SIGNATURE ) )
        
        f.close()
        self.ok()
    
    def writeBandsharing( self, f ):
        
        #write bandsharing
        f.write( "Female ID,Male ID,Band Sharing,1-BS,Nfm,Nf,Nm,Ignored Locus (bacause incomplete)\n" )
        for bs in self.bandsharing:
            Female_ID     = bs[ 0 ].split( "-" )[ 0 ]
            Male_ID       = bs[ 0 ].split( "-" )[ 1 ] 
            Band_Sharing  = bs[ 1 ]
            Nfm           = bs[ 0 ].split( "-" )[ 2 ]
            Nf            = bs[ 0 ].split( "-" )[ 3 ]
            Nm            = bs[ 0 ].split( "-" )[ 4 ]
            Nm            = bs[ 0 ].split( "-" )[ 4 ]
            IgnoredLocus = bs[ 0 ].split( "-" )[ 5 ].replace("_", " ")
            match_string = "%s,%s,%f,%f,%s,%s,%s,%s\n" %( Female_ID, Male_ID, Band_Sharing, 1-Band_Sharing, Nfm, Nf, Nm, IgnoredLocus ) 
            f.write( match_string )
        
    def writeDetails( self, f ):
        #write bandsharing
        f.write( "\n\nBand Sharing details\n\n" )
        for bs in self.bandsharing:
            self.running()
            Female_ID    = int( bs[ 0 ].split( "-" )[ 0 ], 10 )
            Male_ID      = int( bs[ 0 ].split( "-" )[ 1 ], 10 )  
            
            female_bands = self.females[ Female_ID ]
            male_bands   = self.males[ Male_ID ]
            bandsharing  = bs[ 1 ]
            ignored_locus = bs[ 0 ].split("-")[-1].split("_")

            f.write( "Love affinity details between female id %s an male id %s (Band Sharing = %f and Ignored Locus = %s )\n" %( Female_ID, Male_ID, bandsharing, ' '.join( ignored_locus ) ) )
                
            #run until left or right is out
            i, j = 0, 0
            while i < len( female_bands ) and j < len( male_bands ):
                female_band_val = female_bands[ i ].split("-")[0]
                male_band_val   = male_bands[ j ].split("-")[0]
                
                female_band_locus = female_bands[ i ].split("-")[1]
                male_band_locus   = male_bands[ j ].split("-")[1]
                
                #if current left val is < current right val; assign to master list
                if female_band_val < male_band_val:
                    if female_band_locus not in ignored_locus:
                        f.write( "%s,\n" %( female_bands[ i ]) )
                    i += 1; 
                elif female_band_val == male_band_val:
                    if female_band_locus not in ignored_locus and female_band_locus not in ignored_locus:
                        f.write( "%s,%s\n" %( female_bands[ i ], male_bands[ j ]) )
                    i += 1; j += 1
                else:
                    if male_band_locus not in ignored_locus:
                        f.write( ",%s\n" %( male_bands[ j ]) )
                    j += 1;
            
            if i < len( female_bands ):
                for k in range( i, len( female_bands ) ):
                    f.write( "%s,\n" %( female_bands[ k ]) )
            elif j < len( male_bands ):
                for k in range( j, len( male_bands ) ):
                    f.write( ",%s\n" %( male_bands[ k ]) )
            
            
            f.write( "\n" )
            
            
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def run( self ):
        for input_filename_complete in glob.glob( os.path.join( self.input_dir, "*.csv" ) ):
            input_filename = os.path.basename( input_filename_complete )
            self.read( input_filename_complete )
            self.orderVectors()
            self.matchAll()
            
            output_filename = "computed_bandsharing_" + input_filename
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
            self.females = {}
            self.males   = {}
            self.bisex   = {}
            self.bandsharing = []
            
                    
    def ok( self ):
        sys.stdout.write( '[ OK ]\n' )                                                                                                                                                                 
        sys.stdout.flush()
    
    def running( self ):
        sys.stdout.write( '.' )                                                                                                                                                                 
        sys.stdout.flush()
    
    

if __name__ == '__main__': 
    BandSharing().run()
