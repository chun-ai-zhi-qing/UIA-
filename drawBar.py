from pyecharts.charts import Bar
import pandas as pd
t = 1
# df = pd.read_csv('D/'+str(i)+'.csv')
# # print(df['end_geo_id'][1])
# # print(df['ans'][1])
# bar = Bar()
# bar.add_xaxis([df['end_geo_id'][0],df['end_geo_id'][1]])

# bar.add_yaxis("people",[df['ans'][0],df['ans'][1]])
# bar.render()
for i in range(1,4):
    # print(str(i))
    df = pd.read_csv('D/'+str(i)+'.csv')
    # print (df.iloc[:,0].size)
    # print(1)
    bar = Bar()
    bar.add_xaxis([df['end_geo_id'].values])
    bar.add_yaxis("people",[df['ans'].values])
    # for j in range(1,df.iloc[:,0].size):
    #     print(df['end_geo_id'].values)
        # if j%10 == 0:
    bar.render("S/"+str(i)+"_表格图.html")
        #     bar = Bar()
        
    