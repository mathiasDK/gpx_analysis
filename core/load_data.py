import pandas as pd
import numpy as np
import gpxpy
import gpxpy.gpx

def load_data(file_path: str) -> gpxpy.gpx.GPX:
    """
    Loading the gpx file and returning a gpxpy.gpx.GPX object

    Args:
        file_path (str): the path to the file

    Returns:
        gpxpy.gpx.GPX: se gpxpy documentation
    """
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    return gpx


if __name__=='__main__':
    gpx = load_data('data/gpx_files/20220705_TMB1.gpx')
    print(gpx.get_track_points_no())
    print(gpx.get_elevation_extremes())
    print(gpx.get_uphill_downhill())

    print(type(gpx))