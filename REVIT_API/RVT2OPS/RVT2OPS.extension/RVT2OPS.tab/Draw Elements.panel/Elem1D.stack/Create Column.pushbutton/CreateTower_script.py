#! python3
# -*- coding: utf-8 -*-
__title__   = "Create Columns"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Create a vertical analytical member from a selected point on Level X
to a new point at Level X+1 (upward)
_____________________________________________________________________
Last update:
- [21/01/2026] - V0.0 RELEASE 
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
from lib_snaptgridpt import snap_to_grid, GridIntersectionCache, pick_point
config = script.get_config("SelectedCol")
saved_family = getattr(config, "col_family", None)
saved_type   = getattr(config, "col_type", None)



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
    levels = FilteredElementCollector(doc).OfClass(Level)
    Zlevs=[]
    Ilevs=[]
    for lvl in levels:
        elev_internal = lvl.Elevation  # internal units (feet)
        Zlevs.append(elev_internal)
        Ilevs.append(lvl)
        #print(f"**{lvl.Name}**: {elev_internal:.3f} feet")
    #-- retrieve data and check if exists
    saved_symbol = None
    if saved_family and saved_type:
        collector = (
            FilteredElementCollector(doc)
            .OfClass(FamilySymbol)
            .OfCategory(BuiltInCategory.OST_StructuralColumns)
        )

        for sym in collector:
            if sym.Family.Name == saved_family and sym.Name == saved_type:
                saved_symbol = sym
                break
    
    default_type_id = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_StructuralColumns))
    default_symbol = doc.GetElement(default_type_id)


    with TransactionCM(doc,'Create Analytical Member'):
        #t.Start()
        p1_raw= uidoc.Selection.PickPoint("Pick a grid intersection")
        cache = GridIntersectionCache(doc)
        p1 = snap_to_grid(doc, p1_raw, cache)
        #p1c = Point.Create(p1)
        levldiff=[abs(x-p1.Z) for x in Zlevs]
        indz1=argmin(levldiff) #identify current level
        try: 
            Z2=Zlevs[indz1+1] #identify above level
        except:
            TaskDialog.Show("Warning", "No level exists above the active view - Column cannot be created")
        else:
        #print('Z2',Z2)
            top_level=Ilevs[indz1+1]
            p2 = XYZ(p1.X,p1.Y,Z2)
            line = Line.CreateBound(p1,p2)
            col_height = Z2 - p1.Z
            # Get Default Beam Type
            symbol_to_use = saved_symbol if saved_symbol else default_symbol
            if not symbol_to_use.IsActive:
                symbol_to_use.Activate()
                doc.Regenerate()
            column = doc.Create.NewFamilyInstance(
            p1, #it would be a line
            symbol_to_use,
            active_level,
            DBStr.StructuralType.Column) #physical member
            doc.Regenerate()   # <-- critical for 2024–2026 analytical AP
            #print(column.StructuralType)
            #print(column_type.Category.Name)
            #print("TYPE:", type(column))
            #print("CATEGORY:", column.Category.Name)
            #print("STRUCTURAL TYPE:", column.StructuralType)
            #print("ID:", column.Id)
            column.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM).Set(top_level.Id)
            DBStr.AnalyticalMember.Create(doc,line) #analytical member
        
        #t.Commit()

#print('p1',p1.X,p1.Y,p1.Z,'p2c',p2c)

#print("Hello TEST")
# Execute the main function




main()