import haversine as hs
import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    distance = hs.haversine(
        point1=(lat1, lon1),
        point2=(lat2, lon2),
        unit=hs.Unit.METERS
    )
    return np.round(distance, 2)

def distance_calculator_dataframe(df, lat_col, lon_col):
    distances=[]
    for i in range(len(df)):
        if i==0:
            dist = 0
        else:
            dist=haversine_distance(
                lat1=df.iloc[i-1][lat_col], 
                lon1=df.iloc[i-1][lon_col], 
                lat2=df.iloc[i][lat_col], 
                lon2=df.iloc[i][lon_col]
            )
        distances.append(dist)
    return distances
