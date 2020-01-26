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

# put function in here to get something in the scratch gdb

if __name__ == "__main__":
    ea.logger.setup_logging()
    ea.logger.send("running part one of watershed delineating")

    dem_location = r""

    polygon_aoi_fc = None

    nhd_flowline = r""

    dem_clipped = r""

    if polygon_aoi_fc is not None:
        # clip
        True
    else:
        True
        # set the dem_clipped to original dem

    # reproject the datasets to common sr

    nhd_flowline_utmz19 = r""

    dem_clipped_utmz19 = r""

    # burn in the hydrography

    # fill dem using

    # create a flow direction grid

    # create a flow accumulation grid

    # your flow accumulation grid is at >

    # your flow direction grid is at >

    # you must now manually adjust your pour points to the accumulation grid. see instructions.

    # when ready, copy the path to the flow direction grid to the next script.