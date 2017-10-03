# -------------------------------------------------------------------------------
# Name:  BC Data Staging gdb
# Purpose:
#
# Author:      Max
#
# Created:     05/01/2017
# Copyright:   (c) Max 2017
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import os
import arcpy


def main():
    pass
if __name__ == '__main__':
    main()

file_path = os.path.dirname(os.path.realpath(__file__))
file_path = r'C:\Users\Max\PycharmProjects\LVParcelUpdate'
os.chdir(file_path)
newgdb = file_path+r'\BoulderCountyData.gdb'
# Import arcpy module and setup environment

arcpy.env.overwriteOutput = True
if arcpy.Exists(newgdb):
    arcpy.Delete_management(newgdb)
arcpy.CreateFileGDB_management(out_folder_path=file_path, out_name="BoulderCountyData.gdb")
coordsys = arcpy.SpatialReference(2876)

arcpy.env.scratchWorkspace = newgdb
arcpy.env.workspace = newgdb
WorkingGDB= newgdb

# File Paths for Boulder Count and Assessor's Data
Datafolder = file_path+r"\BC_DATA"
Account_Parcels_csv = Datafolder+r"\Account_Parcels.csv"
Buildings_csv = Datafolder+r"\Buildings.csv"
Land_csv = Datafolder+r"\Land.csv"
Owner_Address_csv = Datafolder+r"\Owner_Address.csv"
Permits_csv = Datafolder+r"\Permits.csv"
Sales_csv = Datafolder+r"\Sales.csv"
Tax_Areas_csv = Datafolder+r"\Tax_Areas.csv"
Tax_Authorities_csv= r"\Tax_Authorities.csv"
Values_csv = Datafolder+r"\Values.csv"

Parcels_shp = Datafolder+r"\Parcels.shp"
County_Boundary_shp = Datafolder+r"\County_Boundary.shp"
Municipalities_shp = Datafolder+r"\Municipalities.shp"

#Process: Table to Table (Account_Parcels)
if arcpy.Exists("Account_Parcels"):
    arcpy.Delete_management("Account_Parcels")
arcpy.TableToTable_conversion(Account_Parcels_csv, WorkingGDB, "Account_Parcels")

# Process: Table to Table (Buildings)
if arcpy.Exists("Buildings"):
    arcpy.Delete_management("Buildings")
arcpy.TableToTable_conversion(Buildings_csv, WorkingGDB, "Buildings")

# Process: Table to Table (Land)
if arcpy.Exists("Land"):
    arcpy.Delete_management("Land")
arcpy.TableToTable_conversion(Land_csv, WorkingGDB, "Land")

# Process: Table to Table (Owner_Address)
if arcpy.Exists("Owner_Address"):
    arcpy.Delete_management("Owner_Address")
arcpy.TableToTable_conversion(Owner_Address_csv, WorkingGDB, "Owner_Address")

# Process: Table to Table (Values)
if arcpy.Exists("Values1"):
    arcpy.Delete_management("Values1")
arcpy.TableToTable_conversion(Values_csv,WorkingGDB,"Values1")

#####################################################################
# Import/Overwrite shapefiles to geodatabase
def inshape (shpfl, name):
    name = newgdb+'\\'+name
    if arcpy.Exists(name):
        arcpy.Delete_management(name)
    arcpy.Project_management(in_dataset=shpfl, out_dataset=name, out_coor_system=coordsys)
# Parcels
inshape(Parcels_shp, "BCParcels")
# Municipalities
inshape(Municipalities_shp, "Municipalities")
# Counties
inshape(County_Boundary_shp, "CountyBoundary")

# Select Specific Municipality by attribute value:
# The following inputs are layers or table views: "Municipalities"
arcpy.MakeFeatureLayer_management("Municipalities", "Municipalitieslyr")
MunSelection = arcpy.SelectLayerByAttribute_management(in_layer_or_view="Municipalitieslyr", selection_type="NEW_SELECTION", where_clause="ZONEDESC = 'Louisville'")
Municipality_Selection = "MunicipalBoundary"
arcpy.CopyFeatures_management(MunSelection, Municipality_Selection)

# Select by Location using Municipality Selection
def selbyloc (infeat, outfeat):
    selfeat = newgdb+'\\'+'MunicipalBoundary'
    if arcpy.Exists(outfeat):
        arcpy.Delete_management(outfeat)
    arcpy.MakeFeatureLayer_management(infeat, "templyr")
    lyrselection= arcpy.SelectLayerByLocation_management(in_layer="templyr", overlap_type="WITHIN_A_DISTANCE", select_features= selfeat, search_distance="1 Miles", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")
    arcpy.CopyFeatures_management(lyrselection, outfeat)
# Select and create new feature class (Parcels)
selbyloc(newgdb+"\\BCParcels",  newgdb+"\\Parcels_selection")

#
# QueryTable123 = arcpy.MakeQueryTable_management(["Account_Parcels","Parcels_Lyons"], "QueryTable123", "USE_KEY_FIELDS", "",
#  in_field="Parcels_Lyons.Shape #;Account_Parcels.strap #;Account_Parcels.Parcelno #",
#  where_clause="Account_Parcels.Parcelno = Parcels_Lyons.PARCEL_NO")
#
# ###Process: Make Query Table with only Account Parcels and Louisville_Parcel_shp
# ##arcpy.MakeQueryTable_management(["Account_Parcels", "Parcels_Lyons"], QueryTable1, "USE_KEY_FIELDS", "", "Account_Parcels.strap #;Account_Parcels.Parcelno #;Parcels_Lyons.Shape #", "Account_Parcels.Parcelno = Parcels_Lyons.PARCEL_NO")
#
# # Process: Copy Features
# if arcpy.Exists("QueryTable_Final"):
#     arcpy.Delete_management("QueryTable_Final")
# arcpy.CopyFeatures_management(QueryTable123, QueryTable_Final, "", "0", "0", "0")
#
# # Process: Join Field (Buildings)
# arcpy.JoinField_management(QueryTable_Final, "Account_Parcels_strap", "Buildings", "strap", "bldgClass;EffectiveYear;nbrBedRoom;nbrRoomsNobath;TotalFinishedSF;UnitCount")
#
# # Process: Join Field (Land)
# arcpy.JoinField_management(QueryTable_Final, "Account_Parcels_strap", "Land", "strap", "GIS_sqft;GIS_acreage")
#
# # Process: Join Field (Owner_Address)
# arcpy.JoinField_management(QueryTable_Final, "Account_Parcels_strap", "Owner_Address", "strap", "str_num;str;str_pfx;str_sfx;sub_dscr;owner_name;mailingAddr1;mailingAddr2;mailingCity;mailingState;mailingZip;legalDscr")
#
