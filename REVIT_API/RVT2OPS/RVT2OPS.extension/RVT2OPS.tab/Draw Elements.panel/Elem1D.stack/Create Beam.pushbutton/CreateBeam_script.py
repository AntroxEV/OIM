#! python3
# -*- coding: utf-8 -*-
__title__   = "Create Beams"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Create an horizontal analytical member from two selected points on same Level

_____________________________________________________________________
Last update:
- [27/01/2026] - V0.0 RELEASE 
_____________________________________________________________________
Icon by Icons8 https://icons8.com
_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""

#====================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import UIApplication, TaskDialog
import Autodesk.Revit.DB.Structure as DBStr
from pyrevit import revit, framework, script
import os, sys
from lib_TransformUtils import TransactionCM
from lib_snaptgridpt import snap_to_closest_grid_point, pick_point
config = script.get_config("SelectedBeam")
saved_family = getattr(config, "beam_family", None)
saved_type   = getattr(config, "beam_type", None)
print(config.__dict__)




#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
uidoc   = __revit__.ActiveUIDocument #type: UI.UIDocument
app     = __revit__.Application      
doc     = __revit__.ActiveUIDocument.Document #type: Document 
active_view  = doc.ActiveView
active_level = doc.ActiveView.GenLevel
#anadoc = __revit__.ActiveUIDocument  
#.NET imports clr.AddReference('System') 
# from System.Collection.Generic import List
# listex= List[ElementID](el1,el2,...) or () and then addMethod
#====================================================================================================
def argmin(a):
    return min(range(len(a)), key=lambda x : a[x])


def main():
    #-- retrieve data and check if exists
    saved_symbol = None
    if saved_family and saved_type:
        collector = (
            FilteredElementCollector(doc)
            .OfClass(FamilySymbol)
            .OfCategory(BuiltInCategory.OST_StructuralFraming)
        )

        for sym in collector:
            if sym.Family.Name == saved_family and sym.Name == saved_type:
                saved_symbol = sym
                break
    
    default_type_id = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_StructuralFraming))
    default_symbol = doc.GetElement(default_type_id)


    with TransactionCM(doc,'Create Analytical Member'):
        #t.Start()
        p1_raw= pick_point(uidoc,"Pick start grid point")
        p1 = snap_to_closest_grid_point(doc, p1_raw)
        #p1c = Point.Create(p1)
        #print('Z2',Z2)
        p2_raw= pick_point(uidoc,"Pick end grid point")
        p2 = snap_to_closest_grid_point(doc, p2_raw)
        line = Line.CreateBound(p1,p2)
        # Get Default Beam Type
        symbol_to_use = saved_symbol if saved_symbol else default_symbol
        if not symbol_to_use.IsActive:
            symbol_to_use.Activate()
            doc.Regenerate()
        
        if saved_symbol:
            print(f"Saved symbol: {saved_symbol.Family.Name} : {saved_symbol.Name} (Id {saved_symbol.Id})")
        else:
            print("Saved symbol is None")
        
        if symbol_to_use:
            print(f"Saved symbol to use: {symbol_to_use.Family.Name} : {symbol_to_use.Name} (Id {symbol_to_use.Id})")
        else:
            print("Saved symbol is None")
        
        beam = doc.Create.NewFamilyInstance(
        line, #it would be a line
        symbol_to_use,
        active_level,
        DBStr.StructuralType.Beam) #physical member
        doc.Regenerate()   # <-- critical for 2024–2026 analytical AP
        DBStr.AnalyticalMember.Create(doc,line) #analytical member
        
        #t.Commit()

#print('p1',p1.X,p1.Y,p1.Z,'p2c',p2c)

#print("Hello TEST")
# Execute the main function



main()