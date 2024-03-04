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


def archive_inputs_and_existing_fds():
    try:
        print("Beginning FDS Archiving - inputs and existing Fds")

        # make new datetime stamped folder
        print("making archive dir")
        os.mkdir(new_folder_full_path)

        print("making BPS input dir")
        bps_input_dir = os.path.join(new_folder_full_path, "BPS_inputs")
        os.mkdir(bps_input_dir)

        print("copying metro allocations to BPS input dir")
        shutil.copy(config.metro_allocations,
                    os.path.join(bps_input_dir, os.path.basename(config.metro_allocations)))

        print("copying zoning/ max IA table to BPS input dir")
        shutil.copy(config.zoning_max_impa_table,
                    os.path.join(bps_input_dir, os.path.basename(config.zoning_max_impa_table)))

        print("creating BPS inputs gdb")
        arcpy.management.CreateFileGDB(new_folder_full_path, "BPS_inputs.gdb")
        bps_inputs_full_gdb_path = os.path.join(new_folder_full_path, "BPS_inputs.gdb")

        # copy dev cap into new gdb
        print("copying dev cap fc to BPS inputs gdb")
        # full_fc_path = os.path.join(bps_inputs_full_gdb_path,
        #                             os.path.basename(config.dev_capacity_fc)
        #                             )
        # arcpy.CopyFeatures_management(config.dev_capacity_copy, full_fc_path)
        
        utility.copy_fc_to_gdb(bps_inputs_full_gdb_path, config.dev_capacity_fc)

        print("creating EMGAATS existing gdb")
        arcpy.management.CreateFileGDB(new_folder_full_path, "EMGAATS_existing.gdb")
        emgaats_existing_full_gdb_path = os.path.join(new_folder_full_path, "EMGAATS_existing.gdb")

        print("copying existing scenarios and zoningIA to EMGAATS existing gdb")
        # full_fc_path = os.path.join(emgaats_existing_full_gdb_path,
        #                             os.path.basename(config.FdsBli2050)
        #                             )
        # arcpy.CopyFeatures_management(config.FdsBli2050, full_fc_path)

        utility.copy_fc_to_gdb(emgaats_existing_full_gdb_path, config.FdsBli2050)

        print("FDS Archiving - inputs and existing Fds Complete - {}".format(new_folder_full_path))

    except Exception as e:

        print("Didn't work - deleting {}".format(new_folder_full_path))
        utility.delete_dir_if_exists(new_folder_full_path)
        # utility.delete_file_if_exists(utility.ccsp_gdb_full_path_name() + ".zip")

        # log_obj.info("DATA COULD NOT BE LOADED".format())
        arcpy.ExecuteError()
        # log_obj.exception(str(sys.exc_info()[0]))

        print(str(sys.exc_info()[0]))


archive_inputs_and_existing_fds()

try:
    print("Beginning FDS Archiving - new Fds")

    # copy FdsBliScratch from memory after prepping

    # copy FdsBli2070 after running EMGAATS tool (??)

    except Exception as e:

        print("Didn't work - deleting {}".format(new_folder_full_path))
        utility.delete_dir_if_exists(new_folder_full_path)
        # utility.delete_file_if_exists(utility.ccsp_gdb_full_path_name() + ".zip")

        # log_obj.info("DATA COULD NOT BE LOADED".format())
        arcpy.ExecuteError()
        # log_obj.exception(str(sys.exc_info()[0]))

        print(str(sys.exc_info()[0]))