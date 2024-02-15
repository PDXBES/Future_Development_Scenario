import config


def calc_new_units_per_year(new_units_start_year, new_units_end_year, new_units_count):
    units_per_year = new_units_count/ (new_units_end_year - new_units_start_year)
    return units_per_year

def calc_horizon_year_unit_count(new_units_start_year, horizon_year, units_per_year):
    horizon_year_units = units_per_year * (horizon_year - new_units_start_year)
    return horizon_year_units

#full_capacity_units = BLI Development Capacity sum of NETALLOW_C field
def calc_buildout_delta_fraction(full_capacity_units, horizon_year_units):
    buildout_delta_fraction = horizon_year_units/full_capacity_units
    return buildout_delta_fraction

