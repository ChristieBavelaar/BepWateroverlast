import pandas as pd 
import shapely
from shapely.geometry import Polygon, Point
import ast

def determineTifFile(lat, lon, folder='../../pandafied_data/', file="lat_lon_to_filename.csv"):
    data=pd.read_csv(folder + file)
    point = Point(lon,lat)
    for i in range(len(data['latlon_sw'])):
        sw = ast.literal_eval(str(data['latlon_sw'][i]))
        se = ast.literal_eval(str(data['latlon_se'][i]))
        ne = ast.literal_eval(str(data['latlon_ne'][i]))
        nw = ast.literal_eval(str(data['latlon_nw'][i]))
        polygon = Polygon(((sw[1], sw[0]), (se[1], se[0]), (ne[1], ne[0]), (nw[1], nw[0]), (sw[1], sw[0])))
        if(polygon.contains(point)):
            return data['file_name'][i]

if __name__ == '__main__':
    default = input("Default? y/n")
    if(default == "n"):
        lat=input("Enter lattitude: \n")
        lon=input("Enter longitude: \n")
        print(determineTifFile(lat=lat, lon=lon))
    elif(default == "y"):
        print("snellius:", determineTifFile(lat=52.16944081767487, lon=4.456737798731557))
        print("nieuwe kerk, delft:", determineTifFile(lat=52.01239908847341, lon=4.360902751703506))