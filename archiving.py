import config
import os
import sys
import arcpy
import utility
import shutil

# creates backup package of inputs and results
# need to backup:
# development capacity fc
# zone/max IA table
# unit projections (start, end year, units within that time frame) within a file
# EMGAATS.FdsBliScratch (after being filled from dev cap and formatted) - from in mem probably
# EMGAATS.FdsBli2050/2070/etc - need to be backed up manually?

#TODO - this all needs to go into a method that can be called from fds_main

new_folder_full_path = utility.fds_archive_full_path_name()

try:
    print("Beginning FDS Archiving")

    # make new datetime stamped folder
    print("making archive dir")
    os.mkdir(new_folder_full_path)

    print("copying metro allocations")
    shutil.copy(config.metro_allocations,
                os.path.join(new_folder_full_path, os.path.basename(config.metro_allocations)))

    print("copying zoning/ max IA table")
    shutil.copy(config.zoning_max_impa_table,
                os.path.join(new_folder_full_path, os.path.basename(config.zoning_max_impa_table)))


    print("creating archive gdb")
    arcpy.management.CreateFileGDB(new_folder_full_path, utility.fds_archive_gdb_name())

    # copy dev cap into new gdb
    print("copying dev cap fc to archive gdb")
    full_fc_path = os.path.join(utility.fds_gdb_full_path_name(new_folder_full_path),
                                                               os.path.basename(config.dev_capacity_fc)
                                )
    arcpy.CopyFeatures_management(config.dev_capacity_copy, full_fc_path)

    #copy FdsBliScratch from memory after prepping

    #copy FdsBli2070 after running EMGAATS tool (??)

    #copy

    print("FDS Archiving Complete - {}".format(new_folder_full_path))

except Exception as e:

    print("Didn't work - deleting {}".format(new_folder_full_path))
    utility.delete_dir_if_exists(new_folder_full_path)
    # utility.delete_file_if_exists(utility.ccsp_gdb_full_path_name() + ".zip")

    #log_obj.info("DATA COULD NOT BE LOADED".format())
    arcpy.ExecuteError()
    #log_obj.exception(str(sys.exc_info()[0]))

    print(str(sys.exc_info()[0]))