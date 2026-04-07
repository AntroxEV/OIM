#! python3

import os
from lib_TransformUtils import TransactionCM
from Autodesk.Revit.DB import (
    BuiltInCategory,
    GroupTypeId,
    InstanceBinding,
    TypeBinding,
)

def is_initialised(doc):
    param = doc.ProjectInformation.LookupParameter(
        "MaterialParameters_Initialised"
    )

    if param and param.AsInteger() == 1:
        return True

    return False

def mark_as_initialised(doc):
    param = doc.ProjectInformation.LookupParameter(
        "MaterialParameters_Initialised"
    )

    if param:
        param.Set(1)


def ensure_parameters_bound(
        doc,
        app,
        shared_param_path,
        group_names,
        target_bic=BuiltInCategory.OST_Materials,
        parameter_group=GroupTypeId.IdentityData,
        instance=True):
    """
    Ensures shared parameters are bound correctly.

    - Binds only missing parameters
    - Fixes incorrect category bindings
    - Fixes wrong binding type (instance/type)
    - Supports multiple shared parameter groups
    """

    if not os.path.exists(shared_param_path):
        raise Exception("Shared parameter file not found.")

    app.SharedParametersFilename = shared_param_path
    sp_file = app.OpenSharedParameterFile()

    if sp_file is None:
        raise Exception("Could not open shared parameter file.")

    binding_map = doc.ParameterBindings
    target_category = doc.Settings.Categories.get_Item(target_bic)

    # Prepare category set
    categories = app.Create.NewCategorySet()
    categories.Insert(target_category)

    desired_binding = (
        app.Create.NewInstanceBinding(categories)
        if instance
        else app.Create.NewTypeBinding(categories)
    )

    updated = []
    already_correct = []

    for group_name in group_names:

        group = sp_file.Groups.get_Item(group_name)
        if group is None:
            raise Exception("Shared parameter group '{}' not found.".format(group_name))

        for definition in group.Definitions:
            print('definition -binding:', definition.Name)
            print('XXX')
            existing_binding = binding_map.get_Item(definition)

            if existing_binding:

                # Check if already correct
                is_instance_correct = (
                    instance and isinstance(existing_binding, InstanceBinding)
                )
                is_type_correct = (
                    not instance and isinstance(existing_binding, TypeBinding)
                )

                category_correct = False
                for cat in existing_binding.Categories:
                    if cat.Id == target_category.Id:
                        category_correct = True
                        break

                if is_instance_correct and category_correct:
                    already_correct.append(definition.Name)
                    continue

                # Reinsert to fix incorrect binding
                binding_map.ReInsert(
                    definition,
                    desired_binding,
                    parameter_group
                )
                updated.append(definition.Name)

            else:
                # Not bound at all → insert
                binding_map.Insert(
                    definition,
                    desired_binding,
                    parameter_group
                )
                updated.append(definition.Name)

    return {
        "updated": updated,
        "already_correct": already_correct
    }

def initialise_material_parameters(doc, app, shared_param_path):

    if is_initialised(doc):
        return  # Already done
    print("Binding started")
    print("Shared path:", shared_param_path)
    with TransactionCM(doc,'Initialise Material Parameters'):
        ensure_parameters_bound(
            doc=doc,
            app=app,
            shared_param_path=shared_param_path,
            group_names=[
                "Material_Environmental",
                "Material_Manufacturer",
                "Material_Technical"
            ]
        )
        
        mark_as_initialised(doc)
