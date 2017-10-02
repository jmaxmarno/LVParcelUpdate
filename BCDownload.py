# -------------------------------------------------------------------------------
# Name:  Boulder County Data Download
# Purpose:
#
# Author:      Max
#
# Created:     05/01/2017
# Copyright:   (c) Max 2017
# Licence:     <your licence>
# -------------------------------------------------------------------------------

def main():
    pass
if __name__ == '__main__':
    main()

import os
import shutil
import sys
import zipfile
import requests
#import datetime  # Not needed for current config
# File urls
# Boulder County Data in shapefile format
BC_Parcels = "http://gis.bouldercounty.opendata.arcgis.com/datasets/89ae49d4ddf246388ee5f5e952aa84db_0.zip"
Municpalities = "http://gis.bouldercounty.opendata.arcgis.com/datasets/9597d3916aba47e887ca563d5ac15938_0.zip"
CountyBoundary = "http://gis.bouldercounty.opendata.arcgis.com/datasets/964b8f3b3dbe401bb28d49ac93d29dc4_0.zip"
# Assessor's Property Data
Account_Parcels = "http://assessor.boco.solutions/ASR_PublicDataFiles/Account_Parcels.csv"
Owner_Address = "http://assessor.boco.solutions/ASR_PublicDataFiles/Owner_Address.csv"
Buildings = "http://assessor.boco.solutions/ASR_PublicDataFiles/Buildings.csv"
Land = "http://assessor.boco.solutions/ASR_PublicDataFiles/Land.csv"
Permits = "http://assessor.boco.solutions/ASR_PublicDataFiles/Permits.csv"
Sales = "http://assessor.boco.solutions/ASR_PublicDataFiles/Sales.csv"
Tax_Areas = "http://assessor.boco.solutions/ASR_PublicDataFiles/Tax_Areas.csv"
Tax_Authorities = "http://assessor.boco.solutions/ASR_PublicDataFiles/Tax_Authorities.csv"
Values = "http://assessor.boco.solutions/ASR_PublicDataFiles/Values.csv"

file_path = os.path.dirname(os.path.realpath(__file__))
def create_folder(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            os.makedirs(path)
    except IOError as exception:
        raise IOError('%s: %s' % (path, exception.strerror))
    return None
create_folder(path = (file_path+"\\BC_DATA"))
os.chdir(file_path+"\\BC_DATA")

## get today's date for file name
##todaystr = str(datetime.date.today())
##todaysplit = todaystr.split("-")
##todayjoin = "".join(todaysplit)
def bcdnld(urlstr, namestr, fileextstr):
    r = requests.get(urlstr)
    if r.status_code == 200:
        print(namestr, 'URL Valid- ')
        print("Downloading with requests: ", urlstr)
        fname = namestr + fileextstr
        # to include today's date in filename substitute line below for line above
        ##    fname = namestr+"_"+todayjoin+fileextstr
        with open(fname, "wb") as code:
            code.write(r.content)
    else:
        print(namestr, " URL invalid!")

def extractshps(inputzip):
    try:
        zipref = zipfile.ZipFile(inputzip, "r")
        zipref.extractall()
        zipref.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])



############################################################################

# Download and extract Boulder County Parcel data (shapefile)
bcdnld(BC_Parcels, "Parcels", ".zip")
extractshps("Parcels.zip")
# Download and extract Boulder County Municipalities data (shapefile)
bcdnld(Municpalities, "Municipalities", ".zip")
extractshps("Municipalities.zip")
# Download and extract Boulder County Parcel data (shapefile)
bcdnld(CountyBoundary, "CountyBoundary", ".zip")
extractshps("CountyBoundary.zip")
# Download Assessor's Property Data
bcdnld(Values, "Values", ".csv")
bcdnld(Tax_Authorities, "Tax_Authorities", ".csv")
bcdnld(Tax_Areas, "Tax_Areas", ".csv")
bcdnld(Sales, "Sales", ".csv")
bcdnld(Permits, "Permits", ".csv")
bcdnld(Land, "Land", ".csv")
bcdnld(Buildings, "Buildings", ".csv")
bcdnld(Owner_Address, "Owner_Address", ".csv")
bcdnld(Account_Parcels, "Account_Parcels", ".csv")
print("Done Downloading")
