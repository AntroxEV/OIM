#! python3
# -*- coding: utf-8 -*-
__title__   = "Startup Script"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Special pyRevit hook file that runs at startup. 
Used to set up shared parameters and other necessary data for the extension.

_____________________________________________________________________
Last update:
- [28/01/2026] - V0.0 RELEASE 
_____________________________________________________________________
Icon by Icons8 https://icons8.com
_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""

from System import EventHandler
import os
from lib_binding import initialise_material_parameters
from lib_findPaths import get_shared_parameter_path

def on_document_opened(sender, args):
    uiapp = sender
    app = uiapp.Application
    doc = args.Document  # ALWAYS use event document

    # Skip family documents (optional but professional)
    if doc.IsFamilyDocument:
        return
    shared_param_path = get_shared_parameter_path()
    #print("Shared path:", shared_param_path)
    initialise_material_parameters(
        doc=doc,
        app=app,
        shared_param_path=shared_param_path
    )


# Register event
__uiapp__ = __revit__.Application
if not hasattr(__uiapp__, "_binding_registered"):
    __uiapp__.DocumentOpened += EventHandler(on_document_opened)
    __uiapp__._binding_registered = True