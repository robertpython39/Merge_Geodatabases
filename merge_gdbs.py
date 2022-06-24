#-------------------------------------------------------------------------------
# Name:        merge_gdb's
# Purpose:
#
# Author:      rnicolescu
#
# Created:     17/05/2022
# Copyright:   (c) rnicolescu 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from arcpy import env
import arcpy
import os
import glob

print "Arcpy loading. Please wait..."
destination_folder = r"C:\test\merged_gdbs"
print "Creating destination folder. Please wait..."

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

print "Processing files..."

def copy_gdb(gdb1):
    env.workspace = gdb1
    env.overwriteOutput = True
    global destination_folder
    arcpy.Copy_management(gdb1, destination_folder + "\\merge_gdb.gdb")
    print "Temp GDB succesfully created..."

print "Merge process started. Please wait..."
def merge_gdbs(gdb1, gdb2):
    arcpy.env.workspace = gdb1
    fc_list1 = arcpy.ListFeatureClasses(feature_dataset='ThematicData')
    d1 = {}
    for fc in fc_list1:
        i = 0
        with arcpy.da.SearchCursor(fc, ["SHAPE"]) as cursor:
            for elem in cursor:
                i = 1
                break
        if i == 1:
            d1[fc] = ""

    arcpy.env.workspace = gdb2
    fc_list2 = arcpy.ListFeatureClasses(feature_dataset='ThematicData')
    d2 = {}
    for fc in fc_list2:
        i = 0
        with arcpy.da.SearchCursor(fc, ["SHAPE"]) as cursor:
            for elem in cursor:
                i = 1
                break
        if i == 1:
            d2[fc] = ""
    print "Feature populated in gdb1: " + str(d1)
    print "Feature populated in gdb1: " + str(d2)

    for key in d2:
        cale1 = os.path.join(gdb1, "ThematicData", key)
        cale2 = os.path.join(gdb2, "ThematicData", key)
        temp = os.path.join(gdb1, 'ThematicData', "temp")

        if key in d1:
            print "Now merging... " + key
            arcpy.Merge_management([cale1, cale2], temp)
            cale3 = temp
        else:
            print "Now copying... " + key
            cale3 = cale2
        rows1 = arcpy.InsertCursor(cale1)
        rows2 = arcpy.SearchCursor(cale3)
        for row in rows2:
            rows1.insertRow(row)
        del row
        del rows1
        del rows2
        if cale3 == temp:
            arcpy.Delete_management(temp)

if __name__ == "__main__":
    gdb1_path = raw_input(r"Enter path for the first gdb:")
    gdb2_path = raw_input(r"Enter path for the second gdb:")
    copy_gdb(gdb1_path)
    merge_gdbs(gdb1_path, gdb2_path)
    print "Script done. Press ENTER to exit..."
    exit = raw_input("")
