import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Watershed Watch"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [DelineateWatershedFromDEM]

class DelineateWatershedFromDEM(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Delineate Watershed From DEM & Outlet"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        outlets = arcpy.Parameter(
            displayName="Watershed Outlet Point(s)",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        outlets.filter.list = ["Point"]

        dem = arcpy.Parameter(
            displayName="DEM",
            name="in_dem",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input")

        hydro = arcpy.Parameter(
            displayName="Stream Polyline (Optional)",
            name="in_hydrology",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")

        hydro.filter.list = ["Polyline"]

        out_fc = arcpy.Parameter(
            displayName="Output Features",
            name="out_features",
            datatype="GPFeatureLayer",
            parameterType="Derived",
            direction="Output")

        out_fc.parameterDependencies = [outlets.name]
        out_fc.schema.clone = True

        params = [
            outlets,
            dem,
            hydro,
            out_fc
        ]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return