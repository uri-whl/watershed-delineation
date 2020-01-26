# -*- coding: utf-8 -*-
"""
Created on 2020-11-16

@author: Josh P. Sawyer
"""

import arcpy
import extarc as ea

# set environment flags - we don't want Z / M, we do want overwrite on
# the final product
arcpy.env.outputZFlag = "Disabled"
arcpy.env.outputMFlag = "Disabled"
arcpy.env.overwriteOutput = True

if __name__ == "__main__":
    ea.logger.setup_logging()
    ea.logger.send("delineating watersheds")

    flow_dir_grid = r""
    pour_points = r""

    # there are two methods for delineating sub watersheds. if you simply run
    # the watershed command against a collection of pour points and a flow direction
    # grid what you'll end up getting is a series of non-overlapping subwatersheds.
    #
    # specifically, if pour point B is downstream of pourpoint A, then the watershed
    # for B will include ONLY additional waters that flow into it AFTER point A and
    # watershed A will include all waters which flow into it.
    #
    # alternatively, if you iterate over each pour point and delineate in isolation,
    # the watersheds will contain ALL waters which flow into, e.g. point B would include
    # all the waters flowing through A and additional waters after A. this is the correct
    # interpretation for this project.
    #
    # for a concrete example - consider the worden's pond watershed, which contains 100 acre
    # and 30 acre pond. the first method would have the worden's pond watershed contain only
    # those waters which flow into it AFTER 100 acre pond. the second would correctly include
    # the waters running through 100 and 30 acre pond.

    ww_ids = ea.table.get_unique_field_values(watersheds, "gridcode")

    ea.logger.send("performing area tabulation for " + str(len(wshed_codes)) + " watersheds")
    
    for code in wshed_codes:
       ea.logger.send("operating on gridcode = " + str(code), -1)
