# Watershed Delineation Method for Rhode Island

Sara Frazer, Seaver Anderson & Josh Sawyer
Created: 5/7/2018; Last Updated: 11/10/2019

## Summary

This is the method used to delineate sub-watersheds for Watershed Watch sampling locations. Processing of the original DEM (fill through flow accumulation) is very slow and takes up a lot of space. For this process you need a digital elevation model (DEM) and a (point) feature class of the location of the outlet of the watershed that you want to delineate. Having a compatible location for the watershed outlet is critical for the watershed to be delineated accurately. A Python script was developed to automate the delineation process however the outlet point must still be manually created.

## Requirements

1. ArcMap 10.x or ArcGIS Pro
2. A digital elevation model (DEM) covering the surface of the watershed that you're delineating.
3. A point feature class containing an outlet point for the watershed that you're delineating.
4. A polyline feature class containing existing stream & river networks within the watershed of interest - when in doubt, you can fall back to the NHD datasets

## Manual Procedure

1. _(Optional)_ Clip DEM to area of interest. If you're delineating a subwatershed, such as a URI Watershed Watch sampling point, then you may consider clipping to the HUC10 or HUC12 watershed which contains it, knowing that the subwatershed must necessarily be contained within (note: strictly speaking, this may not be true, as the NHD watershed definitions may lag RI LiDAR derived DEMs. You can do this if you believe your subwatershed is _well_ within the containing watershed, but in the event it lies adjacent to the edge and the area has undergone regrading or other land restructuring (earth quake? sink hole? a giant parking lot and associated re-leveling?), this may be a bad assumption to make). The processing time is greatly improved with a smaller DEM.

2. Convert DEM, outlet feature class and stream feature class to the same projection. It is suggested to match the units of the coordinate system with the units of elevation in the DEM for watershed delineation. The elevation values of the USGS DEM are in meters, and the units for UTM coordinate system are also in meters - for this reason, and that RI is completely contained with UTM Zone 19, using the UTM Zone 19 projected coordinate system is logical.

3. Perform a hydrography _burn-in_ of the DEM with the stream network (see Tarboton, 2012 for a more complete approach; the method described here is simpler). This will lessen the potential for error due to culverts and other under-the-road water connections that will affect the watershed delineation.

    a. Convert the stream network to a raster using the `Polyline to Raster` tool of the `Conversion` toolbox. Specify the cell size as being that of the DEM raster; use any field for value as we'll reclass it shortly.

    b. Reclassify the raster values using the `Reclassify` tool from the `Spatial Analyst` toolbox, setting any _actual_ value to the same constant number and `NoData` to 0. Whatever value you choose for a constant is how much the DEM will be lowered by for cells that overlap the stream raster. Think of it as carving a channel into the DEM so that culverts or other features not observed in a DEM are recognized as connections for a watershed. If you've followed the steps exactly, a good number is in the range of (5, 10) as the vertical unit is meters.

    c. Using `Raster Calculator` from the `Spatial Analyst` toolbox, subtract the stream raster from the DEM. Use the output in the next phase of delineation.

4. Follow the instructions in (Parmenter & Melcher, 2012) or (MaDGIC, 2014). They are reproduced here in brief, but more data is contained within the original article. These tools are located in the `Spatial Analyst` > `Hydrology` toolbox.

    a. Fill DEM using the `Fill` tool to remove any depressions / sinks (cells that do not drain)

    b. Create a flow direction grid / raster using the `Flow Direction` tool. Each cell references another cell to establish direction of flow - there's little point in visualizing this.

    c. Create a flow accumulation grid / raster the `Flow Accumulation` tool. Each cell will now contain the number of cells which flow into it.

    d. Change the symbology on the flow accumulation grid to have two classes - those above a certain number _N_ and those below. The goal is to contrast between those cells which have high flow accumulation and those that don't. You will need to experimentally determine the best _N_ for your purposes. We recommend trying a value of 2000 to start, symbolizing any cell with a number greater than 2000 as white, and everything else as black. When finished, you'll see the major flow lines through the watershed - they should line up approximately with known major rivers.

    e. You may need to edit the outlet point so that it sits on top of the closest high flow accumulation line. If you do, simply edit the point and align it with the flow line. Your goal is to place them at approximately the watershed outlet as dictated by the flow lines.

    f. Use the `Snap Pour Point` tool to align the pour point _definitively_ to the highest flow accumulation point in a certain radius, as well as create a raster dataset containing the pour points.

    f. Finally, create the watershed using the `Watershed` tool and your pour points and flow direction raster. You now have a raster of the delineated watersheds.

    g. Convert watershed from raster to vector.

    h. Convert watershed to final desired projection.

5. Do a final review of the watershed and fix any big errors - this is critical! The delineation process is not perfect and there is almost always something not right in the delineated boundary. Because it is based on the DEM, it does not account for large amounts of impervious cover or hydrography. Display the stream network and contour lines on top of the watershed at the end to make sure that it makes sense. If a stream is cut in half, you should adjust the boundary of the watershed to encompass the entire stream by following the contour lines.

## Scripts

The above process has been scripted and can be run directly from the command line or an IDE such as PyCharm, Spyder or VS Code. For simplicity, it's imperative that you use the binary that comes with your ArcGIS installation, otherwise you will need to go through the difficulty of loading that `arcpy` module into a different binary - doable, but not easy. For explanation on how to do to the complicated `arcpy` loading in a different binary, see [this USGS article that describes how to combine (Ana)conda and `arcpy`](https://my.usgs.gov/confluence/display/EGIS/Using+Anaconda+modules+from+the+ESRI+python+environment).

Alternative, just use the scripts within `..\src` and run them with the provided binary.

The delineation process can be automated for many given points at one time using the script I wrote in Python located in Seaver’s folder, `S:\Gold_Lab\Seaver\Watershed Watch Data\Delineation Files\Python Scripts`. The process of snapping the outlet point to a flow accumulation must still be done manually. This script can delineate many  watersheds at once and convert them to shapefiles in a matter of minutes rather than going through the whole process in ArcGIS. The script has instructions on lines that need to be changed and is quite simple. Make sure the Project Interpreter is set to Python 2.7 before running the code.

## Specific Notes for RI

It's tempting to use RIGIS for all data, but don't. Many of the watersheds will either start or flow into another state, and using only data from RIGIS gives you a hard edge at the state boundary in most cases. NHD data should be used for burn in networks instead of CT / RI / MA data - the spatial resolution isn't as great, but it's consistent across state borders.

Even _with_ the NHD flowline as the burn in, there can be problems. One such example is Mishnock Lake. The steps as described above resulted in a large watershed that included parts of the Flat River Reservoir Watershed. This is because the burn in didn't not lower the height enough for the portion of the river underneath I-95, and so the lowest pour point was through Mishnock Lake. This example underscores the importance of comparing watersheds to actual hydrography and contour lines.

## References

- MaDGIC. (2014, August). Watershed Delineation with ArcGIS 10.2.x. Retrieved from <http://www.trentu.ca/library/sites/default/files/documents/WatershedDelineation_10_2.pdf>
- Parmenter, B., & Melcher, J. (2012, January 10). Watershed and Drainage Delineation by PourPoint in ArcMap 10. Retrieved from <http://sites.tufts.edu/gis/files/2013/11/Watershed-and-Drainage-Delineation-by-Pour-Point.pdf>
- Tarboton, D. (2012). Exercise 4. Watershed and Stream Network Delineation. Retrieved from <http://www.ce.utexas.edu/prof/maidment/giswr2012/Ex4/Ex42012.pdf>
