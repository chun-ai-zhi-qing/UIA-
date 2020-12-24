from pyecharts.charts import Bar
import pandas as pd
from pyecharts import options as opts
for i in range(1 , 258):
    df = pd.read_csv('D/'+str(i)+'.csv')
    sizeNum = df.iloc[:,0].size
    #print(sizeNum)
    t = 1
    row = []
    col = []
    for j in range(0 , sizeNum):
        row.append(df['end_geo_id'][j])
        #row.append(str(j))
        col.append(df['ans'][j])
        # if j%10==0 or j==sizeNum-1:
        #     bar = (
        #         Bar()
        #         #.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)))
        #     )
        #     bar.add_xaxis(row)
        #     bar.add_yaxis("people",col)
        #     # print(col)
        #     # print(row)
        #     bar.render("Ps/"+str(i)+"_Bar_From"+str(t)+"To"+str(j)+".html")
        #     t = j
        #     row = []
        #     col = []
    bar = (Bar()
        .add_xaxis(row)
        .add_yaxis("people", col)
        .set_global_opts(title_opts=opts.TitleOpts(title="区域缩放柱状图"),
                     datazoom_opts=opts.DataZoomOpts(type_="slider"),
                    )
    )
    bar.render("Bar/"+str(i)+".html")