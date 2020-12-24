# from pyecharts.charts import Bar
# bar = Bar()
# bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
# #bar.set_series_opts()
# bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# bar.extend_axis(15)
# #bar.add_yaxis("商家B", [5, 20, 36, 10, 75, 90])
# #bar.add_yaxis("商家B", [5, 20, 36, 10, 75, 90])
# #bar.set_global_opts(opts.TitleOpts(title= "主标题", subtitle = "副标题"))
# bar.render()



import pandas as pd
#空格为分隔符
df=pd.read_csv('ans/test_id_Aug_agg_public5kAns7.csv')
#以年级为分组依据
grade=list(set(df['start_geo_id']))
#不保留行索引,index=0;不保存列名header=0,以空格间隔字段输出
df = df.drop(['Unnamed: 0'],axis = 1)

print(df)

t = 1
for g in grade:
    df[df['start_geo_id']==g].to_csv('D/'+ str(t) +'.csv')
    t = t + 1