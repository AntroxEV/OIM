#! python3
from System.Windows import Window
from System.Windows.Controls import (
    StackPanel, TextBlock, TextBox
)
from collections import defaultdict
from resources.OPS_MATERIALS import UNIAXIAL_MATERIALS

def group_by_class(materials):
    grouped = defaultdict(dict)
    for key, data in materials.items():
        grouped[data["class"]][key] = data
    return grouped

class UniaxialMaterialWindow(Window):
    def __init__(self, xaml_path, doc):
        import wpf
        wpf.LoadComponent(self, xaml_path)

        self.grouped = group_by_class(UNIAXIAL_MATERIALS)
        self.parameter_controls = {}
        self.doc = doc

        self.ClassCombo.ItemsSource = sorted(self.grouped.keys())
        self.ClassCombo.SelectionChanged += self.on_class_changed
        self.TypeCombo.SelectionChanged += self.on_type_changed

        self.material_class = None
        self.material_type = None
        self.parameter_values = None
        self.material_name = None


    def _is_valid_revit_name(self, name):
        if not name:
            return False, "Material name cannot be empty."

        illegal = ':{}[]|;<>?'
        if any(ch in name for ch in illegal):
            return False, "Material name contains invalid characters: : { } [ ] | ; < > ?"

        return True, None


    def _material_exists(self, name):
        from Autodesk.Revit.DB import FilteredElementCollector, Material
        mats = FilteredElementCollector(self.doc).OfClass(Material)
        return any(m.Name == name for m in mats)


    def on_class_changed(self, sender, args):
        cls = self.ClassCombo.SelectedItem
        if not cls:
            return

        self.TypeCombo.ItemsSource = sorted(self.grouped[cls].keys())
        self.TypeCombo.SelectedIndex = -1
        self.ParameterPanel.Children.Clear()

        # Auto-suggest partial name
        self._suggest_name()


    
    def on_type_changed(self, sender, args):
        mat_type = self.TypeCombo.SelectedItem
        if not mat_type:
            return

        cls = self.ClassCombo.SelectedItem
        schema = self.grouped[cls][mat_type]

        self.ParameterPanel.Children.Clear()
        self.parameter_controls = {}

        for param in schema["parameters"]:
            self._add_parameter_row(param)

        # Auto-suggest full name
        self._suggest_name()

    def _suggest_name(self):
        cls = self.ClassCombo.SelectedItem
        mat_type = self.TypeCombo.SelectedItem

        if not cls:
            return

        base = cls
        if mat_type:
            base = f"{cls}_{mat_type}"

        # Ensure uniqueness by adding a counter
        name = base
        counter = 1
        while self._material_exists(name):
            name = f"{base}_{counter:02d}"
            counter += 1

        self.MaterialNameBox.Text = name


    def _add_parameter_row(self, param):
        row = StackPanel()
        row.Margin = (0, 0, 0, 6)

        label = param["name"]
        if param.get("unit"):
            label += " [{}]".format(param["unit"])
        if param.get("required"):
            label += " *"

        row.Children.Add(TextBlock(Text=label))

        tb = TextBox()
        row.Children.Add(tb)

        self.ParameterPanel.Children.Add(row)
        self.parameter_controls[param["name"]] = tb

    def OnOk(self, sender, args):
        cls = self.ClassCombo.SelectedItem
        mat_type = self.TypeCombo.SelectedItem

        if not cls or not mat_type:
            self._message("Please select material class and type.")
            return

        # --- NEW: validate material name ---
        name = self.MaterialNameBox.Text.strip()

        valid, msg = self._is_valid_revit_name(name)
        if not valid:
            self._message(msg)
            return

        if self._material_exists(name):
            self._message("A material named '{}' already exists.".format(name))
            return

    
        schema = self.grouped[cls][mat_type]
        values = {}

        for param in schema["parameters"]:
            name = param["name"]
            text = self.parameter_controls[name].Text.strip()

            if param.get("required") and not text:
                self._message("Parameter '{}' is required.".format(name))
                return

            if text:
                try:
                    values[name] = float(text)
                except ValueError:
                    self._message("Invalid value for '{}'.".format(name))
                    return

        self.material_class = cls
        self.material_type = mat_type
        self.parameter_values = values
        self.material_name = name

        self.DialogResult = True
        self.Close()

    def OnCancel(self, sender, args):
        self.DialogResult = False
        self.Close()

    def _message(self, text):
        from System.Windows import MessageBox
        MessageBox.Show(text)


    def OnMaterialNameChanged(self, sender, args):
        name = self.MaterialNameBox.Text.strip()

        valid, msg = self._is_valid_revit_name(name)
        if not valid:
            self._set_namebox_invalid(msg)
            return

        if self._material_exists(name):
            self._set_namebox_invalid("A material named '{}' already exists.".format(name))
            return

        self._set_namebox_valid()

    def _set_namebox_invalid(self, message):
        from System.Windows.Media import Brushes
        self.MaterialNameBox.BorderBrush = Brushes.Red
        self.MaterialNameBox.ToolTip = message

    def _set_namebox_valid(self):
        from System.Windows.Media import Brushes
        self.MaterialNameBox.BorderBrush = Brushes.Green
        self.MaterialNameBox.ToolTip = None




