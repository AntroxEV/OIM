#! python3
# -*- coding: utf-8 -*-
__title__   = "Select Column Cross-Section"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Select family types for structural columns

_____________________________________________________________________
Last update:
- [28/01/2026] - V0.0 RELEASE 
_____________________________________________________________________
Icon by Icons8 https://icons8.com
_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""

#====================================================================================================
from Autodesk.Revit.DB import FilteredElementCollector, FamilySymbol, BuiltInCategory
from Autodesk.Revit.UI import UIApplication
from pyrevit import revit, framework, script
import os,sys
from lib_findPaths import find_extension_root
from System.Windows.Markup import XamlReader
from System.IO import FileStream, FileMode
#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
uidoc   = __revit__.ActiveUIDocument #type: UI.UIDocument
app     = __revit__.Application      
doc     = __revit__.ActiveUIDocument.Document #type: Document 
config = script.get_config("SelectedCol")
col_family = getattr(config, "col_family", None)
col_type = getattr(config, "col_type", None)
col_symbolId = getattr(config, "col_symbolId", None)
#====================================================================================================



# --- Load XAML UI ---
# Path to extension root
#print(PATH_SCRIPT)
# Add lib folder to sys.path
ext_root = find_extension_root(PATH_SCRIPT)
# Path to XAML inside lib
xaml_path = os.path.join(ext_root, "lib", "uiDropDown.xaml")
#lib_path = os.path.join(ext_root, "lib")
#print(xaml_path)
#print("ext_root:", ext_root)
fs = FileStream(xaml_path, FileMode.Open)
window = XamlReader.Load(fs)
fs.Close()
familyBox = window.FindName("familyBox")
typeBox = window.FindName("typeBox")
okButton = window.FindName("okButton")

# --- Collect families and types ---
CATEGORIES = [
    BuiltInCategory.OST_StructuralColumns,
    #BuiltInCategory.OST_StructuralFraming
]

symbols = []
for cat in CATEGORIES:
    symbols.extend(
        FilteredElementCollector(doc)
        .OfClass(FamilySymbol)
        .OfCategory(cat)
    )

families = {}
for sym in symbols:
    fam = sym.Family.Name
    if fam not in families:
        families[fam] = []
    families[fam].append(sym)

# Populate family dropdown
for fam in sorted(families.keys()):
    familyBox.Items.Add(fam)


# Preselect last used family
if col_family in families:
    familyBox.SelectedItem = col_family

# When family changes, update types
def on_family_changed(sender, args):
    typeBox.Items.Clear()
    fam = familyBox.SelectedItem
    if fam:
        for sym in sorted(families[fam], key=lambda s: s.Name):
            typeBox.Items.Add(sym.Name)

        # Preselect last used type (only if it belongs to this family)
        if fam == col_family and col_type:
            if col_type in [s.Name for s in families[fam]]:
                typeBox.SelectedItem = col_type

familyBox.SelectionChanged += on_family_changed

# Trigger initial type population if family was preselected
if familyBox.SelectedItem:
    on_family_changed(None, None)

# Capture result
selected_symbol = None

def on_ok(sender, args):
    fam = familyBox.SelectedItem
    typ = typeBox.SelectedItem
    if fam and typ:
        global selected_symbol
        selected_symbol = next(s for s in families[fam] if s.Name == typ)

        # Save new defaults
        config.col_family = fam
        config.col_type = typ
        config.col_symbolId = selected_symbol.Id.IntegerValue
        script.save_config()

        window.Close()

okButton.Click += on_ok

# Show UI
window.ShowDialog()




