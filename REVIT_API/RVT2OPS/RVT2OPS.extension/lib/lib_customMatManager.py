#! python3

from pydoc import doc
from Autodesk.Revit.DB import Material, StorageType
from lib_customMatParameters import CUSTOM_PARAMETERS, ensure_material_parameters_bound
from lib_TransformUtils import TransactionCM

def set_param_by_guid(element, guid, value, param_type=None):
    """
    Set a Revit parameter by GUID with automatic type handling.

    Parameters
    ----------
    element : Autodesk.Revit.DB.Element
        The Revit element (Material, Wall, etc.) to set the parameter on.
    guid : System.Guid
        GUID of the shared parameter.
    value : any
        Value to set. Can be float, int, str depending on parameter type.
    param_type : type, optional
        Optional Python type hint (float, int, str). If None, will infer from parameter StorageType.
    """

    param = element.get_Parameter(guid)

    if param is None:
        raise ValueError(f"Parameter with GUID {guid} not found on element {element.Id}.")

    if param.IsReadOnly:
        raise ValueError(f"Parameter {param.Definition.Name} is read-only.")

    # Determine type
    if param_type is None:
        storage = param.StorageType
        if storage == StorageType.Double:
            param_type = float
        elif storage == StorageType.Integer:
            param_type = int
        elif storage == StorageType.String:
            param_type = str
        else:
            raise TypeError(f"Unsupported StorageType {storage} for parameter {param.Definition.Name}")

    # Convert and set value
    try:
        if param_type == float:
            param.Set(float(value))
        elif param_type == int:
            param.Set(int(value))
        elif param_type == str:
            param.Set(str(value))
        else:
            raise TypeError(f"Unsupported param_type {param_type}")
    except Exception as e:
        raise ValueError(f"Failed to set parameter {param.Definition.Name}: {e}")

def create_material(doc, name, parameter_values=None):
    ensure_material_parameters_bound(doc)
    with TransactionCM(doc,'Create Material'):
        material_id = Material.Create(doc, name)
        material = doc.GetElement(material_id)

        # Loop through all defined parameters
        for param_name, param_data in CUSTOM_PARAMETERS.items():
            # param_data can be Guid or dict with metadata
            if isinstance(param_data, dict):
                guid = param_data["guid"]
                py_type = param_data.get("type", None)
            else:
                guid = param_data
                py_type = None

            # Determine value to assign
            value = None
            if parameter_values and param_name in parameter_values:
                value = parameter_values[param_name]

            # Skip parameters without a value
            if value is not None:
                try:
                    set_param_by_guid(material, guid, value, param_type=py_type)
                except Exception as e:
                    # Optional: log error or continue silently
                    print(f"Warning: could not set parameter {param_name}: {e}")

    return material