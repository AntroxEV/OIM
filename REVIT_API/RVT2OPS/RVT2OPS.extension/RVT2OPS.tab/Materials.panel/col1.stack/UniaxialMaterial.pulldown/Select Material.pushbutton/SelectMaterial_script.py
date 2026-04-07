#! python3
# -*- coding: utf-8 -*-
__title__   = "Select Existing Material"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Select an existing material in the current Revit document and save it as default for the current pyRevit session. This is used to pre-select the material in the Uniaxial Material pulldown menu.

_____________________________________________________________________
Last update:
- [03/04/2026] - V0.0 RELEASE 
_____________________________________________________________________
Icon by Icons8 https://icons8.com
_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""

#====================================================================================================
import os
from pyrevit import revit, DB, script
from Autodesk.Revit.UI import UIDocument
import System
from System.Windows import Window, MessageBox
from System.Windows.Controls import ComboBox, Button, TextBox
from System.Windows.Markup import XamlReader
from System.IO import StreamReader
from lib_findPaths import find_extension_root
#====================================================================================================

PATH_SCRIPT = os.path.dirname(__file__)
doc = revit.doc
uidoc = __revit__.ActiveUIDocument

# ---------------------------
# Material helper class
# ---------------------------
class MaterialItem(object):
    def __init__(self, material):
        self.Name = material.Name
        self.Id = material.Id.Value
        self.Element = material

    def __str__(self):
        return self.Name

# ---------------------------
# Load all materials
# ---------------------------
materials = DB.FilteredElementCollector(doc).OfClass(DB.Material).ToElements()
items = sorted([MaterialItem(m) for m in materials], key=lambda x: x.Name)

# ---------------------------
# Load XAML
# ---------------------------
ext_root = find_extension_root(PATH_SCRIPT)
xaml_path = os.path.join(ext_root, "lib", "uiMaterialSelect.xaml")

sr = StreamReader(xaml_path)
window = XamlReader.Load(sr.BaseStream)
sr.Close()

# Access controls
materialBox = window.FindName("materialBox")
searchBox = window.FindName("searchBox")
okButton = window.FindName("okButton")
currentSelectionLabel = window.FindName("currentSelectionLabel")

# ---------------------------
# Populate ComboBox
# ---------------------------
materialBox.Items.Clear()
for m in items:
    materialBox.Items.Add(m)

materialBox.SelectedIndex = 0

# ---------------------------
# Check Material Change
# ---------------------------

def on_material_changed(sender, args):
    m = materialBox.SelectedItem
    if m:
        currentSelectionLabel.Text = "Selected: {}".format(m.Name)

materialBox.SelectionChanged += on_material_changed


# ---------------------------
# Check Default Selection
# ---------------------------

cfg = script.get_config("SelectedMaterial")
previous_id = getattr(cfg, "default_material_id", None)

if previous_id:
    # find matching item
    for i, m in enumerate(items):
        if m.Id == int(previous_id):
            materialBox.SelectedIndex = i
            currentSelectionLabel.Text = "Previously selected: {}".format(m.Name)
            break


# ---------------------------
# Search filter
# ---------------------------
def on_search_changed(sender, args):
    text = searchBox.Text.lower()
    filtered = [m for m in items if text in m.Name.lower()]
    materialBox.Items.Clear()
    for m in filtered:
        materialBox.Items.Add(m)
    if filtered:
        materialBox.SelectedIndex = 0

searchBox.TextChanged += on_search_changed

# ---------------------------
# OK button handler
# ---------------------------
selected_material = None
dialog_result = False   

def on_ok(sender, args):
    global selected_material
    selected_material = materialBox.SelectedItem
    dialog_result = True
    window.Close()

okButton.Click += on_ok

# ---------------------------
# Show window
# ---------------------------
window.ShowDialog()

if not dialog_result or selected_material is None:
    try:
        script.exit()
    except SystemExit:
        pass

# ---------------------------
# Save to pyRevit config
# ---------------------------
# FIX: must store primitives
if selected_material is not None:
    cfg = script.get_config("SelectedMaterial")
    cfg.default_material_id = selected_material.Id
    cfg.default_material_name = selected_material.Name
    #print("Selected material:", selected_material.Name)
    script.save_config()
else:
    #print("No material selected.")
    pass

