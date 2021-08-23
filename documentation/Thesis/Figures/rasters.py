import pandas as pd
import matplotlib.pyplot as plt
import ast
import shapely
from shapely.geometry import Polygon,Point
import geopandas as gpd

def plotRasters(radar, twitterCoords, tiff):
    print(len(radar['latlon_sw']))
    for i in range(len(radar['latlon_sw'])):
        sw = ast.literal_eval(str(radar['latlon_sw'][i]))
        se = ast.literal_eval(str(radar['latlon_se'][i]))
        ne = ast.literal_eval(str(radar['latlon_ne'][i]))
        nw = ast.literal_eval(str(radar['latlon_nw'][i]))
        if radar['radarX'][i] == 429.0 and radar['radarY'][i] == 420.0:
            print("found it")
            polygon = Polygon(((sw[1], sw[0]), (se[1], se[0]), (ne[1], ne[0]), (nw[1], nw[0]), (sw[1], sw[0])))
            # p = gpd.GeoSeries(polygon)
            # p.plot()
            #fig, axs = plt.subplots()
            x, y = polygon.exterior.xy
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(x, y, color='#6699cc', alpha=0.7,
            linewidth=3, solid_capstyle='round', zorder=2)
            plt.show()
       
        # sw1 = ast.literal_eval(str(tiff['latlon_sw'][i]))
        # se1 = ast.literal_eval(str(tiff['latlon_se'][i]))
        # ne1 = ast.literal_eval(str(tiff['latlon_ne'][i]))
        # nw1 = ast.literal_eval(str(tiff['latlon_nw'][i]))
        # if tiff['file_name'][i] == 'ahn2_5_33dn2.tif':
        #     print("found it")
        #     polygon1 = Polygon(((sw[1], sw[0]), (se[1], se[0]), (ne[1], ne[0]), (nw[1], nw[0]), (sw[1], sw[0])))
        #     # p = gpd.GeoSeries(polygon)
        #     # p.plot()
        

        #fig, axs = plt.subplots()
        # ax = fig.add_subplot(111)
        # ax.plot(x, y, color='#6699cc', alpha=0.7,
        # linewidth=3, solid_capstyle='round', zorder=2)
        # axs.fill([sw[1], sw[0], se[1], se[0]], [ne[1], ne[0], nw[1], nw[0]], alpha=.25, fc='r', ec='none')
        # axs.fill([sw1[1], sw1[0], se1[1], se1[0]], [ne1[1], ne1[0], nw1[1], nw1[0]], fc='r', ec='none')
        plt.autoscale()
        

if __name__ == '__main__':
    radar = pd.read_csv("../../pandafied_data/pandafied_h5_radar.csv")
    tiff = pd.read_csv("../../pandafied_data/lat_lon_to_filename.csv")

    print(radar)
    #radar=radar[radar['radarX'] == 429.0]
    #radar=radar[radar['radarY'] == 420.0]
    print(radar)
    plotRasters(radar,0,tiff)
    
