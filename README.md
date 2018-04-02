# 基于E-Chart的期货数据可视化（K线图）


-------------------------------

## * 简介

基本步骤可参考本人的微文：
https://mp.weixin.qq.com/s?__biz=MzIyMjE5Njk1Mw==&mid=503763782&idx=1&sn=e88cde5499ee7b9041e5cf0d534c8811&scene=19#wechat_redirect

开发环境`Python-v3(3.6)`：

 - pandas==0.20.0
 - numpy==1.13.3+mkl
 - pymongo==3.6.0
 - beautifulsoup4==4.6.0
 - PyQt5

## * 可视化界面(`echart_data_visualization.py`)

 - conn_mongodb函数，连接数据库，返回一个collection
 - extractData函数，返回数据库中特定标签数据，以pandas.DataFrame格式返回
 - InputDataFromMongoDB函数，从数据库中查询并抽取所需数据，以numpy.array的格式返回
 - InputDatabyPd函数，导入外部数据，如果需要导入自定义格式数据，则需要重载这个函数，或者直接在此py上改写即可
 - CheckAnyTimeRangeData函数，将数据转成js列表并保存到txt文件中，存储目录在根目录的data_file文件中
 - CreateHTMLForAnalysis函数，用beautifulsoup4来解析EChart的html模板，并把生成的js列表数据插入模板中，生成新的html文件，存储在data_file文件中
 - comBoxAct、leAct、openDataFile、closeEvent、msg均是一些PyQt的监听与执行函数
 - load函数，即在最终的界面上以网页的形式呈现出K线图

## * 用法

 - 按照https://github.com/DemonDamon/tongdaxin-futures-data-clearing-database-operation 处理好数据并存入数据库；或者重载InputDatabyPd函数，导入自定义的CSV或MAT文件
 - 启动MongoDB，运行该py脚本后，输入必要的参数，如下图所示：
 ![image](https://github.com/DemonDamon/futures-data-visualization-via-EChart/blob/master/model1.jpg)
 ![image](https://github.com/DemonDamon/futures-data-visualization-via-EChart/blob/master/model2.jpg)
