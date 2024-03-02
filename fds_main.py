
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

    missing_values = utility.get_missing_value_list(config.dev_capacity_copy, config.FdsZoneMaxIA_table) # or point direct to config.zoning_max_impa_table
    if len(missing_values) == 0:

        # append Dev Cap to Scratch copy - field map ZONE to fds_zone
        dev_cap_zone_field = 'fds_zone'
        scratch_zone_field = 'ZONE'
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


        # populate destination_node_id, existing_area_sqft? - also done in EMGAATS update button



        # populate additional_area_sqft - calcs from above fields
        # --- calc shape_area since in memory doesn't automatically have it -- maybe?? VERIFY
        arcpy.CalculateGeometryAttributes_management(config.FdsBliScratch_copy, )
        utility.calc_additional_area_sqft(config.FdsBliScratch_copy)

        # populate infiltration_fraction - based on intersect with SWMM source
        fds_scratch_points = arcpy.management.FeatureToPoint(config.FdsBliScratch_copy, r"in_memory\fds_scratch_points")
        sect = arcpy.Intersect_analysis([fds_scratch_points, config.infiltration_areas], r"in_memory\sect", '', '', 'POINT')
        utility.get_and_assign_field_value(sect,
                                           'future_area_id', #populated above
                                           'Effectiveness',
                                           config.FdsBliScratch_copy,
                                           'future_area_id',
                                           'Infiltration_fraction')


        # populate modeled_area_sqft - based on additional and infiltration fraction (so goes last)


        # archive package


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