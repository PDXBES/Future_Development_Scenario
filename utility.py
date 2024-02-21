import arcpy
from datetime import datetime
import os
import config
import shutil


def calc_new_units_per_year(new_units_start_year, new_units_end_year, new_units_count):
    units_per_year = new_units_count/ (new_units_end_year - new_units_start_year)
    return units_per_year


def calc_horizon_year_unit_count(new_units_start_year, horizon_year, units_per_year):
    horizon_year_units = units_per_year * (horizon_year - new_units_start_year)
    return horizon_year_units


def calc_horizon_year(horizon_in_years):
    now = datetime.now()
    now_year = now.year
    horizon_year = now_year + horizon_in_years
    return horizon_year


#full_capacity_units = Development Capacity sum of NETALLOW_C field
def calc_buildout_delta_fraction(allocation_txt_file, horizon_in_years, dev_cap_source, capacity_field):
    allocation_values = get_txt_file_values(config.metro_allocations)
    start_year = int(allocation_values[0])
    end_year = int(allocation_values[1])
    new_units = int(allocation_values[2])
    horizon_year = calc_horizon_year(config.horizon_in_years)  # using 50 year horizon
    new_units_per_year = calc_new_units_per_year(start_year, end_year, new_units)
    horizon_year_units = calc_horizon_year_unit_count(start_year, horizon_year, new_units_per_year)
    full_capacity_units = calc_full_capacity_units(config.dev_capacity_copy, 'NETALLOW_C')
    buildout_delta_fraction = calc_buildout_delta_fraction(full_capacity_units, horizon_year_units)
    return buildout_delta_fraction


#dev_capacity_fc = config.dev_capacity_fc
#ield = 'NETALLOW_C'
def calc_full_capacity_units(dev_capacity_fc, field):
    value_list = []
    with arcpy.da.SearchCursor(dev_capacity_fc, field) as cursor:
        for row in cursor:
            value_list.append(row[0])
    full_capacity_units = sum(value_list)
    return full_capacity_units




#TODO - create method to test if config.dev_capacity.ZONE (for now, can change)
# is synced to FdsZoneMaxIA.fds_zone (or directly test against source table?) - if not then bail and message with list of mismatched

def get_distinct_value_list(input_fc, field):
    value_list = []
    with arcpy.da.SearchCursor(input_fc, field) as cursor:
        for row in cursor:
            value_list.append(row[0])
    value_set = set(value_list)
    return value_set


def get_missing_value_list(list1, list2): # finds any values in list1 that are not in list2
    missing_list = []
    for value in list1:
        if value not in list2:
            missing_list.append(value)
    # if len(missing_list) > 0:
    #     print("there are {} values in list 1 that were not found in list 2".format(len(missing_list)))
    # else:
    #     print("all values in list 1 were found in list 2")
    return missing_list

#TODO - add test for max IA value - ensure there is a value for each zone code in BPS list


def fds_archive_folder_name():
    basename = "FDS_archive_"
    dateandtime = datetime.today().strftime('%Y%m%d%H%M%S')
    full_name = basename + dateandtime
    return full_name


def fds_archive_full_path_name():
    new_folder_full_path = os.path.join(config.archive_folder, fds_archive_folder_name())
    return new_folder_full_path


def fds_archive_gdb_name():
    basename = "FDS_archive"
    #datetime = self.datetime_now()
    extension = ".gdb"
    full_name = basename + extension
    return full_name


def fds_gdb_full_path_name(fds_archive_full_path_name):
    full_name = fds_archive_gdb_name()
    full_path = os.path.join(fds_archive_full_path_name, full_name)
    return full_path


def get_txt_file_values(txt_file):
    reader = open(txt_file, "r")
    readlines = reader.readlines()
    values_list = []
    for line in readlines:
        values_list.append(line.strip('\n'))
    return values_list


def delete_dir_if_exists(input):
    if os.path.isdir(input):
        shutil.rmtree(input)
    else:
        pass


def get_field_value_as_dict(input, key_field, value_field):
    value_dict = {}
    with arcpy.da.SearchCursor(input, (key_field, value_field)) as cursor:
        for row in cursor:
            value_dict[row[0]] = row[1]
    #print(value_dict)
    return value_dict


def assign_field_value_from_dict(input_dict, target, target_key_field, target_field):
    with arcpy.da.UpdateCursor(target, (target_key_field, target_field)) as cursor:
        for row in cursor:
            if row[0] in input_dict.keys() and row[1] is None:
                row[1] = input_dict[row[0]]
            cursor.updateRow(row)


def get_and_assign_field_value(source, source_key_field, source_field, target, target_key_field, target_field):
    value_dict = get_field_value_as_dict(source, source_key_field, source_field)
    assign_field_value_from_dict(value_dict, target, target_key_field, target_field)


def cleanup(feature_class):
    try:
        arcpy.TruncateTable_management(feature_class)
    except:
        print("unable to truncate, using Delete Rows")
        arcpy.DeleteRows_management(feature_class)


def calc_additional_area_sqft(target):
    with arcpy.da.UpdateCursor(target, ['additional_area_sqft',
                                        'max_impervious_sqft',
                                        'existing_area_sqft',
                                        'buildout_delta_fraction',
                                        'Shape_Area']) as cursor:
        for row in cursor:
            row[0] = (row[1]/100) * row[4] - row[2] * row[3]
            cursor.updateRow(row)






