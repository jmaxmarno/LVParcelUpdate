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
# Import arcpy module and setup environment
import os
import arcpy
import sys
def main():
    pass
if __name__ == '__main__':
    main()
try:

    # TARGET MUNICIPALITY: (MUST BE IN SINGLE QUOTES!!)
    municpality = "'Louisville'"
    coordsys = arcpy.SpatialReference(2876)
    # SET WORKSPACE AND CREATE STAGING GDB
    # file_path = os.path.dirname(os.path.realpath(__file__)) #DOES NOT WORK WHEN RUN FROM CONSOLE
    file_path = r'C:\Users\Max\PycharmProjects\LVParcelUpdate'
    os.chdir(file_path)
    WorkingGDB = file_path + r'\BCDStaging.gdb'
    arcpy.env.overwriteOutput = True
    if arcpy.Exists(WorkingGDB):
        arcpy.Delete_management(WorkingGDB)
    arcpy.CreateFileGDB_management(out_folder_path=file_path, out_name="BCDStaging.gdb")
    arcpy.env.scratchWorkspace = WorkingGDB
    arcpy.env.workspace = WorkingGDB

    # File Paths for Boulder County and Assessor's Data
    Datafolder = file_path + r"\BC_DATA"
    Account_Parcels_csv = Datafolder + r"\Account_Parcels.csv"
    Buildings_csv = Datafolder + r"\Buildings.csv"
    Land_csv = Datafolder + r"\Land.csv"
    Owner_Address_csv = Datafolder + r"\Owner_Address.csv"
    Permits_csv = Datafolder + r"\Permits.csv"
    Sales_csv = Datafolder + r"\Sales.csv"
    Tax_Areas_csv = Datafolder + r"\Tax_Areas.csv"
    Tax_Authorities_csv = r"\Tax_Authorities.csv"
    Values_csv = Datafolder + r"\Values.csv"

    Parcels_shp = Datafolder + r"\Parcels.shp"
    County_Boundary_shp = Datafolder + r"\County_Boundary.shp"
    Municipalities_shp = Datafolder + r"\Municipalities.shp"



    # Process: Table to Table (Account_Parcels)
    if arcpy.Exists("Account_Parcels"):
        arcpy.Delete_management("Account_Parcels")
    arcpy.TableToGeodatabase_conversion(Account_Parcels_csv, WorkingGDB)
    arcpy.AddField_management("Account_Parcels", field_name="PARCEL_NO", field_type='Text')
    arcpy.CalculateField_management(in_table="Account_Parcels", field="PARCEL_NO", expression="!Parcelno!")

    # Process: Table to Table (Buildings)
    if arcpy.Exists("Buildings"):
        arcpy.Delete_management("Buildings")
    arcpy.TableToGeodatabase_conversion(Buildings_csv, WorkingGDB)

    # Process: Table to Table (Owner_Address)
    if arcpy.Exists("Owner_Address"):
        arcpy.Delete_management("Owner_Address")
    arcpy.TableToGeodatabase_conversion(Owner_Address_csv, WorkingGDB)
    #
    # # Process: Table to Table (Land)
    # if arcpy.Exists("Land"):
    #     arcpy.Delete_management("Land")
    # arcpy.TableToGeodatabase_conversion(Land_csv, WorkingGDB)
    #
    # # Process: Table to Table (Values)
    # if arcpy.Exists("Values_"):
    #     arcpy.Delete_management("Values_")
    # arcpy.TableToGeodatabase_conversion(Values_csv, WorkingGDB)
    #

    #####################################################################
    # Import/Overwrite shapefiles to geodatabase
    def inshape(shpfl, name):
        name = WorkingGDB + '\\' + name
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
    MunSelection = arcpy.SelectLayerByAttribute_management(in_layer_or_view="Municipalitieslyr",
                                                           selection_type="NEW_SELECTION",
                                                           where_clause="ZONEDESC = " + municpality)
    Municipality_Selection = "MunicipalBoundary"
    arcpy.CopyFeatures_management(MunSelection, Municipality_Selection)


    # Select parcels by Location using Municipality Selection and 500 ft buffer
    def selbyloc(infeat, outfeat):
        selfeat = WorkingGDB + '\\' + 'MunicipalBoundary'
        if arcpy.Exists(outfeat):
            arcpy.Delete_management(outfeat)
        arcpy.MakeFeatureLayer_management(infeat, "templyr")
        lyrselection = arcpy.SelectLayerByLocation_management(in_layer="templyr", overlap_type="WITHIN_A_DISTANCE",
                                                              select_features=selfeat, search_distance="500 Feet",
                                                              selection_type="NEW_SELECTION",
                                                              invert_spatial_relationship="NOT_INVERT")
        arcpy.CopyFeatures_management(lyrselection, outfeat)
    selbyloc(WorkingGDB + "\\BCParcels", WorkingGDB + "\\" + "Parcels_selection")
    # GENERATE QUERY TABLE (AS LAYER - THEREFORE MUST BE COPIED)
    QueryTable123 = arcpy.MakeQueryTable_management(["Account_Parcels", "Parcels_selection"], "QueryTable123",
                                                    "USE_KEY_FIELDS", "",
                                                    in_field="Parcels_selection.Shape #;Account_Parcels.strap #;Account_Parcels.PARCEL_NO #",
                                                    where_clause="Account_Parcels.PARCEL_NO = Parcels_selection.PARCEL_NO")
    # END PRODUCT
    QueryTable_Final = WorkingGDB + "\\" + "QueryTable_Final"
    # Process: Copy Features
    if arcpy.Exists("QueryTable_Final"):
        arcpy.Delete_management("QueryTable_Final")
    arcpy.CopyFeatures_management(QueryTable123, QueryTable_Final, "", "0", "0", "0")
    # Process: Join Field (Buildings)
    arcpy.JoinField_management(QueryTable_Final, "Account_Parcels_strap", "Buildings", "strap")

    # Process: Join Field (Owner_Address)
    arcpy.JoinField_management(QueryTable_Final, "Account_Parcels_strap", "Owner_Address", "strap")
except:
    print("Unexpected Error: ", sys.exc_info()[0])
# # Process: Join Field (Buildings)
# arcpy.JoinField_management(QueryTable_Final, "Account_Parcels_strap", "Buildings", "strap", "bldgClass;EffectiveYear;nbrBedRoom;nbrRoomsNobath;TotalFinishedSF;UnitCount")
#
# # Process: Join Field (Land)
# arcpy.JoinField_management(QueryTable_Final, "Account_Parcels_strap", "Land", "strap", "GIS_sqft;GIS_acreage")
#
# # Process: Join Field (Owner_Address)
# arcpy.JoinField_management(QueryTable_Final, "Account_Parcels_strap", "Owner_Address", "strap", "str_num;str;str_pfx;str_sfx;sub_dscr;owner_name;mailingAddr1;mailingAddr2;mailingCity;mailingState;mailingZip;legalDscr")
#



