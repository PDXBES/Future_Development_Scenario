
# conditional - test if spreadsheet zones and dev cap zones are comparable
# if no, stop and warn (get list of mismatched - maybe even write out to file) - will need to either go to BPS or manually BES fix
# if yes, continue
# get empty FdsBLiSCratch table in mem (config.FdsBliScratch_copy)
# append Dev cap fc to that table - map field appropriately
# run pieces in Dave's future_base to update Scratch values (incorporated into fds_main)
# truncate (delete all rows) from target (Intermediate, BO) and then append Scratch values to that
# ----- BO gets full buildout value of 1
# Update Future Areas (EMGAATS toolbar tool) updates additional fields in 2070/BO
# ----- keep this as run manual or incorporate into overall script (or have both)?
# ----- modelers do prob always want to have this bc the model itself changing can create need for update
# archive all inputs and the outputs (Just the Intermediate/ BO now)

# TODO - convert print statements to logging

import arcpy
import config
import utility
import archiving

try:
    print("Starting FDS data prep")
    list1 = utility.get_distinct_value_list(config.dev_capacity_copy, 'ZONE')
    list2 = utility.get_distinct_value_list(config.FdsZoneMaxIA_table, 'fds_zone')
    missing_values = utility.get_missing_value_list_from_field_comparison(config.dev_capacity_copy, 'ZONE', config.FdsZoneMaxIA_table, 'fds_zone')
    if len(missing_values) == 0:

        # run step 1 of archive (copy Scratch, Intermediate and BO Fds, maxZoneIA tables
        # generate unit projection graph jpg - save in main archive folder
        print("Starting Initial Archiving")
        archiving.archive_inputs_and_existing_fds()

        # append formatted maxZoneIA table from csv to table in EMGAATS (after truncating it)
        # TODO - format zone/maxIA table? needs zone code parsed out, use max bldg if no max impa value, assign hard coded values (eg OS)
        # TODO - thing is they may give us a different table with a different format each time
        #  - leave as manual format for now unless we can guarantee format

        # append Dev Cap to Scratch copy - field map ZONE to fds_zone
        dev_cap_zone_field = 'fds_zone'
        scratch_zone_field = 'ZONE' # be careful - field subject to change
        dev_capacity_source = config.dev_capacity_copy

        print("Truncating Scratch fc then appending new Development Capacity to Scratch")
        # delete all rows from Scratch
        utility.cleanup(config.FdsBliScratch_fc)
        arcpy.Append_management(inputs=dev_capacity_source,
                                target=config.FdsBliScratch_fc,
                                schema_type="NO_TEST",
                                field_mapping='{} "{}" true true false 12 Text 0 0 ,First,#,{},{},-1,-1'.format(dev_cap_zone_field,
                                                                                                                dev_cap_zone_field,
                                                                                                                dev_capacity_source,
                                                                                                                scratch_zone_field)
                                ,
                                )

        print("Getting Zone/IA values")
        dict_FdsZoneMaxIA = utility.get_field_value_as_dict(config.FdsZoneMaxIA_table, 'fds_zone', 'max_impervious_percent')
        print("Getting buildout delta fraction")
        buildout_delta_fraction = utility.calc_buildout_delta_fraction()
        print("Buildout delta fraction for this run is {}".format(str(buildout_delta_fraction)))

        print("Populating future_area_id, buildout_delta_fraction and max_impervious_percent fields in Scratch fc")
        with arcpy.da.UpdateCursor(config.FdsBliScratch_fc, ["future_area_id",
                                                               "fds_zone",
                                                               "buildout_delta_fraction",
                                                               "max_impervious_percent"]) as cursor:
            afds_id = 0
            #n_missing_zones = 0
            for row in cursor:
                afds_id = afds_id + 1
                afdsZone = row[1]
                if afdsZone in dict_FdsZoneMaxIA:
                    amax_impervious_percent = dict_FdsZoneMaxIA[afdsZone]
                else:
                    amax_impervious_percent = -1
                    n_missing_zones = n_missing_zones + 1

                row[0] = afds_id
                row[2] = buildout_delta_fraction
                row[3] = amax_impervious_percent
                cursor.updateRow(row)

        print("Truncating Intermediate fc then appending Scratch")
        utility.cleanup(config.FdsBli2050_fc)
        arcpy.Append_management(inputs=config.FdsBliScratch_fc,
                                target=config.FdsBli2050_fc,
                                schema_type="NO_TEST")

        print("Truncating BO fc, setting buildout value to 1 then appending Scratch")
        utility.cleanup(config.FdsBliBO_fc)
        utility.set_scratch_buildout_to_one()
        arcpy.Append_management(inputs=config.FdsBliScratch_fc,
                                target=config.FdsBliBO_fc,
                                schema_type="NO_TEST")

        print("FDS data prep complete - ready for EMGAATS Update button to update future scenarios")


    else:
        arcpy.AddError("No data will be prepared")
        arcpy.AddError("Matched zoning codes are required")
        arcpy.AddMessage("These entries are in the Development Capacity list but NOT IN the zoning/ IA list: " + str(missing_values))
        arcpy.ExecuteError()

except Exception as e:

    #utility.delete_dir_if_exists(data_load.now_gdb_full_path_name)
    #utility.delete_file_if_exists(utility.ccsp_gdb_full_path_name() + ".zip")

    #log_obj.info("DATA COULD NOT BE LOADED".format())
    arcpy.ExecuteError()
    #log_obj.exception(str(sys.exc_info()[0]))