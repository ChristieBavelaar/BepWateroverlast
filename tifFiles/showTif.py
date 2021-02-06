from osgeo import gdal
import matplotlib.pyplot as plt
import sys

def showimage(filename):
    filepath = '../../AHN2_5m/' + str(filename)
    print(filepath)
    dataset = gdal.Open(filepath, gdal.GA_ReadOnly) # Note GetRasterBand() takes band no. starting from 1 not 0
    band = dataset.GetRasterBand(1)
    arr = band.ReadAsArray()
    print('dataset')
    print(dataset)
    print('band')
    print(band)
    print('arr')
    print(arr)
    print('length: '+ str(len(arr)))
    plt.imshow(arr)
    plt.show()
	
def readFile(filename):
    filehandle = gdal.Open(filename)
    band1 = filehandle.GetRasterBand(1)
    geotransform = filehandle.GetGeoTransform()
    geoproj = filehandle.GetProjection()
    band1data = band1.ReadAsArray()
    xsize = filehandle.RasterXSize
    ysize = filehandle.RasterYSize
    print( xsize,ysize)


if __name__ == '__main__':
    #readFile('../../AHN2_5m/' + str(sys.argv[1]))
    showimage(sys.argv[1])
