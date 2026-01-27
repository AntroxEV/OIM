#! python3
# -*- coding: utf-8 -*-
__title__   = "Utils for Transformations "
__doc__ = """Version = 0.0
__________________________________________________________________
Description:

_____________________________________________________________________
Last update:
- [15/12/2025] - V0.0 RELEASE 
_____________________________________________________________________

_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""


#====================================================================================================

from Autodesk.Revit.DB import Transaction

class TransactionCM:
    def __init__(self, doc, name):
        self.t = Transaction(doc, name)

    def __enter__(self):
        self.t.Start()
        return self.t

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.t.RollBack()
        else:
            self.t.Commit()
