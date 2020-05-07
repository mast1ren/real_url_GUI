# -*- coding: utf-8 -*-
import sys, logging, time, importlib, UI, re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from main_UI import Ui_MainWindow

class Interface(QMainWindow, Ui_MainWindow):
    urlByPlatform = {'斗鱼':'douyu', '虎牙':'huya', 'Bilibili':'bilibili',
                     '触手':'chushou', '抖音':'douyin', '企鹅电竞':'egame_qq',
                     '花椒':'huajiao', '火猫':'huomao', '爱奇艺':'iqiyi',
                     '快手':'kuaishou', '酷狗':'kugou', '龙珠':'longzhu',
                     'NOW':'now', 'pps':'pps', '六间房':'v6cn',
                     '网易CC':'wangyi_cc', '西瓜':'xigua', '映客':'yingke',
                     '一直播"':'yizhibo', 'YY':'yy', '战旗':'zhanqi', 
                     '17live':'_17live', '来疯':'laifeng'}

    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)
        self.setupUi(self)
        self.getUrlButton.clicked.connect(self.getUrl)
        self.roomID.textChanged.connect(self.ridStatusChange)
        self.selectedList.itemChanged.connect(self.exportStatusChange)
        self.selectedList.itemClicked.connect(self.urlCopy)
        self.selectedList.itemDoubleClicked.connect(self.deleteItem)
        self.exportButton.clicked.connect(self.exportUrl)

    def getUrl(self):
        platform = self.comboBox.currentText()
        logging.info('get stream platform')
        rid = self.roomID.text()
        logging.info('get room id')
        mod = self.urlByPlatform[platform]

        try:
            fun = importlib.import_module('..' + mod, 'real_url.subpkg')
            logging.info('import ' + mod + ' mod')
        except:
            logging.error('import failed!')
            QMessageBox.warning(self, '错误', '6 导入模块错误')
        try:
            realUrl = fun.get_real_url(rid)
            logging.info('get ' + platform + ' real url')
        except:
            QMessageBox.warning(self, '错误', '0 获取链接错误')
            logging.error('error occur when getting ' + platform + ' real url')
        else:
            textOnlyCHN = "".join(re.compile('[^\u4e00-\u9fa5]').split(realUrl)).strip()
            logging.info('match Chinese unicode')
            if textOnlyCHN != realUrl:
                self.updataSelectList(platform, rid, realUrl)
                logging.info('update url info')
            else:
                QMessageBox.information(self, '失败', '1 获取地址失败')
                logging.warning('failed to get url')

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
        try:
            clipboard.setText(realUrl)
            logging.info('copy url')
        except WindowsError:
            QMessageBox.warning(self, '错误', '2 复制到剪切板失败')
            logging.error('failed to copy url')

    def deleteItem(self):
        self.selectedList.removeRow(self.selectedList.currentRow())
        logging.info('delete url info')

    def updataSelectList(self, platform, rid, url):
        roomInfo = [platform, rid, url]
        row = self.selectedList.rowCount()
        self.selectedList.insertRow(row)
        self.selectedList.setItem(row, 0, QTableWidgetItem(str(roomInfo[0])))
        self.selectedList.setItem(row, 1, QTableWidgetItem(str(roomInfo[1])))
        self.selectedList.setItem(row, 2, QTableWidgetItem(str(roomInfo[2])))

    def exportUrl(self):
        try:
            realUrlFile = open("realUrl.dpl", "w", encoding="utf-8")
            logging.info('create or open realUrl.dpl file')
            realUrlFile.write("DAUMPLAYLIST\ntopindex=0\nsaveplaypos=0\n")
            logging.info('write title in realUrl.dpl')
            rowCount = self.selectedList.rowCount()
            for i in range(rowCount):
                realUrlFile.write(str(i + 1) + "*file*" + self.selectedList.item(i, 2).text() + '\n')
                realUrlFile.write(str(i + 1) + "*title*" + self.selectedList.item(i, 0).text() + '-' + self.selectedList.item(i, 1).text() + '\n')
                realUrlFile.write(str(i + 1) + "*played*0\n")
            logging.info('write information in realUrl.dpl')
        except IOError:
            QMessageBox.warning(self, '失败', '3 读取或写入文件失败')
            logging.error('failed to open or write file')
        except UnicodeError:
            QMessageBox.warning(self, '失败', '4 编码错误')
            logging.error('encoding error')
        except:
            QMessageBox.warning(self, '错误', '5 未知错误')
            logging.error('unknown error')
        else:
            QMessageBox.information(self, '完成', '已经导出文件')
            logging.info('export complete')
            realUrlFile.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    logging.basicConfig(filename = 'info.log', filemode = 'a', format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level = logging.INFO)
    real_url_GUI = Interface()
    real_url_GUI.show()

    sys.exit(app.exec_())
