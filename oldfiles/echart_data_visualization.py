import os, sys
from sys import path  
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Form import Ui_Damon   
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
import numpy as np

class mywindow(QtWidgets.QWidget,Ui_Damon):    
    def __init__(self):
        if not os.path.exists(os.getcwd() + '/' + 'data_file'):
            os.makedirs(os.getcwd() + '/' + 'data_file')
        self.savepath = os.getcwd() + '/' + 'data_file'
        super(mywindow,self).__init__()    
        self.setupUi(self)
        self.BrowseB1.clicked.connect(self.openDataFile)
        self.comboBox.addItem('1M') #1mins
        self.comboBox.addItem('5M') #5mins
        self.comboBox.addItem('D') #Day
        self.comboBox_3.addItem('model1')
        self.comboBox_3.addItem('model2')
        self.comboBox.currentIndexChanged.connect(self.comBoxAct)
        self.comboBox_3.currentIndexChanged.connect(self.comBoxAct)
        self.pushButton.clicked.connect(self.CreateHTMLFile)
        self.dp_le.textChanged.connect(self.leAct) #csv/mat数据路径
        self.ed_le_2.textChanged.connect(self.leAct) #起始日期
        self.ed_le.textChanged.connect(self.leAct) #结束日期
        self.st_le.textChanged.connect(self.leAct) #起始时间
        self.et_le.textChanged.connect(self.leAct) #结束时间
        self.ed_le_3.textChanged.connect(self.leAct) #mongodb期货品种名称
        self.ed_le_4.textChanged.connect(self.leAct) #IP
        self.ed_le_5.textChanged.connect(self.leAct) #PORT
        self.ed_le_6.textChanged.connect(self.leAct) #database name
        self.datapath = ''
        self.startDate = 0
        self.endDate = 0
        self.startTime = 0
        self.endTime = 0
        self.modelType = self.comboBox_3.currentText()
        self.dataFrame = self.comboBox.currentText()
        self.savename = ''
        self.symbolName = ''
        self.setWindowTitle('Demon Chart')

    def conn_mongodb(self,collectionName):
        self._Conn = MongoClient(self._IP, self._PORT) #localhost 27017
        self._mydb = self._Conn[self._databasename]
        collection = self._mydb.get_collection(collectionName)
        return collection

    def extractData(self,collection,tag_list):
        data = []
        Dict = {}
        for tag in tag_list:
            exec(tag + " = collection.distinct('" + tag + "')")
            exec("data.append(" + tag + ")")
            exec("Dict.update({'" + tag + "' : np.array(" + tag + ")})")
        dataFrame = pd.DataFrame(Dict,columns=tag_list)
        return dataFrame

    def InputDataFromMongoDB(self):
        try:
            collection = self.conn_mongodb(self.symbolName) 
        except Exception as e:
            if self._IP == '':
                self.msg("conn_mongodb Error","请输入IP地址！")
            if self._PORT == '':
                self.msg("conn_mongodb Error","请输入端口号！")
            if self._databasename == '':
                self.msg("conn_mongodb Error","请输入数据库名称！")
            if self._IP != '' and self._PORT != '' and self._databasename != '':
                self.msg("conn_mongodb Error","IP、端口号或数据库名称输入有误，请重新输入！")
        cursor_start = [int(cursor['_id']) for cursor in collection.find({"Date":str(self.startDate),"Time":str(self.startTime)})][0]
        cursor_end = [int(cursor['_id']) for cursor in collection.find({"Date":str(self.endDate),"Time":str(self.endTime)})][0]
        idLst = self.extractData(collection,['_id'])._id
        Date = []; Time = []; Open = []; High = []; Low = []; Close = []; Volumn = []
        while cursor_start <= cursor_end:
            Date.append(int(collection.find_one({'_id':str(cursor_start)})['Date']))
            Time.append(int(collection.find_one({'_id':str(cursor_start)})['Time']))
            Open.append(collection.find_one({'_id':str(cursor_start)})['Open'])
            High.append(collection.find_one({'_id':str(cursor_start)})['High'])
            Low.append(collection.find_one({'_id':str(cursor_start)})['Low'])
            Close.append(collection.find_one({'_id':str(cursor_start)})['Close'])
            Volumn.append(collection.find_one({'_id':str(cursor_start)})['Volumn'])
            cursor_start += 1
        date = np.array(Date)
        time = np.array(Time)
        Open = np.double(Open)
        High = np.double(High)
        Low = np.double(Low)
        Close = np.double(Close)
        Volumn = np.double(Volumn)
        date_day = []; Open_day = []; High_day = []; 
        Low_day = []; Close_day = []; Volumn_day = []
        idx = 0
        for i in range(1,len(date)):
            if time[i-1] == 1500:
               date_day.append(date[i-1])
               Open_day.append(Open[idx])
               High_day.append(np.max(High[idx:i]))
               Low_day.append(np.min(Low[idx:i]))
               Close_day.append(Close[i-1])
               Volumn_day.append(np.sum(Volumn[idx:i]))
               idx = i
            if i == len(time) - 1:
               date_day.append(date[-1])
               Open_day.append(Open[idx])
               High_day.append(np.max(High[idx:]))
               Low_day.append(np.min(Low[idx:]))
               Close_day.append(Close[i])
               Volumn_day.append(np.sum(Volumn[idx:]))
        date_day = np.array(date_day)
        Open_day = np.array(Open_day)
        High_day = np.array(High_day)
        Low_day = np.array(Low_day)
        Close_day = np.array(Close_day)
        Volumn_day = np.array(Volumn_day)   
        return date,time,Open,High,Low,Close,Volumn,date_day,Open_day,\
        High_day,Low_day,Close_day,Volumn_day

    def InputDatabyPd(self):
        import pandas as pd
        import numpy as np
        data = pd.read_csv(self.datapath)
        data_processed = data.loc[:,['time','open','high','low','close','volume']]
        start_idx = 0
        date = []; open_day = []; high_day = []
        low_day = []; close_day = []; vol_day = []
        for i in range(len(data_processed)):
            if str(data_processed.time[i])[8:12] == '1500':
                date.append(int(str(data_processed.time[i])[0:8]))
                open_day.append(data_processed.open[start_idx])
                high_day.append(np.max(data_processed.high[start_idx:i+1]))
                low_day.append(np.min(data_processed.low[start_idx:i+1]))
                close_day.append(data_processed.close[i])
                vol_day.append(np.sum(data_processed.volume[start_idx:i+1]))
                start_idx = i + 1
        data_day = pd.DataFrame({'date' : np.array(date),
                                 'open' : np.array(open_day),
                                 'high' : np.array(high_day),
                                 'low' : np.array(low_day),
                                 'close' : np.array(close_day),
                                 'volume' : np.array(vol_day)},
                                 columns = ['date','open','high','low','close','volume'])
        date_day = np.array(data_day.date)
        Open_day = np.double(data_day.open)
        High_day = np.double(data_day.high)
        Low_day = np.double(data_day.low)
        Close_day = np.double(data_day.close)
        Volumn_day = np.array(data_day.volume) 
        date = pd.DataFrame([int(str(data_processed.time[i])[0:8]) for i in range(len(data_processed))])
        time = pd.DataFrame([int(str(data_processed.time[i])[8:12]) for i in range(len(data_processed))])
        del data_processed['time']
        data_processed.insert(0,'date',date)
        data_processed.insert(1,'time',time)
        date = np.array(data_processed.date)
        time = np.array(data_processed.time)
        Open = np.double(data_processed.open)
        High = np.double(data_processed.high)
        Low = np.double(data_processed.low)
        Close = np.double(data_processed.close)
        Volume = np.array(data_processed.volume)
        return date,time,Open,High,Low,Close,Volume,\
        date_day,Open_day,High_day,Low_day,Close_day,Volumn_day

    def CheckAnyTimeRangeData(self):
        import numpy as np
        if self.symbolName != '':
            try:
                date,time,Open,High,Low,Close,Volumn,\
                date_day,Open_day,High_day,Low_day,Close_day,Volumn_day = self.InputDataFromMongoDB() 
            except Exception as e:
                self.msg("CheckAnyTimeRangeData Error","数据库中不存在该期货品种价量数据!")
        elif self.datapath != '' and self.symbolName == '':
            try:
                date,time,Open,High,Low,Close,Volumn,\
                date_day,Open_day,High_day,Low_day,Close_day,Volumn_day = self.InputDatabyPd() 
            except Exception as e:
                self.msg("CheckAnyTimeRangeData Error","数据路径不存在或数据文件内部格式不对!")
        else:
            self.msg("CheckAnyTimeRangeData","请输入数据源信息!")
        if self.dataFrame == '1M' or self.dataFrame == '5M':
            if self.startTime == 0 and self.endTime == 0:
                startIdx = np.where(date == self.startDate)[0][0]
                endIdx = np.where(date == self.endDate)[0][-1]
            else:
                startIdx = np.where(date == self.startDate)[0]
                startIdx = startIdx[np.where(time[startIdx] == self.startTime)[0][0]]
                endIdx = np.where(date == self.endDate)[0]
                endIdx = endIdx[np.where(time[endIdx] == self.endTime)[0][0]]
            dataK = []
            dateS = []
            DataforJS = []
            if self.modelType == 'model1':
                for i in range(startIdx,endIdx+1):
                    dateS.append(str(date[i])[0:4] + '/' + str(date[i])[4:6] + '/' + str(date[i])[6:]\
                    + ' ' + str(time[i])[:-2] + ':' + str(time[i])[-2:])
                    dataK.append([Open[i],Close[i],Low[i],High[i]])
                    DataforJS.append([dateS[-1],Open[i],Close[i],Low[i],High[i]])
                Path = self.savepath + '/' + self.savename + '(' + self.dataFrame + ').txt'
                with open(Path,'w') as f:
                    for i in range(len(DataforJS)):
                        f.write("['" + DataforJS[i][0] + "'," + \
                        str(DataforJS[i][1]) + ',' + str(DataforJS[i][2]) + ',' + \
                        str(DataforJS[i][3]) + ',' + str(DataforJS[i][4]) + '],' + '\n')
                        if i == len(DataforJS) - 1:
                            f.write("['" + DataforJS[i][0] + "'," + \
                            str(DataforJS[i][1]) + ',' + str(DataforJS[i][3]) + ',' + \
                            str(DataforJS[i][3]) + ',' + str(DataforJS[i][4]) + ']' + '\n')
            elif self.modelType == 'model2':
                for i in range(startIdx,endIdx+1):
                    dateS.append(str(date[i])[0:4] + '/' + str(date[i])[4:6] + '/' + str(date[i])[6:]\
                    + ' ' + str(time[i])[:-2] + ':' + str(time[i])[-2:])
                    dataK.append([Open[i],Close[i],Low[i],High[i],Volumn[i]])
                    DataforJS.append([dateS[-1],Open[i],Close[i],Low[i],High[i],Volumn[i]])
                Path = self.savepath + '/' + self.savename + '(' + self.dataFrame + ').txt'
                with open(Path,'w') as f:
                    for i in range(len(DataforJS)):
                        f.write("['" + DataforJS[i][0] + "'," + \
                        str(DataforJS[i][1]) + ',' + str(DataforJS[i][2]) + ',' + \
                        str(DataforJS[i][3]) + ',' + str(DataforJS[i][4]) + ',' + str(DataforJS[i][5]) + '],' + '\n')
                        if i == len(DataforJS) - 1:
                            f.write("['" + DataforJS[i][0] + "'," + \
                            str(DataforJS[i][1]) + ',' + str(DataforJS[i][3]) + ',' + \
                            str(DataforJS[i][3]) + ',' + str(DataforJS[i][4]) + ',' + str(DataforJS[i][5]) + ']' + '\n')                
        elif self.dataFrame == 'D':
            startIdx = np.where(date_day == self.startDate)[0][0]
            endIdx = np.where(date_day == self.endDate)[0][-1]
            dataK = []
            dateS = []
            DataforJS = []
            if self.modelType == 'model1':
                for i in range(startIdx,endIdx+1):
                    dateS.append(str(date_day[i])[0:4] + '/' + str(date_day[i])[4:6] + '/' + str(date_day[i])[6:])
                    dataK.append([Open_day[i],Close_day[i],Low_day[i],High_day[i]])
                    DataforJS.append([dateS[-1],Open_day[i],Close_day[i],Low_day[i],High_day[i]])
                Path = self.savepath + '/' + self.savename + '(' + self.dataFrame + ').txt'
                with open(Path,'w') as f:
                    for i in range(len(DataforJS)):
                        f.write("['" + DataforJS[i][0] + "'," + \
                        str(DataforJS[i][1]) + ',' + str(DataforJS[i][2]) + ',' + \
                        str(DataforJS[i][3]) + ',' + str(DataforJS[i][4]) + '],' + '\n')
                        if i == len(DataforJS) - 1:
                            f.write("['" + DataforJS[i][0] + "'," + \
                            str(DataforJS[i][1]) + ',' + str(DataforJS[i][3]) + ',' + \
                            str(DataforJS[i][3]) + ',' + str(DataforJS[i][4]) + ']' + '\n')      
            elif self.modelType == 'model2':
                for i in range(startIdx,endIdx+1):
                    dateS.append(str(date_day[i])[0:4] + '/' + str(date_day[i])[4:6] + '/' + str(date_day[i])[6:])
                    dataK.append([Open_day[i],Close_day[i],Low_day[i],High_day[i],Volumn_day[i]])
                    DataforJS.append([dateS[-1],Open_day[i],Close_day[i],Low_day[i],High_day[i],Volumn_day[i]])
                Path = self.savepath + '/' + self.savename + '(' + self.dataFrame + ').txt'
                with open(Path,'w') as f:
                    for i in range(len(DataforJS)):
                        f.write("['" + DataforJS[i][0] + "'," + \
                        str(DataforJS[i][1]) + ',' + str(DataforJS[i][2]) + ',' + \
                        str(DataforJS[i][3]) + ',' + str(DataforJS[i][4]) + ',' + str(DataforJS[i][5]) + '],' + '\n')
                        if i == len(DataforJS) - 1:
                            f.write("['" + DataforJS[i][0] + "'," + \
                            str(DataforJS[i][1]) + ',' + str(DataforJS[i][3]) + ',' + \
                            str(DataforJS[i][3]) + ',' + str(DataforJS[i][4]) + ',' + str(DataforJS[i][5]) + ']' + '\n')         

    def CreateHTMLForAnalysis(self):
        from bs4 import BeautifulSoup
        self.CheckAnyTimeRangeData()
        try:
            with open(self.modelHTMLPath,'r',encoding='utf-8') as f:
                Data = BeautifulSoup(f.read(),"lxml")
            jsStr = Data.body.script.string
            Data.body.div['style'] = 'width:1600px;height:600px;' #对style属性和内容进行修改
            Str = "var data0 = splitData(["
            Str2 = "var title_text = "
            importdata = []
            for row in open(self.dataPath):
                importdata.append(row)
            if jsStr.find(Str) != 0:
                njsStr = jsStr[jsStr.find(Str):len(Str)+1] + '\n'
                for i in range(len(importdata)):
                    njsStr = njsStr + importdata[i]
                njsStr = njsStr + jsStr[len(Str)+1:]
            if njsStr.find(Str2) != 0:
                if self.dataPath.split('/')[-1][:-4] == 'MxkOfSglTrdRge':
                    njsStr1 = njsStr[:njsStr.find(Str2)+len(Str2)] + "'单笔最大亏损区间'" \
                    + njsStr[njsStr.find(Str2)+len(Str2):]
                elif self.dataPath.split('/')[-1][:-4] == 'MxkRge':
                    njsStr1 = njsStr[:njsStr.find(Str2)+len(Str2)] + "'回测期最大回撤区间'" \
                    + njsStr[njsStr.find(Str2)+len(Str2):]            
                elif self.dataPath.split('/')[-1][:-4] == 'MxAmntOfCtusWdlRge':
                    njsStr1 = njsStr[:njsStr.find(Str2)+len(Str2)] + "'最大连续回撤次数区间'" \
                    + njsStr[njsStr.find(Str2)+len(Str2):]
                else:
                    if self.dataFrame == '1M':
                        njsStr1 = njsStr[:njsStr.find(Str2)+len(Str2)] + "'1分钟K线图'" \
                        + njsStr[njsStr.find(Str2)+len(Str2):]    
                    elif self.dataFrame == '5M':
                        njsStr1 = njsStr[:njsStr.find(Str2)+len(Str2)] + "'5分钟K线图'" \
                        + njsStr[njsStr.find(Str2)+len(Str2):]     
                    elif self.dataFrame == 'D':
                        njsStr1 = njsStr[:njsStr.find(Str2)+len(Str2)] + "'日线K线图'" \
                        + njsStr[njsStr.find(Str2)+len(Str2):]                    
            Data.body.script.string = njsStr1
            html = open(self.newHTMLPath, "w", encoding="utf-8");
            html.write(str(Data));
            html.close();
        except Exception as e:
            self.msg("CreateHTMLForAnalysis Error","创建HTML分析出错，请检查！")

    def comBoxAct(self):
        self.dataFrame = self.comboBox.currentText()
        if self.comboBox.currentText() == 'D':
            self.st_le.setEnabled(False)
            self.et_le.setEnabled(False)
            self.startTime = 0
            self.endTime = 0
        else:
            self.st_le.setEnabled(True)
            self.et_le.setEnabled(True)
        self.modelType = self.comboBox_3.currentText()

    def leAct(self):
        if len(self.dp_le.text()) != 0:
            self.datapath = self.dp_le.text()
        if self.ed_le_2.text() != '':
            self.startDate = int(self.ed_le_2.text())
        if self.ed_le.text() != '':
            self.endDate = int(self.ed_le.text())
        if self.st_le.text() != '':
            self.startTime = int(self.st_le.text())
        if self.et_le.text() != '':
            self.endTime = int(self.et_le.text())
        if self.ed_le_3.text() != '':
            self.symbolName = self.ed_le_3.text().upper() 
        if self.ed_le_4.text() != '':
            self._IP = self.ed_le_4.text()
        if self.ed_le_5.text() != '':
            self._PORT = int(self.ed_le_5.text())
        if self.ed_le_6.text() != '':
            self._databasename = self.ed_le_6.text()

    def openDataFile(self):  
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))  
        if filename:
           self.dp_le.setText(filename)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def msg(self,string1,string2):
        reply = QMessageBox.critical(self,string1,string2)

    def load(self):
        try:      
            self.webView.load(QUrl.fromUserInput(self.newHTMLPath))
            self.webView.show()
        except Exception as e:
            self.msg("load Error","载入窗口部分有误，请检查！")

    def CreateHTMLFile(self):  
        if self.dataFrame == '1M' or self.dataFrame == '5M':
            if self.startTime == 0 and self.endTime == 0:
                self.savename = str(self.startDate) + "-" + str(self.endDate)
                self.newHTMLPath = self.savepath + "/" + self.savename + '(' + self.dataFrame + ').html'
                self.dataPath = self.savepath + "/" + self.savename + '(' + self.dataFrame + ').txt'
            else:
                self.savename = str(self.startDate) + str(self.startTime) + "-" + str(self.endDate) + str(self.endTime)
                self.newHTMLPath = self.savepath + "/" + self.savename + '(' + self.dataFrame + ').html'
                self.dataPath = self.savepath + "/" + self.savename + '(' + self.dataFrame + ').txt'
        elif self.dataFrame =='D':
            self.savename = str(self.startDate) + "-" + str(self.endDate)
            self.newHTMLPath = self.savepath + "/" + self.savename + '(' + self.dataFrame + ').html'
            self.dataPath = self.savepath + "/" + self.savename + '(' + self.dataFrame + ').txt'     
        self.modelHTMLPath = os.getcwd() + "/" + self.modelType + ".html"
        try:
           self.CreateHTMLForAnalysis()
           self.load()
        except Exception as e:
            self.msg("CreateHTMLFile Error","该日期时间对应的数据不存在，请重新输入!")


if __name__ == '__main__':    
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
