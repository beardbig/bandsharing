#!/usr/bin/env python

#:::::::::::::::::::::::::::::::::::::::::::::::::::::
#Author:        Damiano Barboni <damianobarboni@gmail.com>
#Version:       0.1
#Description:   Band Sharing gender independent
#Changelog:     Wed May  6 10:08:31 CEST 2015
#
#::::::::::::::::::::::::::::::::::::::::::::::::::::

from bandsharing import BandSharing

if __name__ == '__main__':
    bs_rainbow = BandSharing()
    bs_rainbow.setVatican( False )
    bs_rainbow.run()
