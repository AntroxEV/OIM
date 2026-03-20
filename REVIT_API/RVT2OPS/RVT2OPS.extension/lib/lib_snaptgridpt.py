#! python3
# snap_to_grid.py
from Autodesk.Revit.DB import (
    FilteredElementCollector, Grid, IntersectionResultArray,
    SetComparisonResult, XYZ
)

from Autodesk.Revit.Exceptions import OperationCanceledException

def closest_point_on_curve(curve, point):
    """
    Returns the closest point on a Revit curve to a given XYZ.
    Works for lines, arcs, ellipses, NURBS, etc.
    """
    # Project point onto curve
    result = curve.Project(point)
    if result is None:
        return None
    return result.XYZPoint


def snap_to_closest_grid_point(doc, picked_point):
    """
    Returns the closest point ON ANY GRID CURVE to the picked point.
    """
    grids = FilteredElementCollector(doc).OfClass(Grid).ToElements()
    curves = [g.Curve for g in grids]

    closest_pt = None
    closest_dist = float("inf")

    for curve in curves:
        pt_on_curve = closest_point_on_curve(curve, picked_point)
        if pt_on_curve is None:
            continue

        d = pt_on_curve.DistanceTo(picked_point)
        if d < closest_dist:
            closest_dist = d
            closest_pt = pt_on_curve

    # If no grids exist, return original point
    return closest_pt if closest_pt else picked_point

class GridIntersectionCache(object):
    """
    Computes and caches all grid intersection points in the document.
    Useful when snapping multiple points in a single command.
    """

    def __init__(self, doc):
        self.doc = doc
        self._points = None

    @property
    def points(self):
        if self._points is None:
            self._points = self._compute_intersections()
        return self._points

    def _compute_intersections(self):
        grids = FilteredElementCollector(self.doc).OfClass(Grid).ToElements()
        curves = [g.Curve for g in grids]

        pts = []
        for i in range(len(curves)):
            for j in range(i + 1, len(curves)):
                result = IntersectionResultArray()
                if curves[i].Intersect(curves[j], result) == SetComparisonResult.Overlap:
                    for k in range(result.Size):
                        pts.append(result.get_Item(k).XYZPoint)

        return pts



def snap_to_grid(doc, picked_point, cache=None):
    """
    Returns the nearest grid intersection to the picked point.
    If no cache is provided, intersections are computed on demand.
    """

    if cache is None:
        cache = GridIntersectionCache(doc)

    intersections = cache.points
    if not intersections:
        return picked_point  # no grids in model

    # Find nearest intersection
    nearest = min(intersections, key=lambda p: p.DistanceTo(picked_point))
    return nearest

def pick_point(uidoc, msg="Pick a grid point"):
    '''
    Pick a point safetly using exceptions
    
    :param uidoc: revit uidoc
    :param msg: (optional) message
    '''
    try:
        return uidoc.Selection.PickPoint(msg)
    except OperationCanceledException:
        return None