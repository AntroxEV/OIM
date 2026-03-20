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
from Autodesk.Revit.UI import UIApplication
import Autodesk.Revit.DB.Structure as DBStr
from pyrevit import revit, framework, script
import os, sys
from lib_TransformUtils import TransactionCM
import subprocess
import json


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
def argmin(a):
    return min(range(len(a)), key=lambda x : a[x])

def findLevel(proc,payload,Zlevs):
    stdout, stderr = proc.communicate(json.dumps(payload).encode("utf-8"))

    if stderr:
        print(f"**Error:** {stderr.decode('utf-8')}")
        Z2=0
    else:
        result = json.loads(stdout.decode("utf-8"))
        Z2=Zlevs[result['index']]
        print(f"**Elevation:** {Z2}")
    
    return Z2

def main():
    active_view = doc.ActiveView
    levels = FilteredElementCollector(active_view).OfClass(Level)
    Zlevs=[]
    for lvl in levels:
        elev_internal = lvl.Elevation  # internal units (feet)
        Zlevs.append(elev_internal)
        print(f"**{lvl.Name}**: {elev_internal:.3f} feet")


    python_exe = sys.executable if "python" in sys.executable.lower() else "python"
    # Run external Python
    proc = subprocess.Popen(
        [python_exe, numpy_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
        )



    

    with TransactionCM(doc,'Create Analytical Member'):
        #t.Start()
        p1= uidoc.Selection.PickPoint("Pick start grid point")
        #p1c = Point.Create(p1)
        levldiff=abs(Zlevs-p1.Z)
        # Data to send
        payload = {
        "levldiff": levldiff
        #,
        #"p2": [10, 20, 30]
        }
        Z2=findLevel(proc,payload,Zlevs)
        p2 = XYZ(p1.X,p1.Y,Z2)
        line = Line.CreateBound(p1,p2)
        DBStr.AnalyticalMember.Create(doc,line)
        #t.Commit()

#print('p1',p1.X,p1.Y,p1.Z,'p2c',p2c)

#print("Hello TEST")
# Execute the main function



# Path to your NumPy script
numpy_script = r"..\\..\\..\\..\\lib_findLevel.py"

main()