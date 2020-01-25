# Watershed Delineation

## Overview

This repository contains a method guide and python code for delineating watersheds with an optional stream burn-in. The full technique is described in [the doc folder](doc/README.md), but this is a common approach that was automated for the purposes of generating watersheds and maps for [URI's Watershed Watch](https://web.uri.edu/watershedwatch/).

## Contents

- `doc` contains [manual instructions, script usage information and caveats](doc/README.md).
- `src` contains a standalone script for use with `arcpy`

## Requirements

You'll need `arcpy`, either 2.x or 3.x. It's recommended that you run this script against the python binary included with ArcGIS.