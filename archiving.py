import config
import os
import sys
import arcpy
import utility
import shutil
import graphing

# creates backup package of inputs and results
# need to backup:
# development capacity fc
# zone/max IA table
# unit projections (start, end year, units within that time frame) within a file
# EMGAATS.FdsBliScratch (after being filled from dev cap and formatted) - from in mem probably
# EMGAATS.FdsBli2050/2070/etc - need to be backed up manually?


new_folder_full_path = utility.fds_archive_full_path_name()

def archive_inputs_and_existing_fds():
    try:
        print("Beginning FDS Archiving - BPS inputs and existing Fds")

        # make new datetime stamped folder
        print("making archive dir")
        os.mkdir(new_folder_full_path)

        print("making BPS input dir")
        bps_input_dir = os.path.join(new_folder_full_path, "BPS_inputs")
        os.mkdir(bps_input_dir)

        print("saving unit projection graph to BPS input dir")
        graphing.graph_projections(new_folder_full_path)

        print("copying to BPS input dir")
        input_file_list = [config.metro_allocations, config.zoning_max_impa_table]
        for file in input_file_list:
            print("... {}".format(os.path.basename(file)))
            shutil.copy(file,
                        os.path.join(bps_input_dir, os.path.basename(file)))

        # print("copying zoning/ max IA table to BPS input dir")
        # shutil.copy(config.zoning_max_impa_table,
        #             os.path.join(bps_input_dir, os.path.basename(config.zoning_max_impa_table)))

        print("creating BPS_inputs.gdb")
        arcpy.management.CreateFileGDB(new_folder_full_path, "BPS_inputs.gdb")
        bps_inputs_full_gdb_path = os.path.join(new_folder_full_path, "BPS_inputs.gdb")

        # copy dev cap into new gdb
        print("copying Development Capacity fc to BPS_inputs.gdb")
        utility.copy_fc_to_gdb(bps_inputs_full_gdb_path, config.dev_capacity_fc)

        print("creating EMGAATS_existing.gdb")
        arcpy.management.CreateFileGDB(new_folder_full_path, "EMGAATS_existing.gdb")
        emgaats_existing_full_gdb_path = os.path.join(new_folder_full_path, "EMGAATS_existing.gdb")

        print("copying to EMGAATS_existing.gdb")
        input_fc_list = [config.FdsBliBO_fc,
                         config.FdsBli2050_fc,
                         config.FdsBliScratch_fc,
                         config.FdsZoneMaxIA_table]
        for obj in input_fc_list:
            name = os.path.basename(obj).split('.')[2]
            print("... {}".format(name))
            utility.copy_object_to_gdb(emgaats_existing_full_gdb_path, obj)

        print("FDS Archiving - inputs and existing Fds Complete - {}".format(new_folder_full_path))

    except Exception as e:

        print("Didn't work - deleting {}".format(new_folder_full_path))
        #utility.delete_dir_if_exists(new_folder_full_path)
        # utility.delete_file_if_exists(utility.ccsp_gdb_full_path_name() + ".zip")

        # log_obj.info("DATA COULD NOT BE LOADED".format())
        arcpy.ExecuteError()
        # log_obj.exception(str(sys.exc_info()[0]))

        print(str(sys.exc_info()[0]))


#archive_inputs_and_existing_fds() # for testing - DELETE


# only run this method after running the EMGAATS Update
# prob need to tell it which archive folder as param since this will be run asynchronously from initial archive
def archive_new_fds(archive_folder_path):

    try:
        print("Beginning FDS Archiving - new Fds")

        print("creating EMGAATS_new_result.gdb")
        arcpy.management.CreateFileGDB(archive_folder_path, "EMGAATS_new_result.gdb")
        emgaats_new_result_full_gdb_path = os.path.join(archive_folder_path, "EMGAATS_new_result.gdb")

        print("copying to EMGAATS_new_result.gdb")
        input_fc_list = [config.FdsBliBO_fc,
                         config.FdsBli2050_fc,
                         config.FdsBliScratch_fc,
                         config.FdsZoneMaxIA_table]
        for obj in input_fc_list:
            name = os.path.basename(obj).split('.')[2]
            print("... {}".format(name))
            utility.copy_object_to_gdb(emgaats_new_result_full_gdb_path, obj)

        print("FDS Archiving - new Fds Complete - {}".format(emgaats_new_result_full_gdb_path))

    except Exception as e:

        print("Didn't work - deleting {}".format(new_folder_full_path))
        #utility.delete_dir_if_exists(archive_folder_path)
        # utility.delete_file_if_exists(utility.ccsp_gdb_full_path_name() + ".zip")

        # log_obj.info("DATA COULD NOT BE LOADED".format())
        arcpy.ExecuteError()
        # log_obj.exception(str(sys.exc_info()[0]))

        print(str(sys.exc_info()[0]))


# TODO - modify this final archive piece so it is not run manually from here.
#  Forgetting to comment it out when fds_main is run means it runs at the wrong time
# folder_path = r"\\besfile1\ccsp\03_WP1_Analysis_Solution_Dev\02_Data_Framework\FutureCondition\Fds_archive\FDS_archive_2024040312"
# archive_new_fds(folder_path)