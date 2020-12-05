from osgeo import gdal
import matplotlib.pyplot as plt
import sys

filepath = '../../AHN2_5m/' + str(sys.argv[1])
print(filepath)
dataset = gdal.Open(filepath, gdal.GA_ReadOnly) # Note GetRasterBand() takes band no. starting from 1 not 0
band = dataset.GetRasterBand(1)
arr = band.ReadAsArray()
plt.imshow(arr)
plt.show()
