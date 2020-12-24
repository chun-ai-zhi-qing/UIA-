# from pyecharts.charts import Bar


# columns = ['衡阳', '长沙', '株洲', '湘潭', '邵阳', '岳阳', '常德', '张家界', '益阳','娄底','郴州','永州','怀化','湘西']
# # #//设置数据
# data1 = [48,242,80,36,102,156,82,5,60,76,39,44,40,8]
# data2 = [5,20,6,5,2,7,6,9,4,3,10,9,4,4]
# #
# #//设置柱状图的主标题与副标题
# bar = Bar()
# #//添加柱状图的数据及配置项
# bar.add("累计感染", columns, data1, mark_line=["average"], mark_point=["max", "min"])
# bar.add("累计死亡", columns, data2, mark_line=["average"], mark_point=["max", "min"])
# #//生成本地文件（默认为.html文件）
# bar.render("柱状图.html")


from pyecharts.charts import Bar
bar = Bar()
bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
#bar.set_series_opts()
bar.add_yaxis("商家A", [5.5, 20, 36, 10, 75, 90])
bar.extend_axis(15)
#bar.add_yaxis("商家B", [5, 20, 36, 10, 75, 90])
#bar.add_yaxis("商家B", [5, 20, 36, 10, 75, 90])
#bar.set_global_opts(opts.TitleOpts(title= "主标题", subtitle = "副标题"))
bar.render()