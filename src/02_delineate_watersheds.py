# -*- coding: utf-8 -*-
"""
Created on 2020-11-16

@author: Josh P. Sawyer
"""

import arcpy
import extarc as ea
from pyprojroot import here

# set environment flags - we don't want Z / M, we do want overwrite on
# the final product
arcpy.env.outputZFlag = "Disabled"
arcpy.env.outputMFlag = "Disabled"
arcpy.env.overwriteOutput = True

if __name__ == "__main__":
    ea.logger.setup_logging()
    ea.logger.send("delineating watersheds")

    # flow direction from part 1
    flow_dir_grid = str(here('./results/dem_fdirection.tif', warn=False))
    pour_points = str(here('./data/pour_point.shp', warn=False))

    # there are two methods for delineating sub watersheds. if you simply run
    # the watershed command against a collection of pour points and a flow direction
    # grid what you'll end up getting is a series of non-overlapping subwatersheds.
    #
    # specifically, if pour point B is downstream of pourpoint A, then the watershed
    # for B will include ONLY additional waters that flow into it AFTER point A
    # and watershed A will include all waters which flow into it.
    #
    # alternatively, if you iterate over each pour point and delineate in isolation,
    # the watersheds will contain ALL waters which flow into, e.g. point B would
    # include all the waters flowing through A and additional waters after A.
    # this is the correct interpretation for this project.
    #
    # for a concrete example - consider the worden's pond watershed, which
    # contains 100 acre and 30 acre pond. the first method would have the
    # worden's pond watershed contain only those waters which flow into it
    # AFTER 100 acre pond. the second would correctly include the waters
    # running through 100 and 30 acre pond.

    # you need to iterate on a meaningful unique field - here, we use the watershed
    # watch station number
    ww_ids = ea.table.get_unique_field_values(pour_points, "WW_StaNumb")

    ea.logger.send("performing watershed calculation for " + str(len(ww_ids)) + " pour points")
    
    watersheds = []
    
    # to do select by attribute, need a feature layer    
    pp_flayer = "pp_flayer"
    arcpy.MakeFeatureLayer_management(pour_points, pp_flayer)
    
    for code in ww_ids:
        ea.logger.send("operating on WW_StaNumb = " + str(code), -1)
       
        # select the one attribute
        # select a feature
        arcpy.SelectLayerByAttribute_management(pp_flayer, 'NEW_SELECTION', 
                                        '"WW_StaNumb" = ' + str(code))
        # make a scratch copy
        sc_wshed = ea.object.get_unused_fc_in_memory()
    
        #    
        arcpy.CopyFeatures_management(pp_flayer, sc_wshed)
       
        # perform the watershed calculation
        outWatershed = arcpy.sa.Watershed(flow_dir_grid, sc_wshed, "WW_StaNumb")
         
        
        
        # save to scratch gdb
        wshed_poly = ea.object.get_unused_fc_in_memory()
        # convert to polygon
        
        arcpy.RasterToPolygon_conversion(outWatershed, wshed_poly, "NO_SIMPLIFY", "value")
        
        # append to delineated array
        watersheds.append(wshed_poly)
       
    delineated_wsheds = str(here('./results/delineated_wsheds.shp', warn=False))
       
    arcpy.Merge_management(watersheds, delineated_wsheds)
    
    ea.logger.send("processing complete")
    ea.logger.send("your delineated wshed file is located at: {}".format(delineated_wsheds))
