'''
Name:        UMP Tools
Purpose:      ump tools to make the process of working in a UMP easier. There
                is terrible latency when working on/ interacting with the
                network. It is easier to work on a local copy then export to the
                network

Author:      Spencer_C
Created:     18/06/2025
Copyright:   (c) Spencer_C 2025
Licence:     <your licence>
'''

def get_site_name_from_park_boundary():
    """
    Returns the 'site_name' attribute(s) of selected features in the
    'Park Boundary' layer of the current map in ArcGIS Pro.

    Returns:
        list: A list of 'site_name' values from the selected features.
    """
    site_names = []

    # Access the current ArcGIS Pro project and the active map
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    active_map = aprx.activeMap

    # Attempt to get the 'Park Boundary' layer
    park_layer = None
    for lyr in active_map.listLayers():
        if lyr.name.lower() == "park boundary" and lyr.supports("SELECTION") and not lyr.isGroupLayer:
            park_layer = lyr
            break

    if not park_layer:
        print("Layer 'Park Boundary' not found or not valid.")
        return site_names

    # Check for 'site_name' field
    fields = [f.name.lower() for f in arcpy.ListFields(park_layer)]
    if "site_name" not in fields:
        print("Field 'site_name' not found in 'Park Boundary' layer.")
        return site_names

    # Get selected feature IDs
    selected_oids = park_layer.getSelectionSet()
    if not selected_oids:
        print("No features selected in 'Park Boundary' layer.")
        return site_names

    # Use SearchCursor to fetch 'site_name' values
    with arcpy.da.SearchCursor(park_layer, ["site_name"], where_clause=f"OBJECTID IN ({','.join(map(str, selected_oids))})") as cursor:
        for row in cursor:
            site_names.append(row[0])

    return site_names

def apply_site_name_query(site_name_value,
                          aprx = arcpy.mp.ArcGISProject("CURRENT"),
                          map_name = None):
    """
    Applies a definition query to all layers in the given map object
    where the layer has a 'site_name' field. The query filters the layer
    to only include features where site_name equals the input string.

    Parameters:
        map_name (str): The map name containing layers.
        site_name_value (str): The site name value to filter by.
        aprx (project object): The project to look for the map in. The default value is the current project.
    """
    # Get name of active map
    if not map_name:
        map_name = aprx.activeMap.name

    # Get map object using the map name
    try:
        map_obj = aprx.listMaps(map_name)[0]
    except Exception as e:
        print(f"Could not find {map_name}: {e}")

    # Apply definition queries to all appropriate layers in the map
    for lyr in map_obj.listLayers():
        if lyr.supports("DEFINITIONQUERY") and lyr.supports("DATASOURCE") and not lyr.isGroupLayer:
            try:
                # Check if 'site_name' field exists
                desc = arcpy.Describe(lyr)
                fields = [f.name.lower() for f in arcpy.ListFields(lyr)]
                if 'site_name' in fields:
                    # Apply definition query
                    dql = lyr.listDefinitionQueries()
                    for dq in dql:
                        dq['isActive'] = False
                    lyr.updateDefinitionQueries([{'name': 'Site Name Query', 'sql': f"site_name = '{site_name_value}'", 'isActive': True}])
                    #print(f"Applied query to {lyr.name}: {query}")
            except Exception as e:
                print(f"Could not apply query to {lyr.name}: {e}")

def remove_queries(aprx = arcpy.mp.ArcGISProject("CURRENT"),
                   map_name = None):
    """
    Remove all definition queries added by apply_site_name_query().

    Parameters:
        map_name (str): The map name containing layers.
        aprx (project object): The project to look for the map in. The default value is the current project.
    """
    # Get name of active map
    if not map_name:
        map_name = aprx.activeMap.name
    # Get map object from name
    try:
        map_obj = aprx.listMaps(map_name)[0]
    except Exception as e:
        print(f"Could not find {map_name}: {e}")
    # Apply definition queries to all appropriate layers in the map
    for lyr in map_obj.listLayers():
        if lyr.supports("DEFINITIONQUERY") and lyr.supports("DATASOURCE") and not lyr.isGroupLayer:
            try:
                # Check if 'site_name' field exists
                desc = arcpy.Describe(lyr)
                fields = [f.name.lower() for f in arcpy.ListFields(lyr)]
                if 'site_name' in fields:
                    # Apply definition query
                    dql = lyr.listDefinitionQueries()
                    for dq in dql:
                        dq['isActive'] = False
                    lyr.updateDefinitionQueries([{}])
                    #print(f"Applied query to {lyr.name}: {query}")
            except Exception as e:
                print(f"Could not apply query to {lyr.name}: {e}")

