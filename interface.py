import os
import signal
import sys
import datetime
import json
# 主窗口
from time import sleep

import mainwindow
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QInputDialog, QMessageBox, QFileDialog
# 条形图
from PyQt5.QtChart import QBarSet,QBarSeries,QBarCategoryAxis,QValueAxis,QChart
from PyQt5.QtCore import *
# 功能实现
import capture

from PyQt5.QtChart import QChartView

from model import createModel

class TimerMessageBox(QMessageBox):
    def __init__(self, timeout=3, parent=None):
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle("提示")
        self.time_to_wait = timeout
        self.setText("请等待，剩余时间 {0} 秒".format(timeout))
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        self.setText("请等待，剩余时间 {0} 秒".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait < 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

class Window(mainwindow.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setup_ui()

        # 实现功能
    def setup_ui(self):
        self.setupUi(self)
        self.setWindowTitle("用户管理界面")
        self.pushButton_2.clicked.connect(self.web_capture) #网络捕包
        self.pushButton_3.clicked.connect(self.local_split)  # 网络捕包
        self.pushButton.clicked.connect(self.kill_pid)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.on_switch)

    def on_switch(self):
        if self.tabWidget.currentIndex() == 1:
            self.display_bar()
        elif self.tabWidget.currentIndex() == 2:
            self.diplay_table()

    # 捕包
    def web_capture(self):
        capture.packet_web()
        # messagebox = TimerMessageBox(14, self)
        # messagebox.exec_()

    # 本地分析
    def local_split(self):
        filename , _ = QFileDialog.getOpenFileName(self,'打开文件','.','(*.pcap)')
        capture.packet_local(filename)


    # 实现条形图
    def display_bar(self):
        # QBarSet表示条形图中的一组条型，并添加数据
        data = json.load(open("sizetemp.tmp", 'r'))

        if data is None:
            return

        set0 = QBarSet("Byte")
        for d in data:
            set0.append(d)

        # QBarSeries类将一系列数据显示为按类别分组的垂直条。
        series = QBarSeries()
        series.append(set0)

        # QChart类管理图表系列(series)、图例(legends)和轴(axes)。
        chart = QChart()    #获取QChartView自带的chart
        self.graphicsView.setChart(chart)
        chart.addSeries(series) #将创建好的条形图series添加进chart中
        chart.setTitle("类型字节数") #设置标题
        chart.setAnimationOptions(QChart.SeriesAnimations)  #设置图表变化时的变化效果

        categories = ['Chat', 'Email', 'File', 'Stream/Browsing']    #x轴分类
        axisX = QBarCategoryAxis()
        axisX.setTitleText("类型")    #x轴标题
        axisX.append(categories)    #添加分类
        chart.addAxis(axisX,Qt.AlignBottom) #x轴放置在图表底部
        series.attachAxis(axisX)    #将axis指定的轴附着到series

        axisY = QValueAxis()
        # axisY.setRange(0,10)  #y轴范围
        axisY.setTitleText("字节数量")  #y轴标题
        chart.addAxis(axisY,Qt.AlignLeft)   #y轴放置在左侧
        series.attachAxis(axisY)

        chart.legend().setVisible(True) #图例可见
        chart.legend().setAlignment(Qt.AlignRight)  #图例位置

    # 实现表
    def diplay_table(self):
        # table = QTableWidget()
        # table.setFont(QFont("宋体"))
        # table.setColumnCount(3)
        # table.setHorizontalHeaderLabels(['应用','类型','pid'])

        self.tableWidget.clearContents()
        procl = json.load(open("proctemp.tmp", 'r'))
        i = 0
        for p in procl:
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(p[2]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(p[1]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(p[3]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(p[0]))
            i+=1

        # 禁止编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 整行显示
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 占满整行
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(True)

    # kill进程
    def kill_pid(self):
        text1, ok = QInputDialog.getInt(self, "kill进程", "请输入对应的pid")
        os.kill(text1, signal.SIGINT)
        output_path = ".\\log\\KillLog.log"
        f = open(output_path, "a")
        f.write(str(datetime.datetime.now()) + "\t" + "kill了pid为" + str(text1) + "的进程" + "\n")

config = json.load(open("configure.json", "r"))
dict_6class = {0:'Chat',1:'Email',2:'File',3:'P2p',4:'Streaming',5:'Voip'}
model = createModel(class_num=config["6net_novpn"]["class_num"])
model.load_weights(config["6net_novpn"]["ckpt_path"])
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Window()
    main_window.resize(884,798)
    main_window.show()
    sys.exit(app.exec_())