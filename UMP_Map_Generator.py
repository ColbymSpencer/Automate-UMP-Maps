#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Spencer_C
#
# Created:     07/07/2024
# Copyright:   (c) Spencer_C 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os

#### INPUTS ####
#park name, map size
##parks_dict = {      "Caladesi Island State Park":'11X17P',
##                    "Terra Ceia Preserve State Park":'11X17P',
##                    "Judah P. Benjamin Confederate Memorial at Gamble Plantation Historic State Park":'8.5X11P',
##                    "Werner-Boyce Salt Springs State Park":'11X17P',
##                    "Hillsborough River State Park":'11X17P',
##                    "South Fork State Park":'11X17L',
##                    "Myakka River State Park":'11X17L',
##                    "Gasparilla Island State Park":'11X17P',
##                    "Paynes Creek Historic State Park":'11X17P',
##                    "Estero Bay Preserve State Park":'11X17P',
##                    "Lovers Key State Park":'11X17L',
##                    "Koreshan State Park":'11X17L'}

parks_dict = {'Judah P. Benjamin Confederate Memorial at Gamble Plantation Historic State Park':'8.5X11P'}

#map_type, layer_name in order from bottom to top of contents pane
maps_dictionary = { 'Base': ['Park Boundary', 'Park Roads', 'Trails', 'Walkways','Parking Lots','Structures','Camping Sites'],
                    'Management Zones': ['Park Boundary', 'Management Zones'],
                    'Natural Communities': ['Natural Communities','Park Boundary'],
                    'Optimum Boundary': ['Park Boundary', 'Optimum Boundary'],
                    'Soils': ['Soils']}
template_file_path = r"\\floridadep\data\DRP\GIS\Codes and Scripts\Python3x\UMP_Automation_Testing\project_template.aprx"
park_folder = "\\\\floridadep\\data\\drp\\gis\\parks\\"

for park,dims in parks_dict.items():

    # make directory for new UMP projects in each park's folder
    try:
        os.mkdir(f'{park_folder}{park}\\Projects\\UMP\\UMP_2024')
        print(f'directory created at {park_folder}{park}\\Projects\\UMP\\UMP_2024')
    except:
        print(f'\nERROR making directory at {park_folder}{park}\\Projects\\UMP\\UMP_2024 \n')

    for map_type, layer_list in maps_dictionary.items():

        #referesh the project
        aprx = arcpy.mp.ArcGISProject(r'C:\Users\Spencer_C\Desktop\Local_Copy\Example_Project.aprx')
        aprx.save()
        aprx = arcpy.mp.ArcGISProject(template_file_path)

        #import layer file and declare map to work in
        aprx.importDocument(f'\\\\floridadep\\data\\DRP\\GIS\\STANDARDS\\Templates\\UMP\\{dims}\\{map_type} Map {dims}.pagx') #add appropriate layout file to project
        maps = aprx.listMaps(f'{map_type} Map Frame')
##        maps[0].name = f'{map_type} Map Frame' #rename the map in the template project
        for layer_name in layer_list:
            try:
                lf = arcpy.mp.LayerFile(f'\\\\floridadep\\data\\drp\\gis\\legends\\Layer_Files\\{layer_name}.lyrx').listLayers()[0]
                lf.definitionQuery = f"SITE_NAME = '{park}'"
                lf.name = f'{layer_name}'
                print(f'{map_type}\t{layer_name} layer created for \t{park}')
                maps[0].addLayer(lf, 'TOP')

            except:
                print(f'\nERROR {park}\t{map_type} Map\t{layer_name}\n')

##        try:
##            aprx.importDocument(f'\\\\floridadep\\data\\DRP\\GIS\\STANDARDS\\Templates\\UMP\\{dims}\\{map_type} Map {dims}.pagx') #add appropriate layout file to project
##        except:
##            print('\nERROR issue adding layout file\n')
        aprx.saveACopy(f"{park_folder}{park}\\Projects\\UMP\\UMP_2024\\{map_type} {dims}.aprx") #save a copy of the project to the directory created earlier
        print(f'{park} {map_type} map created\n')

##        # remove all layers except satelite imagery from map
##        for lf_object in maps[0].listLayers():
##            if lf_object.name != 'World Imagery':
##                try:
##                    maps[0].removeLayer(lf_object)
##                except:
##                    print(f'\nERROR removing {lf_object.name} from {park}\'s {map_type} map\n')


