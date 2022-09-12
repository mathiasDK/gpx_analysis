from plot import plot
from calc import distance_calculator_dataframe
from load_data import load_data, create_df_of_gpx
from os import listdir
import json

def main():
    route_desc = json.load(open('data/route/route_names.json'))
    for day, file_name in enumerate(listdir('./data/gpx_files/')):
        file_path = 'data/gpx_files/' + file_name
        gpx = load_data(file_path)
        df = create_df_of_gpx(gpx)

        df['distance'] = distance_calculator_dataframe(df, 'latitude', 'longitude')
        df['acc_distance_km'] = df['distance'].cumsum() / 1000.
        df['height_change'] = df['elevation'] - df['elevation'].shift(-1)

        start_city = route_desc['route_description'][day]['start']
        end_city = route_desc['route_description'][day]['end']
        meters_up = round(sum(df[df['height_change']>0]['height_change']), 0)
        meters_down = round(sum(df[df['height_change']<0]['height_change']), 0)*-1.

        plot(show_fig=True).continuous(
            df.acc_distance_km.tolist(), 
            df.elevation.tolist(), 
            end_annotation=True,
            title=f'Dag {day+1}<br>{start_city} - {end_city}',
            x_title='Km',
            y_title='Højde'
        )

if __name__=='__main__':
    main()