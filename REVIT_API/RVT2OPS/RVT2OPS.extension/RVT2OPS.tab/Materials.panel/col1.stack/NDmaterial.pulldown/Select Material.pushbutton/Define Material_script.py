#! python3
# -*- coding: utf-8 -*-
__title__   = "Select Material"
__doc__ = """Version = 0.0
__________________________________________________________________
Description:
Select material in the current Revit document and show its properties in the Properties panel.

_____________________________________________________________________
Last update:
- [28/01/2026] - V0.0 RELEASE 
_____________________________________________________________________
Icon by Icons8 https://icons8.com
_____________________________________________________________________
Author: Dr Alessandro Tombari https://antroxev.github.io/"""


from lib_TransformUtils import TransactionCM
from pyrevit import revit, DB

from Autodesk.Revit.DB.Visual import AssetType
from  Autodesk.Revit.DB.ExtensibleStorage import (
    Schema, 
    SchemaBuilder,
    Entity, 
    AccessLevel,
) 
from Autodesk.Revit.DB import  Material, MaterialAspect
from System import Guid, Double
from Autodesk.Revit.DB import UnitTypeId



doc = revit.doc
uidoc = revit.uidoc
app = doc.Application



# ------------------------------------------------------------
# 1. Create or retrieve a schema for custom material properties
# ------------------------------------------------------------
def get_or_create_schema():
    # Use your own stable GUID here
    schema_guid = Guid("e3a4b7d2-9c1f-4f7a-8b3d-abcdef123456")
    schema = Schema.Lookup(schema_guid)
    if schema:
        return schema

    builder = SchemaBuilder(schema_guid)
    builder.SetSchemaName("CustomStructuralMaterialProperties")
    builder.SetReadAccessLevel(AccessLevel.Public)
    builder.SetWriteAccessLevel(AccessLevel.Public)

    # Structural physical properties (all stored as Double)
    # --- Unit-aware fields ---
    builder.AddSimpleField("Density", Double)
    builder.AddSimpleField("YoungModulus", Double)


    builder.AddSimpleField("PoissonRatio", Double)
    # Custom properties
    builder.AddSimpleField("Porosity", Double)
    builder.AddSimpleField("VoidRatio", Double)

    return builder.Finish()

# ------------------------------------------------------------
# 2. Create a new material
# ------------------------------------------------------------
def create_material(name="CE_Custom_Material_01"):
    mat_id = Material.Create(doc, name)
    return doc.GetElement(mat_id)


# ------------------------------------------------------------
# 3. Store structural + custom properties via Extensible Storage
# ------------------------------------------------------------
def set_custom_properties(material,
                          density,
                          youngs_modulus,
                          poisson_ratio,
                          porosity,
                          void_ratio):
    schema = get_or_create_schema()
    entity = Entity(schema)

    entity.Set(schema.GetField("Density"),       Double(density), UnitTypeId.KilogramsPerCubicMeter)
    entity.Set(schema.GetField("YoungModulus"),  Double(youngs_modulus), UnitTypeId.KilonewtonsPerSquareMeter)
    entity.Set(schema.GetField("PoissonRatio"),  Double(poisson_ratio))
    entity.Set(schema.GetField("Porosity"),      Double(porosity))
    entity.Set(schema.GetField("VoidRatio"),     Double(void_ratio))

    material.SetEntity(entity)



# ------------------------------------------------------------
# 5. Main execution
# ------------------------------------------------------------
with TransactionCM(doc,'Create Analytical Member'):

    # User inputs (replace with UI later if needed)
    density = 1800.0
    youngs_modulus = 25e9
    poisson_ratio = 0.25
    porosity = 0.18
    void_ratio = 0.22

    mat = create_material("Material_With_Custom_Props")

    # Assign physical asset
    set_custom_properties(mat,
                          density,
                          youngs_modulus,
                          poisson_ratio,
                          porosity,
                          void_ratio)

  


