#-------------------------------------------------------------------------------
# Name:        ApplyDefQuery
# Purpose:      apply new defintion query to layer
#
# Author:      Spencer_C
#
# Created:     10/07/2024
# Copyright:   (c) Spencer_C 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#setup
import arcpy
park = ['Terra Ceia Preserve State Park']
template_file_path = r"C:\Users\Spencer_C\Desktop\StartupProject\StartupProject.aprx"
##layer_file_path = r'\\floridadep\data\DRP\GIS\LEGENDS\Layer_Files\Park Boundary.lyrx'
layer_file_path = r'\\floridadep\data\DRP\GIS\PARKS\Crystal River Archaeological State Park\Park Boundary.lyrx'

aprx = arcpy.mp.ArcGISProject(template_file_path)
maps = aprx.listMaps()

# import a layer to the project
lf = arcpy.mp.LayerFile(layer_file_path).listLayers()[0]
lf.definitionQuery("SITE_NAME = 'Joe Momma'")
dq_dict = lf.listDefinitionQueries()
print(f'{dq_dict}')
##lf.updateDefinitionQueries()
##maps[0].addLayer(lf, 'TOP')

# apply defintion query to layer

#rename layer

#save the project with the new layer
##aprx.saveACopy(f"C:\\Users\\Spencer_C\Desktop\\test_layers\\test_layers.aprx")