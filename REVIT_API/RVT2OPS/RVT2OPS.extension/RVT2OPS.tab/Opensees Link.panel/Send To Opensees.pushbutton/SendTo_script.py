# -*- coding: utf-8 -*-
__title__   = "RUN"
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
from pyrevit import forms   # By importing forms you also get references to WPF package! Very IMPORTANT
import wpf, os, clr         # wpf can be imported only after pyrevit.forms!

#====================================================================================================
PATH_SCRIPT = os.path.dirname(__file__)
uidoc   = __revit__.ActiveUIDocument 
app     = __revit__.Application 
doc     = __revit__.ActiveUIDocument.Document #type: Document 
anadoc = __revit__.ActiveUIDocument.Structure  
#====================================================================================================
sel_el_ids = uidoc.Selection.GetElementIds()
sel_el = [doc.GetElement(e_id) for e_id in sel_el_ids]
sel_inview = [el for el in sel_el if issubclass(type(el),View)]

if not sel_inview:
    sel_inview = forms.select_views()
if not sel_inview:
    forms.alert('No Views Selected. Please try again', exitscript=True)

print('sel_inview',sel_inview)
print('sel_el',sel_el)

with Transaction(doc,'test') as t:
    t.Start()
    p1= uidoc.Selection.PickPoint()
    p2= uidoc.Selection.PickPoint()
    line = Line.CreateBound(p1,p2)
    analine = anadoc.AnalyticalMember
    t.Commit()

print('p1',p1.X,p1.Y,p1.Z,'p2',p2)

print("Hello TEST")
