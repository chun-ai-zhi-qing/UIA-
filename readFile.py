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



#读取文件,这个数据一律不可以操作，易出错


#处理poi数据集得到两个地址
def GetTwoPoiSet():
    print("GetTwoPoiSet start")
    start = time.time()

    #读取文件
    poi = pd.read_csv('Data/poi.csv',encoding = 'ansi', header=None, names = list(range(21)))
    
    #拷贝文件
    tmp = poi[:]
    tmp = tmp.drop([1,3,5,7,9,11,13,15,17,19],axis = 1)

    #复制到poiFrom,poiTo
    poiFrom = tmp[:]
    poiTo = tmp[:]

    #命名
    poiFrom.columns = ['start_geo_id','Foil','Fmarket','Fuptown','Fsubway','Fbus','Fcaffee','Fchinese','Fatm','Foffice','Fhotel']
    poiTo.columns = ['end_geo_id','Toil','Tmarket','Tuptown','Tsubway','Tbus','Tcaffee','Tchinese','Tatm','Toffice','Thotel']

    #输出
    poiFrom.to_csv("TablesOfProcessedData/poiFrom.csv")
    poiTo.to_csv("TablesOfProcessedData/poiTo.csv")
    
    #计算时间
    print("Getting Two PoiSet:",time.time() - start)
    return poiFrom,poiTo




def GetWeatherSet():
    print("Get weatherSet start")
    start = time.time()
    weatherSet = pd.read_csv('Data/weather.csv',encoding = 'utf-8')
    #临时转化时间之后删除
    weatherSet ['date'] = weatherSet ['date'].map(lambda x:dt.datetime.strptime(x,'%Y-%m-%d %H:%M'))
    
    #数据集里面天气，风向只有八个,转换一下，方便之后转换float
    weatherSet['weatherCode'] = weatherSet['text'].map({'晴':8,'多云':7,'阴':6,'阵雨':5,'雷阵雨':4,'小雨':3,'中雨':2,'大雨':1})
    weatherSet['windDirectionCode'] = weatherSet['wind_direction'].map({'南':8,'西南':7,'西':6,'东南':5,'西北':4,'北':3,'东':2,'东北':1})
    

    #需要对时间进行特殊处理:月份,日期,以半小时的天气做为这个时间的天气
    #weatherSet['Month'] = weatherSet['date'].dt.month
    #weatherSet['Day'] = weatherSet['date'].dt.day
    weatherSet['Hour'] = weatherSet[weatherSet['date'].dt.minute==30]['date'].dt.hour
    weatherSet['date'] = weatherSet['date'].dt.date


    #除去部分数据
    weatherSet=weatherSet.dropna()

    #先转换为int,方便对接表格
    weatherSet['Hour'] = weatherSet['Hour'].map(lambda x:int(float(x)))


    #删除部分数据
    weatherSet = weatherSet.drop(['text','wind_direction'],axis = 1)
    weatherSet.to_csv("TablesOfProcessedData/weatherSet.csv")

    #输出
    print("Getting weatherSet:",time.time() - start)
    #print(weatherSet)
    #print(weatherSet.values)
    
    return weatherSet






def GetBaseSet():
    start = time.time()
    
    #读取文件合并
    july= pd.read_csv('Data/train_July.csv')
    aug = pd.read_csv('Data/train_Aug.csv')
    tmpSet=pd.concat([july,aug])
    tmpSet['date'] = tmpSet['create_date'].map(lambda x:dt.datetime.strptime(x,'%Y-%m-%d'))
    tmpSet['date'] = tmpSet['date'].dt.date
    #tmpSet['Month'] = tmpSet['date'].dt.month
    #tmpSet['Day'] = tmpSet['date'].dt.day

    #添加统计行
    tmpSet['count'] = 1
    df = tmpSet.groupby(['start_geo_id','end_geo_id','create_hour','date'])[['count','estimate_distance','estimate_term','estimate_money']].sum()
    df['estimate_distance'] = df['estimate_distance'] / df['count']
    df['estimate_term'] = df['estimate_term'] / df['count']
    df['estimate_money'] = df['estimate_money'] / df['count']
    #df['testid'] = df['start_geo_id']
    


    #输出
    #print(tmpSet)
    #print(df)
    df.to_csv("TablesOfProcessedData/df.csv")
    #print(df['start_geo_id'])
    
    print("Getting BaseSet:",time.time() - start)
    return tmpSet


#表格合并,废弃了，没用
def AllSetToCSV():
    start = time.time()
    
    #四个数据集
    poiFromSet,poiToSet = GetTwoPoiSet()
    weatherSet = GetWeatherSet()
    baseSet = GetBaseSet()

    #拼接有问题，思考其他拼接方式
    #baseSet.to_csv("baseSet.csv")
    #tainSet = pd.concat([baseSet, weatherSet], axis=1, join='inner', sort=True)
    #tainSet = baseSet.merge(poiToSet,on = 'end_geo_id',how = 'left')
    #baseSet = baseSet.merge(poiFromSet,on = 'start_geo_id')
    #tainSet.to_csv("tainSet.csv")
    #tainSet = baseSet.merge(weatherSet,left_on = ['date'],right_on=['Date'])
    #tainSet.to_csv("tainSet.csv")

    # tainSet = pd.DataFrame()
    # tainSet.


    tmp = baseSet[:]
    tmp = tmp.merge(poiFromSet,on='start_geo_id')
    print("poiFromSet merge:",time.time() - start)


    tmp = tmp.merge(poiToSet,on='end_geo_id')
    print("poiToSet merge:",time.time() - start)
    
    #时间合并
    #tmp = tmp.merge(weatherSet,left_on = ['Date','create_hour'],right_on=['Date','Hour'])
    print("weatherSet merge:",time.time() - start)
    #tmp = tmp.merge(weatherSet,left_on = ['Month','Day','create_hour'],right_on=['Month','Day','Hour'])
    
    #冗余数据查看
    #tmp.to_csv("Pretmp.csv")
    
    #删除部分数据
    #tmp = tmp.drop(['id','driver_id','member_id','create_hour','status','date'],axis = 1)
    #print(tmp[0])
    tmp.to_csv("TablesOfProcessedData/tmp.csv")

    print("Getting AllSetToCSV:",time.time() - start)





#调用之后生成文件到一个文件里面，主要还是出来东西
if __name__ == "__main__":
    AllSetToCSV()