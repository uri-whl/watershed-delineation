# -*- coding: utf-8 -*-
"""
Created on 2020-11-16

@author: Josh P. Sawyer
"""

import arcpy
import extarc as ea
from pyprojroot import here

# overwrite can be set to true
arcpy.env.overwriteOutput = True

# set a prefix for all the scratch data in case we want to look at it
scr_dat_prefix = "part01"

if __name__ == "__main__":
    ea.logger.setup_logging(here("./src/logging.yaml"))
    ea.logger.send("running part one of watershed delineating")

    aoi = str(here('./data/aoi.shp'))
    nhd_flowline = str(here('./data/nhd_flowline.shp'))
    dem = arcpy.Raster(str(here('./data/aoi_dem')))
    
    # we're working with rasters, so set the extent to the AOI
    # if you DON'T have an aoi, then this is the dem extent
    arcpy.env.extent = aoi if aoi is not None else dem
    # and set the cellsize to that of the dem
    arcpy.env.cellSize = dem


    dem_clipped = str(here('./results/dem_clipped.tif', warn=False))

    # if the polygon aoi exists, clip the dem to the aoi
    if aoi is not None:
        
        dem_extent = arcpy.Describe(dem).extent
        
        ext_str = "{} {} {} {}".format(
            dem_extent.XMin,
            dem_extent.YMin,
            dem_extent.XMax,
            dem_extent.YMax
        )
        
        arcpy.Clip_management(
            dem,
            "",
            dem_clipped,
            aoi,
            nodata_value="-3.402823e+38",
            clipping_geometry="NONE",
            maintain_clipping_extent="NO_MAINTAIN_EXTENT"
        )
    else:
        # set the dem_clipped to original dem in the case it doesn't exist
        dem_clipped = dem

    # reproject the datasets to something with common units - dem is in meters,
    # so use utm zone 19
    utmz19 = ea.sr.get_sr_nad83_utm_z19()
        
    nhd_flowline_p = str(here('./results/nhd_p.shp', warn=False))
    arcpy.Project_management(nhd_flowline, nhd_flowline_p, utmz19)

    # convert nhd flowline to raster with same cellsize as dem
    nhd_flowline_r = str(here('./results/nhd_f_raster.tif', warn=False))
    
    arcpy.PolylineToRaster_conversion(
        nhd_flowline_p,
        "Enabled",
        nhd_flowline_r,
        "MAXIMUM_LENGTH",
        "NONE")
    
    # reclass to 0 / height
    nhd_flowline_rc = str(here('./results/nhd_f_rasterrc.tif', warn=False))
    
    stream_burn_height = 5
    arcpy.Reclassify_3d(
        nhd_flowline_r,
        "Value",
        "1 {};NODATA 0".format(stream_burn_height),
        nhd_flowline_rc,
        "DATA")

    # burn in the hydrography with raster calculator
    ea.logger.send("burning in hydrography")
    
    dem_b = str(here('./results/dem_burned.tif', warn=False))
    
    arcpy.RasterCalculator_ia(
        expression=" "%dem_clipped%"- "%nhd_flowline_rc%"",
        output_raster=dem_b
    )

    
    # now start working through watershed creation
    
    # fill dem using
    ea.logger.send("filling dem")

    # create a flow direction grid
    ea.logger.send("your flow direction grid is located at: ")
    
    # create a flow accumulation grid
    ea.logger.send("your flow accumulation grid is located at: ")


    ea.logger.send("processing of part 01 is complete")
    ea.logger.send("please inspect your pour points against the flow accumulation grid")
    ea.logger.send("when ready, read and then run '02_delineate_watersheds.py'")
    ea.logger.send("you'll need paths to your pour points and your accmulation grid")