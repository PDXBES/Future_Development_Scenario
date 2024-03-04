
# conditional - test if spreadsheet zones and dev cap zones are comparable
# if no, stop and warn (get list of mismatched - maybe even write out to file) - will need to either go to BPS or manually BES fix
# if yes, continue
# get empty FdsBLiSCratch table in mem - got it = config.FdsBliScratch_copy
# append Dev cap fc to that table - map field appropriately
# run pieces in Dave's future_base to update SCratch values
# truncate (delete all rows) target (2050, rename to 2070?, or is it just the BO now bc that is 2070?) and then append Scratch values to that
# Update Future Areas (EMGAATS toolbar tool) updates additional fields in 2070/BO
# -----keep this as run manual or incorporate into overall script (or have both)?
# -----modelers do prob always want to have this bc the model itself changing can create need for update
# archive all inputs and the outputs (I think just the 2070/ BO now)


import arcpy
import config
import utility

try:

    #TODO - format zone/maxIA table? needs zone code parsed out, use max bldg if no max impa value, assign hard coded values (eg OS)
    # the thing is they may give us a different table with a different format each time - leave for now unless we can gaurantee format

    missing_values = utility.get_missing_value_list(config.dev_capacity_copy, config.FdsZoneMaxIA_table) # or point direct to config.zoning_max_impa_table
    if len(missing_values) == 0:

        # run step 1 of archive (copy Scratch, Intermediate and BO Fds, maxZoneIA tables

        # append Dev Cap to Scratch copy - field map ZONE to fds_zone
        dev_cap_zone_field = 'fds_zone'
        scratch_zone_field = 'ZONE' # be careful - field subject to change
        dev_capacity_source = config.dev_capacity_copy
        arcpy.Append_management(inputs=dev_capacity_source,
                                target=config.FdsBliScratch_copy,
                                schema_type="NO_TEST",
                                field_mapping='{} "{}" true true false 12 Text 0 0 ,First,#,{},{},-1,-1'.format(dev_cap_zone_field,
                                                                                                                dev_cap_zone_field,
                                                                                                                dev_capacity_source,
                                                                                                                scratch_zone_field)
                                ,
                                )

        # populate future_areas_id, buildout_delta_fraction, max_imp % - get from future_base
        # --- pull buildout delta fraction from config.metro_allocations + methods

        dict_FdsZoneMaxIA = utility.get_field_value_as_dict(config.FdsZoneMaxIA_table, 'fds_zone', 'max_impervious_percent')

        buildout_delta_fraction = utility.calc_buildout_delta_fraction()

        with arcpy.da.UpdateCursor(config.FdsBliScratch_copy, ["future_area_id",
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


        # truncate/ delete rows from Intermediate Fds then append Scratch to that Fds (currently 2050, may want name change)

        # truncate/ delete rows from BO Fds. Set Scracth buildout_delta_fraction to 1, then append Scratch to BO

        # run step 2 and 3 of archive - Dev Cap fc, metro allocations file, Scratch, Intermediate, BO Fds and maxZoneIA tables (all after refresh)


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