#! python3
# -*- coding: utf-8 -*-
__title__   = "Activate Analytical View"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Toogle ON/OFF visibility of analytical nodes and members in the current view.
The toggle state stays global, but the effect is applied per‑view
_____________________________________________________________________
Last update:
- [28/12/2025] - V0.0 RELEASE 
_____________________________________________________________________
Icon by Icons8 https://icons8.com
_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""


#====================================================================================================


from pyrevit import script
from Autodesk.Revit.DB import *
from lib_TransformUtils import TransactionCM

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
view = doc.ActiveView


def show_analytical(view):
    with TransactionCM(doc, "Show Analytical Model"):

        # Required for nodes
        view.DetailLevel = ViewDetailLevel.Fine

        # Categories to show
        categories = [
            BuiltInCategory.OST_AnalyticalModel,
            BuiltInCategory.OST_AnalyticalNodes,
            BuiltInCategory.OST_AnalyticalBeams,
            BuiltInCategory.OST_AnalyticalColumns,
            BuiltInCategory.OST_AnalyticalBraces
        ]

        for bic in categories:
            cat = Category.GetCategory(doc, bic)
            if cat:
                view.SetCategoryHidden(cat.Id, False)



def hide_analytical(view):
    with TransactionCM(doc, "Hide Analytical Model"):

        categories = [
            BuiltInCategory.OST_AnalyticalModel,
            BuiltInCategory.OST_AnalyticalNodes,
            BuiltInCategory.OST_AnalyticalBeams,
            BuiltInCategory.OST_AnalyticalColumns,
            BuiltInCategory.OST_AnalyticalBraces
        ]

        for bic in categories:
            cat = Category.GetCategory(doc, bic)
            if cat:
                view.SetCategoryHidden(cat.Id, True)


# -----------------------------
# MAIN TOGGLE 
# -----------------------------
state = script.get_toggle_state()

if toggle_state:
    show_analytical(view)
else:
    hide_analytical(view)
