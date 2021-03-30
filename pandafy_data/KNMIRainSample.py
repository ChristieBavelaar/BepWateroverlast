import h5py
from os import listdir
from os.path import isfile, join
import pandas as pd
from pyproj import CRS, Transformer
import sys
from tqdm import tqdm
from joblib import Parallel, delayed
import multiprocessing
import numpy as np

def parallel_data_parsing(subfolder,folder,year_counter,total_year,subfolder_counter,subfolder_total):
    data = {}
    data['rain'] = []
    data['radarX'] = []
    data['radarY'] = []
    data['date'] = []
    #data['start_time'] = []
    #data['stop_time'] = []
    data = pd.DataFrame(data)
    print("subfolder no.: " +str(subfolder))
    onlyfiles = [f for f in listdir(folder+subfolder) if isfile(join(folder+subfolder, f))]
    h5_files = [f for f in onlyfiles if '.h5' in f]
    h5_files.sort()
    sum_data = {}
    sum_data['rain'] = []
    sum_data['radarX'] = []
    sum_data['radarY'] = []
    sum_data['date'] = []
    sum_data = pd.DataFrame(sum_data)
    print(len(h5_files))
    for filename_idx in range(len(h5_files)):
        temp_date = h5_files[filename_idx][22:30]
        temp_time = h5_files[filename_idx][30:34]
        print("year: ",year_counter," / ",total_year," subfolder: ", subfolder_counter, " / ",subfolder_total, " file: ",filename_idx," / ", len(h5_files))
        with h5py.File(folder+subfolder+h5_files[filename_idx], 'r') as f:
            img = np.array(list(f['image1/image_data']))
            len_y,len_x = img.shape
            local_data = {}
            local_data['rain']= img.flatten().tolist()
            local_data['radarY'] = [i for i in range(len_y) for j in range(len_x)]
            local_data['radarX'] = [i for i in range(len_x)]*len_y
            local_data['date']= [temp_date]*len_x*len_y
            local_data = pd.DataFrame(local_data)
            local_data = local_data[local_data.rain < 65535]
            sum_data = sum_data.append(local_data,sort=False)
            #for i, row in enumerate(img):
            #    for j, num  in enumerate(row):
            #        if num < 65535:
            #            local_data = {}
            #            local_data['rain']=num
            #            local_data['radarX']=[j]
            #            local_data['radarY']=[i]
            #            local_data['date']= [temp_date]
            #            local_data = pd.DataFrame(local_data)
            #            sum_data = sum_data.append(local_data,sort=False)
        if temp_time == '2400':
            sum_data = sum_data.groupby(['date','radarX','radarY'])['rain'].sum().reset_index(name='rain')
            data = data.append(sum_data,sort=False)
            sum_data = {}
            sum_data['rain'] = []
            sum_data['radarX'] = []
            sum_data['radarY'] = []
            sum_data['date'] = []
            sum_data = pd.DataFrame(sum_data)
    return data

def pandafy_h5(save_name_radar='/home/s2155435/pandafied_data/pandafied_h5_radar.csv',save_name_rain='/home/s2155435/pandafied_data/pandafied_h5_rain_2017_12.csv',folder = '/home/s2155435/KNMI/'):
    '''
        This function reads the KNMI precipitation data, aggregates it by summing up the amount of rain per day, it puts it into a pandas dataframe and saves it to disk.
    '''
    results = []
    year_counter = 2017
    total_year = 1
    
    super_folder = folder+ 'RADNL_CLIM____MFBSNL25_01H_20170101T000000_20180101T000000_0002/RAD_NL25_RAC_MFBS_01H/' + str(year_counter) +'/'
    month_folders = ['12']
    month_folders.sort()
    for i in range(len(month_folders)):
        month_folders[i] += '/'
        print(month_folders[i])
    num_cores = multiprocessing.cpu_count()
    print("num_cores: " + str(num_cores))

    results.append(Parallel(n_jobs=num_cores)(delayed(parallel_data_parsing)(month_folders[i],super_folder,year_counter,total_year,i,len(month_folders)) for i in range(len(month_folders))))
    
    data = {}
    data['rain'] = []
    data['radarX'] = []
    data['radarY'] = []
    data['date'] = []
    data = pd.DataFrame(data)
    
    print("len(results)")
    for result in results:
        print(len(result))
    print("len(d.index)")
    for result in results:
        for d in result:
            print(len(d.index))
            data = data.append(d,sort=False)
    print(data[(data.radarX==442.0) & (data.radarY==251.0)])
    print(5)
    print(len(data.index))
    print(data)
    print("len index: ",len(data.index))
    print(6)
    data.to_csv(save_name_rain,index=False)
    print(7)
    return data

if __name__ == '__main__':
    pandafy_h5()
