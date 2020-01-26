# Watershed Delineation

## Overview

This repository contains a method guide and python code for delineating watersheds with an optional stream burn-in. The full technique is described in [the doc folder](doc/README.md), but this is a common approach that was automated for the purposes of generating watersheds and maps for [URI's Watershed Watch](https://web.uri.edu/watershedwatch/).

## Contents

- `doc` contains [manual instructions, script usage information and caveats](doc/README.md).
- `src` contains a standalone script for use with `arcpy`

## Requirements

You'll need the `arcpy` that ships with ArcGIS. It's recommended that you run this script against the python binary included with ArcGIS - otherwise you have to jump through hoops. See [the instructional doc](doc/README.me) for more information.

Additionally, to use the script in its current form, you'll need a small helper libray, [extarc](https://github.com/joshpsawyer/extarc). From the python terminal, type:

```bash
pip install --editable=git+https://github.com/joshpsawyer/extarc.git#egg=extarc
```

to download the latest stable version from github. Eventually, this will make its way into PyPI and can be installed with pip or conda in normal fashion.
