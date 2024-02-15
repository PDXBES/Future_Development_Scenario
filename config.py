import os

sde_connections = r"\\besfile1\CCSP\03_WP2_Planning_Support_Tools\03_RRAD\CCSP_Data_Management_ToolBox\connection_files"

EMGAATS_PROD1_sde = "BESDBPROD1.EMGAATS.sde"
EMGAATS_PROD1_sde_path = os.path.join(sde_connections, EMGAATS_PROD1_sde)

FdsZoneMaxIA_table = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsZoneMaxIA"
FdsBliBO_fc = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsBliBO"
FdsBliScratch_fc = EMGAATS_PROD1_sde_path + r"\EMGAATS.GIS.FdsBliBO"

new_units_start_year = None
new_units_end_year = None
new_units_count = None