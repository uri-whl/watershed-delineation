# -*- coding: utf-8 -*-
"""
this is an extra file that you don't actually need to delineate watersheds
but it was created for this project to run LULC analysis over each watershed.

it's not otherwise versioned so it was stashed here. to use it you'll need
to change field names and paths.

@author: Josh P. Sawyer
"""

import arcpy
from pyprojroot import here
import extarc as ea

# set environment flags - we don't want Z / M, we do want overwrite on
# the final product
arcpy.env.outputZFlag = "Disabled"
arcpy.env.outputMFlag = "Disabled"
arcpy.env.overwriteOutput = True

if __name__ == "__main__":
    ea.logger.setup_logging()    
    
    watersheds = str(here('./final.gdb/watershed_watch/watershed_delineated', warn=False))
    lulc = str(here('./final.gdb/RasterT_NLCD_201', warn=False))

    ea.logger.send("Tabulating area by L1 type for watersheds")
    
    tabulations = []
    
    wshed_flayer = "wshed_flayer"
    
    arcpy.MakeFeatureLayer_management(watersheds, wshed_flayer)

    
    # get unique object ids from the watershed dataset
    wshed_codes = ea.table.get_unique_field_values(watersheds, "gridcode")
    
    ea.logger.send("performing area tabulation for " + str(len(wshed_codes)) + " watersheds")
    
    for code in wshed_codes:
        ea.logger.send("operating on gridcode = " + str(code), -1)
        # select a feature
        arcpy.SelectLayerByAttribute_management(wshed_flayer, 'NEW_SELECTION', 
                                        '"gridcode" = ' + str(code))
        # make a scratch copy
        sc_wshed = ea.object.get_unused_fc_in_memory()
        arcpy.CopyFeatures_management(wshed_flayer, sc_wshed)

        # get a scratch table
        sc_table = ea.object.get_unused_fc_in_memory()
             
        # perform the tabulation in a scratch tablw
        arcpy.sa.TabulateArea(
            sc_wshed,
            "gridcode",
            lulc,
            "Level1",
            sc_table)
    
        # append it to the list
        tabulations.append(sc_table)
    
    # merge them all back together
    ea.logger.send("merging tabulated data")
        
    m_table = ea.object.get_unused_scratch_fc()
    
    arcpy.Merge_management(tabulations, m_table)

    # the area is in units, but we need it in %
    # iterate over all the rows and recalculated as %
    area_fields = [
        "LEVEL_1",
        "LEVEL_2",
        "LEVEL_3",
        "LEVEL_4",
        "LEVEL_7",
        "LEVEL_8",
        "LEVEL_9"
    ]


    ea.logger.send("converting sums to %")
    
    cursor = arcpy.da.UpdateCursor(m_table, area_fields)

    for row in cursor:
        total_area = 0
        
        for i in range(0, len(area_fields)):
            if row[i] is not None:
                total_area += row[i]
  
        for i in range(0, len(area_fields)):
            if row[i] is not None:
                row[i] /= total_area
            else:
                row[i] = 0
        
        ea.logger.send(str(total_area))
        # field2 will be equal to field1 multiplied by 3.0
        #row.setValue(field2, row.getValue(field1) * 3.0)
        cursor.updateRow(row)
       
    # copy to final.gdb
    watershed_lulc = str(here('./final.gdb/watershed_lulc', warn=False))
    
    arcpy.CopyRows_management(m_table, watershed_lulc)
    
    wshed_df = ea.table.get_arcgis_table_as_df(watershed_lulc)
    
    wshed_pour = str(here('./final.gdb/watershed_watch/watershed_pour_points', warn=False))
    wshed_names = ea.table.get_arcgis_table_as_df(wshed_pour)
    
    wshed_joined = wshed_df.set_index('GRIDCODE').join(wshed_names.set_index('WW_StaNumb'))
    
    wshed_joined.to_csv("watershed_lulc_percentage.csv")
    
    # also write out as a csv
    ea.logger.send("Completed L1 area tabluation, results in: " + watershed_lulc)