#! python3
# -*- coding: utf-8 -*-
__title__   = "Create 3D Member"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Create an analytical member from two selected points in the active view. 
The member will be vertical (column) if the view is a plan, and horizontal (beam) if the view is a section/elevation/3D.
The selected or default beam cross-section will be assigned to the member. 
If a default material is set, it will be assigned to the member as well. 
The structural role is structural member (not structural column or beam) to allow for more flexibility in later assigning the role.
____________________________________________________________________
Last update:
- [03/12/2025] - V0.0 RELEASE 
_____________________________________________________________________
Icon by Icons8 https://icons8.com
_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""

#====================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import UIApplication
import Autodesk.Revit.DB.Structure as DBStr
from pyrevit import revit, framework, script
import os
from lib_TransformUtils import TransactionCM

#import forms, clr         # wpf can be imported only after pyrevit.forms!
config = script.get_config("SelectedBeam")
saved_family = getattr(config, "beam_family", None)
saved_type   = getattr(config, "beam_type", None)
saved_Id = getattr(config, "beam_symbolId", None)
cfg = script.get_config("SelectedMaterial")
saved_material_id = getattr(cfg, "default_material_id", None)
#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
uidoc   = __revit__.ActiveUIDocument #type: UI.UIDocument
app     = __revit__.Application      
doc     = __revit__.ActiveUIDocument.Document #type: Document 
view    = doc.ActiveView
#anadoc = __revit__.ActiveUIDocument  
#.NET imports clr.AddReference('System') 
# from System.Collection.Generic import List
# listex= List[ElementID](el1,el2,...) or () and then addMethod
#====================================================================================================
# Correct function to check if the work plane is visible
def is_work_plane_visible(view):
    return view.AreWorkPlanesVisible()

# Correct function to toggle work plane visibility
def toggle_work_plane(view, visible):
    view.IsWorkPlaneVisible = visible


# -----------------------------
# Set the active SketchPlane
# -----------------------------
def set_plane_as_active(plane):
    with TransactionCM(doc, "Set Active Work Plane"):
        sketch_plane = SketchPlane.Create(doc, plane)
        view.SketchPlane = sketch_plane


# -----------------------------
# Create a plane aligned with the view
# -----------------------------
def get_plane_aligned_with_view(view):
    # PLAN VIEW → horizontal plane at the level elevation
    if isinstance(view, ViewPlan):
        level = view.GenLevel
        elevation = level.Elevation
        return Plane.CreateByNormalAndOrigin(XYZ.BasisZ, XYZ(0,0,elevation))

    # SECTION / ELEVATION / 3D → vertical plane aligned with view direction
    normal = view.ViewDirection
    origin = view.Origin
    return Plane.CreateByNormalAndOrigin(normal, origin)

def main():
    active_view = doc.ActiveView
    #if is_work_plane_visible(active_view):
        #toggle_work_plane(active_view, False)
    #else:
        #toggle_work_plane(active_view, True)

    # Build a plane aligned with the view
    plane = get_plane_aligned_with_view(active_view)
    # Activate the plane
    set_plane_as_active(plane)

    saved_symbol = doc.GetElement(ElementId(saved_Id)) if saved_Id else None
    
    default_type_id = doc.GetDefaultFamilyTypeId(ElementId(BuiltInCategory.OST_StructuralFraming))
    default_symbol = doc.GetElement(default_type_id)

    saved_material = revit.doc.GetElement(ElementId(saved_material_id)) if saved_material_id else None



    with TransactionCM(doc,'Create Analytical Member'):
        #t.Start()
        p1= uidoc.Selection.PickPoint("Pick start grid point")
        #p1c = Point.Create(p1)
        p2= uidoc.Selection.PickPoint("Pick end grid point")
        #p2c = Point.Create(p2)
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
        
        member = doc.Create.NewFamilyInstance(
        line, #it would be a line
        symbol_to_use,
        plane,
        DBStr.StructuralType.UnknownFraming) #physical member
        doc.Regenerate()   # <-- critical for 2024–2026 analytical AP
        analytical_member = DBStr.AnalyticalMember.Create(doc,line) #analytical member
        analytical_member.StructuralRole = DBStr.AnalyticalStructuralRole.StructuralRoleMember
        analytical_member.SectionTypeId = symbol_to_use.Id
        if saved_material is not None:
            analytical_member.MaterialId = saved_material.Id

        #t.Commit()

#print('p1',p1.X,p1.Y,p1.Z,'p2c',p2c)

#print("Hello TEST")
# Execute the main function
main()