def zoom_to_active_park(aprx = arcpy.mp.ArcGISProject("CURRENT")):
    """
    Zooms to the park that is selected in the active map.

    Parameters:
        aprx (project): the project to change the active view of
    """
    mv = aprx.activeView # mapview
    m = mv.map # map
    try:
        mv.camera.setExtent(mv.getLayerExtent(m.listLayers('Park Boundary')[0]))
    except Exception as e:
        print(f"Could not zoom to the Park Boundry layer: {e}")

import os

def update_layer_datasources(aprx = arcpy.mp.ArcGISProject("CURRENT"),
                             map_name = None,
                             old_path = r"C:\Users\Spencer_C\Desktop\GDB Copy\FloridaStateParksGIS.gdb",
                             new_path = r"\\floridadep\data\DRP\GIS\statewidecoverages\FloridaStateParksGIS.gdb"):
    """
    Replaces the workspace path of each layer in the map from the local GDB
    to the network GDB.

    Parameters:
        aprx (project): project that contains the maps and the layers. The default argument is the current project.
        map_name (str): The name of the map containing layers to update. The default argument is the
        old_path (str): the file path to the geodatabase to convert from.
        new_path (str): the file path to the geodatabase to convert to
    """
    # Get name of active map
    if not map_name:
        map_name = aprx.activeMap.name

    # Get map object from name
    try:
        map_obj = aprx.listMaps(map_name)[0]
    except Exception as e:
        print(f"Could not find {map_name}: {e}")

    # Update layer datasources
    for lyr in map_obj.listLayers():
        if lyr.supports("DATASOURCE") and not lyr.isGroupLayer:
            try:
                # Check if the layer is using the old path
                current_path = lyr.dataSource
                if old_path.lower() in current_path.lower():
                    # Extract dataset name (feature class name)
                    dataset_name = os.path.basename(current_path)
                    # Update the data source
                    lyr.updateConnectionProperties(old_path, new_path, validate=True)
                    #print(f"Updated {lyr.name} to use data from: {new_path}\\{dataset_name}")
            except Exception as e:
                print(f"Failed to update {lyr.name}: {e}")

def save_layout_file(output_folder=r'C:\Users\Spencer_C\Documents\UMP_Automation_Testing\testing',
                     aprx=arcpy.mp.ArcGISProject("CURRENT"),
                     layout_name=None,
                     pagx_filename=None):
    """
    Exports a layout from an ArcGIS Pro project to a .pagx file.

    Parameters:
        aprx (project): project that contains the maps and the layers. The default argument is the current project.
        output_folder (str): Directory where the .pagx file will be saved.
        layout_name (str): Optional. Name of the layout to export. If None, the first layout is used.
        pagx_filename (str): Optional. Filename for the exported .pagx file. Defaults to layout name.

    Returns:
        str: Full path to the exported .pagx file.
    """
    try:
        if layout_name:
            layout = next((lyt for lyt in aprx.listLayouts() if lyt.name == layout_name), None)
            if not layout:
                raise ValueError(f"Layout named '{layout_name}' not found.")
        else:
            layout = aprx.listLayouts()[0]  # default to first layout

        # Determine filename
        if not pagx_filename:
            pagx_filename = f"{layout.name}.pagx"
        pagx_path = os.path.join(output_folder, pagx_filename)

        # Export the layout
        layout.exportToPAGX(pagx_path)

        print(f"Layout '{layout.name}' exported successfully to: {pagx_path}")
        return pagx_path

    except Exception as e:
        print(f"Error exporting layout: {e}")
        raise

