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

#full_capacity_units = BLI Development Capacity sum of NETALLOW_C field
def calc_buildout_delta_fraction(full_capacity_units, horizon_year_units):
    float_full_capacity_units = full_capacity_units * 1.0 #ensures a float result
    buildout_delta_fraction = round(horizon_year_units/float_full_capacity_units, 2)
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

#TODO - create method to test if config.dev_capacity.ZONE (for now, can change) is synced to FdsZoneMaxIA.fds_zone - if not then bail and message
# provide list of zones that are not synced?

def get_distinct_value_list(input_fc, field):
    value_list = []
    with arcpy.da.SearchCursor(input_fc, field) as cursor:
        for row in cursor:
            value_list.append(row[0])
    value_set = set(value_list)
    return value_set

def missing_value_tester(list1, list2): # finds any values in list1 that are not in list2
    missing_list = []
    for value in list1:
        if value not in list2:
            missing_list.append(value)
    if len(missing_list) > 0:
        print("there are {} values in list 1 that were not found in list 2".format(len(missing_list)))
    else:
        print("all values in list 1 were found in list 2")
    return missing_list

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

def get_cred_values(cred_file):
    reader = open(cred_file, "r")
    readlines = reader.readlines()
    creds = []
    for line in readlines:
        creds.append(line.strip('\n'))
    return creds

def delete_dir_if_exists(input):
    if os.path.isdir(input):
        shutil.rmtree(input)
    else:
        pass