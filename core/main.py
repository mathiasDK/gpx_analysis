from plot import plot
from calc import distance_calculator_dataframe
from load_data import load_data, create_df_of_gpx
from os import listdir

def main():
    for day, file_name in enumerate(listdir('./data/gpx_files/')):
        file_path = 'data/gpx_files/' + file_name
        gpx = load_data(file_path)
        df = create_df_of_gpx(gpx)

        df['distance'] = distance_calculator_dataframe(df, 'latitude', 'longitude')
        df['acc_distance_km'] = df['distance'].cumsum() / 1000.

        plot(show_fig=True).continuous(
            df.acc_distance_km.tolist(), 
            df.elevation.tolist(), 
            end_annotation=True,
            title=f'Dag {day+1}',
            x_title='Km',
            y_title='Højde'
        )

if __name__=='__main__':
    main()