# -*- coding: utf-8 -*-
"""
Created on 2020-11-16

@author: Josh P. Sawyer
"""

import arcpy

# set environment flags - we don't want Z / M, we do want overwrite on
# the final product
arcpy.env.outputZFlag = "Disabled"
arcpy.env.outputMFlag = "Disabled"
arcpy.env.overwriteOutput = True

if __name__ == "__main__":
    print("ok")