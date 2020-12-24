import datetime as dt
import pickle
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
import pandas as pd
import numpy as np
from sklearn import datasets,ensemble
from sklearn.model_selection import train_test_split
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor

import readFile



def modelText():
    with open('model100.pkl', 'rb') as f:
        model = pickle.load(f)
    testSet = pd.read_csv('./Data/test_id_Aug_agg_public5k.csv')
    poiFrom,poiTo = readFile.GetTwoPoiSet()


    #组织数据
    testData = pd.DataFrame()
    testData['Hour'] = testSet['create_hour']
    testData[['estimate_distance','estimate_term','estimate_money']] = 0
    testData['start_geo_id'] = testSet['start_geo_id']
    testData['end_geo_id'] = testSet['end_geo_id']
    testData = testData.merge(poiFrom,on = 'start_geo_id',sort = 'false')
    testData = testData.merge(poiTo,on = 'end_geo_id',sort = 'false')
    testData[['code','temperature','feels_like','pressure','humidity','visibility','wind_direction_degree','wind_speed','wind_scale','weatherCode','windDirectionCode']] = 0
    testData['Date'] = testSet['create_date']
    testData['Date'] = testData ['Date'].map(lambda x:dt.datetime.strptime(x,'%Y-%m-%d'))
    testData['Month'] = testData ['Date'].dt.month
    testData['Day'] = testData ['Date'].dt.day
    
    
    ansSet = pd.DataFrame()
    ansSet[['start_geo_id','end_geo_id','Month','Day','Hour']] = testData[['start_geo_id','end_geo_id','Month','Day','Hour']]

    #删除部分数据，与训练的时候一样
    testData = testData.drop(['Date','start_geo_id','end_geo_id'],axis = 1)
    


    #查看是不是一样的
    testData.to_csv("testData2.csv")
    ans = model.predict(testData.values)

    ansSet['ans'] = ans
    ansSet.to_csv("ans/test_id_Aug_agg_public5kAns100.csv")


if __name__ == "__main__":
    modelText()