
import matplotlib.pyplot as plt
import numpy as np
import config
import utility

allocation_values = utility.get_txt_file_values(config.metro_allocations)
start_year = int(allocation_values[0])
end_year = int(allocation_values[1])
new_units = int(allocation_values[2])
max_units = utility.calc_full_capacity_units(config.dev_capacity_copy, 'NET_ALLOWC')
horizon_year = utility.calc_horizon_year(50)
new_units_per_year = utility.calc_new_units_per_year(start_year, end_year, new_units)
buildout_year = utility.calc_buildout_year(max_units, new_units_per_year)

def graph_projections():
    # Your existing data points
    x = np.array([start_year, end_year])  # from variables
    y = np.array([0, max_units])  # from variables

    # Create the scatter plot
    plt.scatter(x, y)

    # Fit a linear trendline
    z_linear = np.polyfit(x, y, 1)
    p_linear = np.poly1d(z_linear)
    # Plot the trendline
    plt.plot(x, p_linear(x), color="blue", label="Linear Trendline")

    # Extend the trendline
    x_extended = np.linspace(min(x), max(x) + 70, 100)  # Extend by 70 years
    plt.plot(x_extended, p_linear(x_extended), color="blue", label="Linear Trendline")

    # Calculate intersection points
    y_intersection_horizon = p_linear(horizon_year)  # use horizon year variable
    y_intersection_buildout = p_linear(buildout_year)  # use buildout year variable
    # Label the intersection points
    plt.scatter(horizon_year, y_intersection_horizon, color="red", label="Intersection Point (2080)")
    plt.scatter(buildout_year, y_intersection_buildout, color="red", label="Intersection Point (2100)")

    # Annotate each point
    plt.annotate(f'({x[0]}, {y[0]})', xy=(x[0], y[0]), xytext=(30, 0), textcoords='offset points', fontsize=8)
    plt.annotate(f'({x[1]}, {y[1]})', xy=(x[1], y[1]), xytext=(30, 0), textcoords='offset points', fontsize=8)
    # Annotate the intersection points
    plt.annotate(f'({horizon_year}, {y_intersection_horizon:.0f})', xy=(horizon_year, y_intersection_horizon), xytext=(30, 0),
                 textcoords='offset points', fontsize=8)  # again use horizon year variable
    plt.annotate(f'({buildout_year}, {y_intersection_buildout:.0f})', xy=(buildout_year, y_intersection_buildout), xytext=(30, 0),
                 textcoords='offset points', fontsize=8)  # again use buildout year variable
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.title("Population Trend")
    plt.grid()
    plt.show() # show only really needed for QC since we'll export it
    # TODO - export graph to jpg

graph_projections()
