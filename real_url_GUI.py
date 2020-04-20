# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from main_UI import Ui_MainWindow
import re
from real_url import *

class Interface(QMainWindow, Ui_MainWindow):
    urlByPlatform = {'斗鱼':douyu.get_real_url, '虎牙':huya.get_real_url, 'Bilibili':bilibili.get_real_url,
                     '触手':chushou.get_real_url, '抖音':douyin.get_real_url, '企鹅电竞':egame_qq.get_real_url,
                     '花椒':huajiao.get_real_url, '火猫':huomao.get_real_url, '爱奇艺':iqiyi.get_real_url,
                     '快手':kuaishou.get_real_url, '酷狗':kugou.get_real_url, '龙珠':longzhu.get_real_url,
                     'NOW':now.get_real_url, 'pps':pps.get_real_url, '六间房':v6cn.get_real_url,
                     '网易CC':wangyi_cc.get_real_url, '西瓜':xigua.get_real_url, '映客':yingke.get_real_url,
                     '一直播"':yizhibo.get_real_url, 'YY':yy.get_real_url, '战旗':zhanqi.get_real_url}

    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)
        self.setupUi(self)
        self.getUrlButton.clicked.connect(self.getUrl)
        self.roomID.textChanged.connect(self.ridStatusChange)
        self.selectedList.itemChanged.connect(self.exportStatusChange)
        self.selectedList.itemClicked.connect(self.urlCopy)
        self.selectedList.itemDoubleClicked.connect(self.deleteItem)

    def getUrl(self):
        platform = self.comboBox.currentText()
        rid = self.roomID.text()

        realUrl = self.urlByPlatform[platform](rid)

        textOnlyCHN = "".join(re.compile('[^\u4e00-\u9fa5]').split(realUrl)).strip()
        
        if textOnlyCHN != realUrl:
            self.updataSelectList(platform, rid, realUrl)
        else:
            QMessageBox.information(self, '完成', '获取地址错误')

    def ridStatusChange(self):
        if len(self.roomID.text()) == 0:
            self.getUrlButton.setEnabled(False)
        else:
            self.getUrlButton.setEnabled(True)
    
    def exportStatusChange(self):
        if self.selectedList.rowCount == 0:
            self.exportButton.setEnabled(False)
        else:
            self.exportButton.setEnabled(True)

    def urlCopy(self):
        realUrl = self.selectedList.item(self.selectedList.currentRow(), 2).text()
        clipboard = QApplication.clipboard()
        clipboard.setText(realUrl)

    def deleteItem(self):
        self.selectedList.removeRow(self.selectedList.currentRow())

    def updataSelectList(self, platform, rid, url):
        roomInfo = [platform, rid, url]
        row = self.selectedList.rowCount()
        self.selectedList.insertRow(row)
        self.selectedList.setItem(row, 0, QTableWidgetItem(str(roomInfo[0])))
        self.selectedList.setItem(row, 1, QTableWidgetItem(str(roomInfo[1])))
        self.selectedList.setItem(row, 2, QTableWidgetItem(str(roomInfo[2])))



if __name__ == "__main__":
    app = QApplication(sys.argv)

    real_url_GUI = Interface()
    real_url_GUI.show()

    sys.exit(app.exec_())
