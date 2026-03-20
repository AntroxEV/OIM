#! python3
# -*- coding: utf-8 -*-
__title__   = "Create New Material"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Create a new material in the current Revit document and set custom structural properties.

_____________________________________________________________________
Last update:
- [28/01/2026] - V0.0 RELEASE 
_____________________________________________________________________
Icon by Icons8 https://icons8.com
_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""


from pydoc import doc
from lib_customMatManager import create_material
from pyrevit import revit

doc    = __revit__.ActiveUIDocument.Document #type:Document
parameter_values = {
    "EmbodiedCarbon": 2500,
    "Manufacturer": "JBM Materials",
}



create_material(doc, "Concrete_Custom_02", parameter_values)



  


