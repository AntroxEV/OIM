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

#====================================================================================================
import os
from pydoc import doc
from lib_customMatManager import create_material
from pyrevit import revit
from System.Windows import Window
from uniaxialmatwindow import UniaxialMaterialWindow
from lib_findPaths import find_extension_root
#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
doc    = __revit__.ActiveUIDocument.Document #type:Document
#parameter_values = {
 #   "EmbodiedCarbon": 2500,
  #  "Manufacturer": "JBM Materials",
#}


# ---------------------------
# Load XAML
# ---------------------------
ext_root = find_extension_root(PATH_SCRIPT)
xaml_path = os.path.join(ext_root, "lib", "UniaxialMaterial.xaml")
window = UniaxialMaterialWindow(xaml_path, doc)  
winres = window.ShowDialog()

dataresult = {
    "Class": winres.material_class,
    "Type": winres.material_type,
    "Parameters": winres.parameter_values,
    "Name": winres.material_name
}


#print("Creating new material with custom parameters...")
create_material(doc, dataresult["Name"], dataresult["Parameters"])



  


