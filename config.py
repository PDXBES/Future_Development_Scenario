import os
import arcpy

sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"

EMGAATS_PROD1_sde = "BESDBPROD1.EMGAATS.sde"
EMGAATS_PROD1_sde_path = os.path.join(sde_connections, EMGAATS_PROD1_sde)

FdsBliScratch_fc = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsBliBO"
FdsZoneMaxIA_table = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsZoneMaxIA"
FdsBliBO_fc = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsBliBO"
# use of FdsBli2050, FdsAllBO, FdsRip2050, FdsRipBO have all been deprecated as of 2024

archive_folder = r"\\besfile1\ccsp\03_WP1_Analysis_Solution_Dev\02_Data_Framework\FutureCondition\Fds_archive"
log_folder = r"\\besfile1\ccsp\03_WP1_Analysis_Solution_Dev\02_Data_Framework\FutureCondition\logging"

# read these from allocation file
#new_units_start_year = None
#new_units_end_year = None
#new_units_count = None

# placeholder inputs
BPS_sources_base_folder = r"\\besfile1\ccsp\03_WP1_Analysis_Solution_Dev\02_Data_Framework\FutureCondition\from_BPS"
current_sources_folder = os.path.join(BPS_sources_base_folder, "data_received_April_2023")

dev_capacity_fc = os.path.join(current_sources_folder, r"BLI_output_230414.gdb\BLI_output_30ratio_230411")
zoning_max_impa_table = os.path.join(current_sources_folder, r"zoning_max_impa.csv")
metro_allocations = os.path.join(current_sources_folder, r"metro_allocation.txt")

dev_capacity_fl = arcpy.MakeFeatureLayer_management(dev_capacity_fc, r"in_memory\dev_capacity_fl", "NET_ALLOW > 0 OR EMP_SQFT > 0")
dev_capacity_copy = arcpy.CopyFeatures_management(dev_capacity_fl, r"in_memory\dev_capacity_copy")

