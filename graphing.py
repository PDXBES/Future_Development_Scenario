
import matplotlib.pyplot as plt
import numpy as np
import config
import utility
import os

allocation_values = utility.get_txt_file_values(config.metro_allocations)
start_year = int(allocation_values[0])
end_year = int(allocation_values[1])
new_units = int(allocation_values[2])
max_units = utility.calc_full_capacity_units(config.dev_capacity_copy, 'NET_ALLOWC')
horizon_year = utility.calc_horizon_year(50)
new_units_per_year = utility.calc_new_units_per_year(start_year, end_year, new_units)
buildout_year = utility.calc_buildout_year(start_year, max_units, new_units_per_year)

def graph_projections(output_folder):
    # Data points
    x = np.array([start_year, end_year])
    y = np.array([0, new_units])

    # Fit a linear regression line
    coefficients = np.polyfit(x, y, 1)
    trendline = np.poly1d(coefficients)

    # Extend trendline 70 years beyond 2045
    extended_year = end_year + 70
    extended_years = np.arange(start_year, extended_year)  # 70 years beyond 2045
    extended_units = trendline(extended_years)

    # Calculate the value at 214520 units
    value_at_buildout = max_units
    # year_at_214520 = (value_at_buildout - coefficients[1]) / coefficients[0]

    # Plot the data points, trendline, and additional points
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='blue', label='BPS Projections')
    plt.plot(extended_years, extended_units, color='orange', label='Trendline')
    plt.scatter(horizon_year, trendline(horizon_year), color='red', marker='o', label='50 Year Horizon')
    plt.scatter(buildout_year, value_at_buildout, color='green', marker='o', label='Full Buildout')

    # Add labels to data points
    plt.text(x[0], y[0], f'({x[0]}, {y[0]})', ha='right', va='bottom')
    plt.text(x[1], y[1], f'({x[1]}, {y[1]})', ha='left', va='top')
    plt.text(horizon_year, trendline(horizon_year), f'({horizon_year}, {int(trendline(horizon_year))})', ha='right',
             va='bottom')
    plt.text(buildout_year, value_at_buildout, f'({int(buildout_year)}, {value_at_buildout})', ha='left', va='top')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Units')
    DDMMYYYY = utility.find_current_DDMMYYYY()
    plt.title('Unit Projections ({})'.format(DDMMYYYY))
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, "unit_projection_graph_" + DDMMYYYY.replace('/', '') + ".jpg")) # where should it really go?
    # plt.show() #this only for QC if its being written out to file

graph_projections()
