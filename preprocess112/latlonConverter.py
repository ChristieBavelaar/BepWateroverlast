import math
class Converter:
    RDOriginX = 155E3
    RDOriginY = 463E3
    GpsOriginLat = 52.1551744
    GpsOriginLon = 5.38720621
    def __init__(self):
        self.lat = []
        self.lon = []
        for i in range(0,11):
            self.lat.insert(i, [])
            self.lon.insert(i, [])
            self.lon.insert(i+1,[])

        ## Latitude calculation
        self.lat[0] = [0,1,3235.65389]
        self.lat[1] = [2,0,-32.58297]
        self.lat[2] = [0,2,-0.2475]
        self.lat[3] = [2,1,-0.84978]
        self.lat[4] = [0,3,-0.0665]
        self.lat[5] = [2,2,-0.01709]
        self.lat[6] = [1,0,-0.00738]
        self.lat[7] = [4,0,0.0053]
        self.lat[8] = [2,3,-3.9E-4]
        self.lat[9] = [4,1,3.3E-4]
        self.lat[10] = [1,1,-1.2E-4]
        
        ## Longitude calculation
        self.lon[0] = [1,0,5260.52916]
        self.lon[1] = [1,1,105.94684]
        self.lon[2] = [1,2,2.45656]
        self.lon[3] = [3,0,-0.81885]
        self.lon[4] = [1,3,0.05594]
        self.lon[5] = [3,1,-0.05607]
        self.lon[6] = [0,1,0.01199]
        self.lon[7] = [3,2,-0.00256]
        self.lon[8] = [1,4,0.00128]
        self.lon[9] = [0,0,2.2E-4]
        self.lon[10] = [2,0,-2.2E-4]
        self.lon[11] = [5,0,2.6E-4]

    def toLat(self,rdX,rdY):
        a = 0
        dX = 1E-5 * (rdX - self.RDOriginX)
        dY = 1E-5 * (rdY - self.RDOriginY)

        for i in range(0,11):
            a = a + ( self.lat[i][2] * math.pow(dX, self.lat[i][0]) * math.pow(dY, self.lat[i][1]) )

        return round(self.GpsOriginLat + ( a / 3600 ), 9)

    def toLon(self,rdX,rdY):
        a = 0
        dX = 1E-5 * (rdX - self.RDOriginX)
        dY = 1E-5 * (rdY - self.RDOriginY)
        
        for i in range(0,12):
            a = a + ( self.lon[i][2] * math.pow(dX,self.lon[i][0]) * math.pow(dY, self.lon[i][1]) )

        return round(self.GpsOriginLon + ( a / 3600 ), 9)