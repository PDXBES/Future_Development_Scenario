import os
import arcpy

print("Importing config")

sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"

EMGAATS_PROD1_sde = "BESDBPROD1.EMGAATS.sde"
EMGAATS_PROD1_sde_path = os.path.join(sde_connections, EMGAATS_PROD1_sde)

FdsBliScratch_fc = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsBliScratch"
FdsZoneMaxIA_table = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsZoneMaxIA"
FdsBliBO_fc = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsBliBO"
FdsBli2050_fc = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsBli2050"
# use of FdsBli2050, FdsAllBO, FdsRip2050, FdsRipBO have all been deprecated as of 2024
EMGAATS_Areas = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.Areas"

archive_folder = r"\\besfile1\ccsp\03_WP1_Analysis_Solution_Dev\02_Data_Framework\FutureCondition\Fds_archive"
log_folder = r"\\besfile1\ccsp\03_WP1_Analysis_Solution_Dev\02_Data_Framework\FutureCondition\logging"

# BPS data
BPS_sources_base_folder = r"\\besfile1\ccsp\03_WP1_Analysis_Solution_Dev\02_Data_Framework\FutureCondition\from_BPS"

# ------ THESE ARE YOUR VARIABLES --------------------------------------------------------------------

#  --- testing inputs ---------------
# current_sources_folder = os.path.join(BPS_sources_base_folder, "data_received_April_2023")
# dev_capacity_fc = os.path.join(current_sources_folder, r"BLI_output_230414.gdb\BLI_output_30ratio_230411")
# zoning_max_impa_table = os.path.join(current_sources_folder, r"zoning_max_impa.csv")
# metro_allocations = os.path.join(current_sources_folder, r"metro_allocation.txt")
#  --- testing inputs ---------------

current_sources_folder = os.path.join(BPS_sources_base_folder, "current_inputs")
dev_capacity_fc = os.path.join(current_sources_folder, r"BLI_output_240328.gdb\BLI_output_240328")
zoning_max_impa_table = os.path.join(current_sources_folder, r"zoning_max_impa.csv")
metro_allocations = os.path.join(current_sources_folder, r"metro_allocation.txt")

horizon_in_years = 50

# -----------------------------------------------------------------------------------------------------

infiltration_areas = r"\\besfile1\asm_projects\9ESEN0000008\EMGAATS\FutureBase\gis\spatial\SWMM_Effectiveness_copy_20240220.gdb\SWMM_Regions"

# getting inputs into memory
# OLD QUERY
#dev_capacity_fl = arcpy.MakeFeatureLayer_management(dev_capacity_fc, r"in_memory\dev_capacity_fl", "NET_ALLOW > 0 OR EMP_SQFT > 0")

dev_capacity_fl = arcpy.MakeFeatureLayer_management(dev_capacity_fc, r"in_memory\dev_capacity_fl", "underutilized = 1")
dev_capacity_copy = arcpy.CopyFeatures_management(dev_capacity_fl, r"in_memory\dev_capacity_copy")

FdsBliScratch_copy = arcpy.CopyFeatures_management(FdsBliScratch_fc, r"in_memory\FdsBliScratch_copy")
EMGAATS_Areas_copy = arcpy.CopyFeatures_management(EMGAATS_Areas, r"in_memory\EMGAATS_Areas_copy")
