#! python3
from System import Guid
from lib_findPaths import get_shared_parameter_path
from lib_binding import ensure_parameters_bound

# Shared parameter groups
GROUP_ENV = "Material_Environmental"
GROUP_MANU = "Material_Manufacturer"
GROUP_TECH = "Material_Technical"

ALL_GROUPS = [GROUP_ENV, GROUP_MANU, GROUP_TECH]

# GUID registry

CUSTOM_PARAMETERS = {
    "EmbodiedCarbon": {"guid": Guid("11111111-2222-3333-4444-555555555555"), "type": float, "group": "Material_Environmental"},
    "GlobalWarmingPotential": {"guid": Guid("22222222-3333-4444-5555-666666666666"), "type": float, "group": "Material_Environmental"},
    "RecycledContent": {"guid": Guid("33333333-4444-5555-6666-777777777777"), "type": float, "group": "Material_Manufacturer"},
    "Manufacturer": {"guid": Guid("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"), "type": str, "group": "Material_Manufacturer"},
    "ProductCode": {"guid": Guid("bbbbbbbb-cccc-dddd-eeee-ffffffffffff"), "type": str, "group": "Material_Manufacturer"},
    "EPDReference": {"guid": Guid("cccccccc-dddd-eeee-ffff-111111111111"), "type": str, "group": "Material_Manufacturer"},
    "YoungModulusNegative": {"guid": Guid("55555555-6666-7777-8888-999999999999"), "type": float, "group": "Material_Technical"},
    "DryDensity": {"guid": Guid("66666666-7777-8888-9999-aaaaaaaaaaaa"), "type": float, "group": "Material_Technical"},
    # add hundreds more here
}

# Project flag
INITIALISED_FLAG = "MaterialParameters_Initialised"

# binding wrapper
def ensure_material_parameters_bound(doc):
    app = doc.Application
    shared_param_path = get_shared_parameter_path()

    ensure_parameters_bound(
        doc=doc,
        app=doc.Application,
        shared_param_path=shared_param_path,
        group_names=ALL_GROUPS,
    )