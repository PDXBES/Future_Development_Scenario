import arcpy
from datetime import datetime
import os
import sys
import config
import shutil
import logging


print("Importing utility")


def Logger(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                  datefmt='%Y/%m/%d %H:%M:%S')  # %I:%M:%S %p AM|PM format
    logging.basicConfig(filename='%s.log' % (file_name),
                        format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S', filemode='a', level=logging.INFO)
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.DEBUG)
    # log_obj = logging.getLogger().addHandler(logging.StreamHandler())

    # console printer
    screen_handler = logging.StreamHandler(stream=sys.stdout)  # stream=sys.stdout is similar to normal print
    screen_handler.setFormatter(formatter)
    logging.getLogger().addHandler(screen_handler)

    log_obj.info("Starting log session..")
    return log_obj


def calc_new_units_per_year(new_units_start_year, new_units_end_year, new_units_count):
    units_per_year = int(new_units_count)/ (int(new_units_end_year) - int(new_units_start_year))
    return units_per_year


def calc_horizon_year_unit_count(new_units_start_year, horizon_year, units_per_year):
    horizon_year_units = units_per_year * (horizon_year - new_units_start_year)
    return horizon_year_units


def calc_horizon_year(horizon_in_years):
    now_year = find_current_year()
    horizon_year = now_year + horizon_in_years
    return horizon_year


def find_current_year():
    now = datetime.now()
    now_year = now.year
    return now_year


def find_current_YYYYMMDD():
    now = datetime.now()
    YYYYMMDD = str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    return YYYYMMDD


def calc_units_at_horizon_year(horizon_in_years, new_units_per_year):
    horizon_year = calc_horizon_year(horizon_in_years)
    now_year = find_current_year()
    year_diff = horizon_year - now_year
    units_at_horizon_year = year_diff * new_units_per_year
    return units_at_horizon_year


def calc_buildout_year(start_year, full_capacity_units, new_units_per_year):
    years_to_max_units = int(full_capacity_units/ new_units_per_year)
    buildout_year = start_year + years_to_max_units
    return buildout_year


def calc_fraction(full_capacity_units, horizon_year_units):
    fraction = round(horizon_year_units/ full_capacity_units, 2)
    return fraction


#full_capacity_units = Development Capacity sum of NET_ALLOWC field (always verify)
def calc_buildout_delta_fraction():
    allocation_values = get_txt_file_values(config.metro_allocations)
    start_year = int(allocation_values[0])
    end_year = int(allocation_values[1])
    new_units = int(allocation_values[2])
    horizon_year = calc_horizon_year(config.horizon_in_years)  # using 50 year horizon as the default
    new_units_per_year = calc_new_units_per_year(start_year, end_year, new_units)
    horizon_year_units = calc_horizon_year_unit_count(start_year, horizon_year, new_units_per_year)
    full_capacity_units = calc_full_capacity_units(config.dev_capacity_copy, 'NET_ALLOWC')
    buildout_delta_fraction = calc_fraction(full_capacity_units, horizon_year_units)
    return buildout_delta_fraction


#dev_capacity_fc = config.dev_capacity_fc
#ield = 'NET_ALLOWC'
def calc_full_capacity_units(dev_capacity_fc, field):
    value_list = []
    with arcpy.da.SearchCursor(dev_capacity_fc, field) as cursor:
        for row in cursor:
            if row[0] is not None:
                value_list.append(row[0])
    full_capacity_units = int(sum(value_list))
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


def get_missing_value_list_from_field_comparison(input_fc1, field1, input_fc2, field2): # finds any values in list1 that are not in list2
    list1 = get_distinct_value_list(input_fc1, field1)
    list2 = get_distinct_value_list(input_fc2, field2)

    missing_list = []
    for value in list1:
        if value not in list2:
            missing_list.append(value)
    return missing_list


def fds_archive_folder_name():
    basename = "FDS_archive_"
    dateandtime = datetime.today().strftime('%Y%m%d%H')
    full_name = basename + dateandtime
    return full_name


def fds_archive_full_path_name():
    new_folder_full_path = os.path.join(config.archive_folder, fds_archive_folder_name())
    return new_folder_full_path


def copy_fc_to_gdb(target_gdb, source_fc):
    if ".gdb" in source_fc:
        name = os.path.basename(source_fc)
        full_fc_path = os.path.join(target_gdb,
                                    name
                                    )
    elif ".sde" in source_fc:
        name = os.path.basename(source_fc).split('.')[2]
        full_fc_path = os.path.join(target_gdb,
                                    name
                                    )
    arcpy.CopyFeatures_management(source_fc, full_fc_path)


def copy_table_to_gdb(target_gdb, source_fc):
    if ".gdb" in source_fc:
        name = os.path.basename(source_fc)
        full_fc_path = os.path.join(target_gdb,
                                    name
                                    )
    elif ".sde" in source_fc:
        name = os.path.basename(source_fc).split('.')[2]
        full_fc_path = os.path.join(target_gdb,
                                    name
                                    )
    arcpy.Copy_management(source_fc, full_fc_path)


def copy_object_to_gdb(target_gdb, source_fc):
    desc = arcpy.Describe(source_fc)
    if hasattr(desc, 'featureType'): # only feature classes have 'featureType' not tables
        copy_fc_to_gdb(target_gdb, source_fc)
    else:
        copy_table_to_gdb(target_gdb, source_fc)


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
        #print("unable to truncate, using Delete Rows")
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


def set_scratch_buildout_to_one():
    with arcpy.da.UpdateCursor(config.FdsBliScratch_fc, 'buildout_delta_fraction') as cursor:
        for row in cursor:
            row[0] = 1
            cursor.updateRow(row)





