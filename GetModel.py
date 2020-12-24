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

#from sklearn import svm
#from sklearn.externals import joblib


def readAllFile():
    groupedSet = pd.read_csv("TablesOfProcessedData/df.csv")
    poiFromSet = pd.read_csv("TablesOfProcessedData/poiFrom.csv")
    poiToSet = pd.read_csv("TablesOfProcessedData/poiTo.csv")
    tmpSet = pd.read_csv("TablesOfProcessedData/tmp.csv")
    weatherSet = pd.read_csv("TablesOfProcessedData/weatherSet.csv")
    

    poiFromSet = poiFromSet.drop('Unnamed: 0',axis = 1)
    poiToSet = poiToSet.drop('Unnamed: 0',axis = 1)
    weatherSet = weatherSet.drop('Unnamed: 0',axis = 1)

    

    #print(groupedSet)
    #print(poiFromSet)
    # print(poiToSet)
    # print(weatherSet)
    # print(tmpSet)
    
    
    return groupedSet,poiFromSet,poiToSet,tmpSet,weatherSet


#合并所有的数据集
def MergeSet():
    groupedSet,poiFromSet,poiToSet,tmpSet,weatherSet = readAllFile()

    tmp = groupedSet[:]
    tmp = tmp.merge(poiFromSet,on = 'start_geo_id')
    tmp = tmp.merge(poiToSet,on = 'end_geo_id')
    tmp = tmp.merge(weatherSet,left_on = ['date','create_hour'],right_on=['date','Hour'])
    
    y = tmp['count']

    tmp ['date'] = tmp ['date'].map(lambda x:dt.datetime.strptime(x,'%Y-%m-%d'))
    tmp ['Month'] = tmp['date'].dt.month
    tmp ['Day'] = tmp['date'].dt.day
    tmp = tmp.drop(['Hour','count','start_geo_id','end_geo_id','date'],axis = 1)
    
    
    #print(y)


    y.to_csv("y.csv")
    tmp.to_csv("tmp.csv")
    return tmp,y
    

#训练后保存模型
def SaveModel():
    tmpX ,tmpY = MergeSet()
    
    #X = tmpX[1:500000]
    #Y = tmpY[1:500000]
    X = tmpX[:]
    Y = tmpY[:]
    
    
    
    start = time.time()
    #决策树：200，随机数400
    #model = RandomForestRegressor(n_estimators=500,random_state=400)
    
    #决策树：800，随机数600
    #model = RandomForestRegressor(n_estimators=800,random_state=600)

    #决策树：1200，随机数600
    model = RandomForestRegressor(n_estimators=1200,random_state=600)
    #决策树：500，随机数1000
    #model = RandomForestClassifier(n_estimators=30,random_state=200)
    
    model = GradientBoostingRegressor( loss='lad',n_estimators=400, max_depth=350, learning_rate=0.1,
			min_samples_leaf=160, min_samples_split=160, random_state=1024)
        # clf = GradientBoostingRegressor(loss='lad', n_estimators=500, max_depth=350, learning_rate=0.05,
		# min_samples_leaf=128, min_samples_split=128, random_state=1024)
        # clf = GradientBoostingRegressor(loss='lad', n_estimators=400, max_depth=350, learning_rate=0.1,
		# 	min_samples_leaf=128, min_samples_split=128, random_state=1024)
    model.fit(X.values,Y.values)
    print("model fit:",time.time() - start)
    
    
    #torch.save(model,"model.pth")
    #joblib.dump(model,"train_model.m")
    with open('model100.pkl', 'wb') as f:
        pickle.dump(model, f)



# def modelText():
#     with open('model5.pkl', 'rb') as f:
#         model = pickle.load(f)
#     testSet = pd.read_csv('.\\Data\\test_id_Aug_agg_public5k.csv')
#     poiFrom,poiTo = readFile.GetTwoPoiSet()


#     #组织数据
#     testData = pd.DataFrame()
#     testData['Hour'] = testSet['create_hour']
#     testData[['estimate_distance','estimate_term','estimate_money']] = 0
#     testData['start_geo_id'] = testSet['start_geo_id']
#     testData['end_geo_id'] = testSet['end_geo_id']
#     testData = testData.merge(poiFrom,on = 'start_geo_id',sort = 'false')
#     testData = testData.merge(poiTo,on = 'end_geo_id',sort = 'false')
#     testData[['code','temperature','feels_like','pressure','humidity','visibility','wind_direction_degree','wind_speed','wind_scale','weatherCode','windDirectionCode']] = 0
#     testData['Date'] = testSet['create_date']
#     testData['Date'] = testData ['Date'].map(lambda x:dt.datetime.strptime(x,'%Y-%m-%d'))
#     testData['Month'] = testData ['Date'].dt.month
#     testData['Day'] = testData ['Date'].dt.day
    
    
#     ansSet = pd.DataFrame()
#     ansSet[['start_geo_id','end_geo_id','Month','Day','Hour']] = testData[['start_geo_id','end_geo_id','Month','Day','Hour']]

#     #删除部分数据，与训练的时候一样
#     testData = testData.drop(['Date','start_geo_id','end_geo_id'],axis = 1)
    


#     #查看是不是一样的
#     testData.to_csv("testData2.csv")
#     ans = model.predict(testData.values)

#     ansSet['ans'] = ans
#     ansSet.to_csv(".\\ans\\test_id_Aug_agg_public5kAns7.csv")





if __name__ == "__main__":
    SaveModel()
    