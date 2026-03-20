#! python3
# -*- coding: utf-8 -*-
__title__   = "Create Member"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Send the analytical model to opensees for structural analysis
_____________________________________________________________________
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
from pyrevit import revit, framework
import os
from lib_TransformUtils import TransactionCM

#import forms, clr         # wpf can be imported only after pyrevit.forms!

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


    with TransactionCM(doc,'Create Analytical Member'):
        #t.Start()
        p1= uidoc.Selection.PickPoint("Pick start grid point")
        #p1c = Point.Create(p1)
        p2= uidoc.Selection.PickPoint("Pick end grid point")
        #p2c = Point.Create(p2)
        line = Line.CreateBound(p1,p2)
        DBStr.AnalyticalMember.Create(doc,line)
        #t.Commit()

#print('p1',p1.X,p1.Y,p1.Z,'p2c',p2c)

#print("Hello TEST")
# Execute the main function
main()