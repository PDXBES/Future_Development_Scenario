#-------------------------------------------------------------------------------
# Name:        future_base.py
# Purpose:
#
# Author:      DAVIDC
#
# Created:     March 15 2018
# Copyright:
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

#folders
connection_folder = r"\\besfile1\asm_projects\9ESEN0000008\EMGAATS\connections"

sde_prod = connection_folder + r"\BESDBPROD1.EMGAATS.OSA.sde"
targetFC = sde_prod + r"\EMGAATS.GIS.FdsBliScratch"
FdsZoneMaxIA = sde_prod + r"\EMGAATS.GIS.FdsZoneMaxIA"

n_missing_zones = 0
# abuildout_delta_fraction = 0.67 # per Jan 2020 extrapolation calc
abuildout_delta_fraction = 1 # use if running separately for All BO

dict_FdsZoneMaxIA ={}


def main():
    arcpy.env.overwriteOutput = True
    arcpy.env.qualifiedFieldNames = False


    arcpy.MakeTableView_management(FdsZoneMaxIA,"FdsZoneMaxIA")

    print "building dictionary"
    dict_FdsZoneMaxIA.clear
    with arcpy.da.SearchCursor("FdsZoneMaxIA", ["fds_zone", "max_impervious_percent"]) as cursor:
        for row in cursor:
            afdsZone = row[0]
            amax_impervious_percent = row[1]
            if amax_impervious_percent == None:
                amax_impervious_percent = 0
            #config.dict_Area_lookup[row[0]] = [row[1], row[2], row[3], row[2], 0, None, 0]
            dict_FdsZoneMaxIA[afdsZone] = amax_impervious_percent

    del row
    del cursor

    print "updating data"
    with arcpy.da.UpdateCursor(targetFC, ["future_area_id","fds_zone","buildout_delta_fraction", "max_impervious_percent"]) as cursor:
        afds_id = 0
        n_missing_zones = 0
        for row in cursor:
            afds_id = afds_id + 1
            afdsZone = row[1]
            if afdsZone in dict_FdsZoneMaxIA:
                amax_impervious_percent = dict_FdsZoneMaxIA[afdsZone]
            else:
                amax_impervious_percent =-1
                n_missing_zones = n_missing_zones + 1

            row[0] = afds_id
            row[2] = abuildout_delta_fraction
            row[3] = amax_impervious_percent
            cursor.updateRow(row)

    del row
    del cursor


    if n_missing_zones == 0:
        print "no missing zones were found"
    else:
        print str(n_missing_zones) + " rows with missing zones were found"

    print "done"


if __name__ == '__main__':
    main()
