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

def create_df_of_gpx(gpx:gpxpy.gpx.GPX) -> pd.DataFrame:
    """Creating a dataframe from the loaded gpx file.

    Consisting of the following columns:
    - latitude
    - longitude
    - elevation
    - time

    Args:
        gpx (gpxpy.gpx.GPX): A gpx type

    Returns:
        pd.DataFrame: A dataframe with a row per observation from the gpx file.
    """

    route_info = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                route_info.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time
                })

    route_df = pd.DataFrame(route_info)
    return route_df

if __name__=='__main__':
    gpx = load_data('data/gpx_files/20220705_TMB1.gpx')
    df = create_df_of_gpx(gpx)
    print(df.head())
