import sys
import os
import ipaddress

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
from configparser import ConfigParser
from ftplib import FTP

import Connect
import HomePage
import EditConfig

CONFIG_PARSER = ConfigParser()


class Home_Page(QtWidgets.QMainWindow, HomePage.Ui_StartWindow):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Home_Page, self).__init__(parent)
        self.setupUi(self)
        self.config_check()
        self.ConnectButton.clicked.connect(self.ConnectButtonPressed)
        self.QuitButton.clicked.connect(self.QuitButtonPressed)
        self.iniConfigButton.clicked.connect(self.EditConfigButtonPressed)
        self.homeController = Controller()

    def ConnectButtonPressed(self):
        self.hide()
        self.homeController.ShowConnectPage()

    def EditConfigButtonPressed(self):
        self.hide()
        self.homeController.ShowEditConfigPage()

    def config_check(self):
        ConfigFilePath = os.path.join(sys.path[0], "config.ini")
        isFile = os.path.isfile(ConfigFilePath)
        if isFile == False:
            QMessageBox.about(
                self, "Critical Error!", "Config.ini file not found in the same dir of this application!")
            QMessageBox.setIcon(QMessageBox.Critical)
            QMessageBox.show()
            exit()

    def QuitButtonPressed(self):
        exit()


class Connect_Page(QtWidgets.QMainWindow, Connect.Ui_ConnectWindow):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Connect_Page, self).__init__(parent)
        self.setupUi(self)
        self.BackPushButton.clicked.connect(self.BackButtonPressed)
        self.ConnectController = Controller()

    def BackButtonPressed(self):
        self.hide()
        self.ConnectController.ShowHomePage()


class Edit_Config_Page(QtWidgets.QMainWindow, EditConfig.Ui_EditConfigWindow):

    switch_wndow = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Edit_Config_Page, self).__init__(parent)
        self.setupUi(self)
        ConfigFilePath = self.config_check()
        Config_Parser = ConfigParser()
        Config_Parser.read(ConfigFilePath)
        connectionCount = Config_Parser.get("Connection Count", "count")
        autoLoad = Config_Parser.get("settings", "auto_connect")

        if autoLoad == "true":
            self.AutoLoadButton.setChecked(True)

        self.GetConnectionInfo(Config_Parser, connectionCount)
        self.BackButton.clicked.connect(self.BackButtonPressed)
        # For the list widget link the selected function to a method here!
        # self.AutoLoadButton.clicked.connect(self.SetAutoLoad)
        self.EditConfigController = Controller()

    def BackButtonPressed(self):
        self.hide()
        self.EditConfigController.ShowHomePage()

    # Checks when the Window is rendered to see if the Config.ini file is present, else give a critical error and close.
    def config_check(self):
        ConfigFilePath = os.path.join(sys.path[0], "config.ini")
        isFile = os.path.isfile(ConfigFilePath)
        if isFile == False:
            QMessageBox.about(
                self, "Critical Error!", "Config.ini file not found in the same dir of this application!")
            QMessageBox.setIcon(QMessageBox.Critical)
            QMessageBox.show()
            exit()
        else:
            return ConfigFilePath

    def GetConnectionInfo(self, Config_Parser, connectionCount):
        count = 1
        while count <= int(connectionCount):
            header = "Connection " + str(count)
            ConnectionIP = Config_Parser.get(header, "ip")
            ConnectionPort = Config_Parser.get(header, "port")
            line = "Connection " + str(count) + ": IP: " + str(ConnectionIP) + \
                " Port: " + str(ConnectionPort)
            self.DisplayListWidget.insertItem(count, line)
            count += 1

    def SetAutoLoad(self):
        AutoLoad = ""
        if self.AutoLoadButton.isChecked == True:
            AutoLoad = "True"
        elif self.AutoLoadButton.isChecked == False:
            AutoLoad = "False"
        print(AutoLoad)

    def RemoveConnection(self, ConfigFilePath, ConfigParser):

        return

    def AddConnection(self):

        return


class Controller:
    def __init__(self):
        pass

    def ShowHomePage(self):
        self.HomePage = Home_Page()
        self.HomePage.show()

    def ShowConnectPage(self):
        self.ConnectPage = Connect_Page()
        self.ConnectPage.show()

    def ShowEditConfigPage(self):
        self.EditConfigPage = Edit_Config_Page()
        self.EditConfigPage.show()


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.ShowHomePage()
    app.exec_()


if __name__ == '__main__':
    main()
