#! python3
# -*- coding: utf-8 -*-
__title__   = "Utils for Paths "
__doc__ = """Version = 0.0
__________________________________________________________________
Description:

_____________________________________________________________________
Last update:
- [28/01/2026] - V0.0 RELEASE 
_____________________________________________________________________

_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""


#====================================================================================================
import os

def find_extension_root(path):
    while True:
        if path.lower().endswith(".extension"):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            raise Exception("Extension root not found")
        path = parent
        
def get_shared_parameter_path():
    current_file = __file__
    extension_root = find_extension_root(current_file)
    sp_path = os.path.join(extension_root, "resources", "GUID_MaterialProperties.txt")
    if not os.path.exists(sp_path):
        raise Exception("GUID_MaterialProperties file not found.")

    #app.SharedParametersFilename = sp_path
    #return app.OpenSharedParameterFile() #return file, not path
    return sp_path


