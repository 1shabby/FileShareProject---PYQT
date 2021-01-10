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

        ConfigFilePath = self.config_check()
        Config_Parser = CONFIG_PARSER

        super(Edit_Config_Page, self).__init__(parent)
        self.setupUi(self)
        Config_Parser.read(ConfigFilePath)
        connectionCount = Config_Parser.get("Connection Count", "count")
        autoLoad = Config_Parser.get("settings", "auto_connect")

        if autoLoad == "True":
            self.AutoLoadButton.setChecked(True)

        self.GetConnectionInfo(Config_Parser, connectionCount)
        self.BackButton.clicked.connect(self.BackButtonPressed)
        self.DisplayListWidget.itemSelectionChanged.connect(
            self.viewItemChanged)
        self.lineEdit_2.textChanged.connect(self.InputFieldsChanged)
        self.ServerIPLineEdit.textChanged.connect(self.InputFieldsChanged)
        self.SaveButton.clicked.connect(self.EditConnection)
        self.AutoLoadButton.toggled.connect(self.SetAutoLoad)

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

    def viewItemChanged(self):
        if self.DisplayListWidget.size() == 0:
            self.RemoveButton.setEnabled(False)
            self.IndexLabel.setText("Current Index: None Selected")
        newIndex = self.DisplayListWidget.currentRow() + 1
        self.IndexLabel.setText("Current Index: " + str(newIndex))
        self.RemoveButton.setEnabled(True)

    def InputFieldsChanged(self):
        if self.ServerIPLineEdit.text() != "" and self.lineEdit_2.text() != "":
            self.AddNewConnectionButton.setEnabled(True)
            if self.DisplayListWidget.currentRow() > -1:
                self.SaveButton.setEnabled(True)
        else:
            self.SaveButton.setEnabled(False)
            self.AddNewConnectionButton.setEnabled(False)

    def SetAutoLoad(self):
        ConfigFilePath = self.config_check()
        Config_Parser = CONFIG_PARSER

        AutoLoad = ""
        if self.AutoLoadButton.isChecked() == True:
            AutoLoad = "True"

        elif self.AutoLoadButton.isChecked() == False:
            AutoLoad = "False"

        Config_Parser.set('settings', 'auto_connect', AutoLoad)
        with open(ConfigFilePath, 'w') as configfile:
            Config_Parser.write(configfile)

    # TODO: Implement the back end modification of the ini file and update the GUI.
    def RemoveConnection(self):

        return
    # TODO: Implement the back end modification of the ini file and update the GUI.

    def AddConnection(self):

        return

    def EditConnection(self):
        ServerIP = self.ServerIPLineEdit.text()
        ServerPort = self.lineEdit_2.text()
        IPValid = self.ip_check(ServerIP)
        PortValid = self.port_check(ServerPort)
        SelectedRow = self.DisplayListWidget.currentRow() + 1

        Config_Parser = CONFIG_PARSER
        ConfigFilePath = self.config_check()
        ConnectionCount = Config_Parser.get("Connection Count", "count")

        if IPValid == True and PortValid:
            Config_Parser.set(
                'Connection ' + str(SelectedRow), 'ip', str(ServerIP))
            Config_Parser.set('Connection ' + str(SelectedRow),
                              'port', str(ServerPort))
            with open(ConfigFilePath, 'w') as configfile:
                Config_Parser.write(configfile)
            # self.DisplayListWidget.clear()
            #self.GetConnectionInfo(ConfigParser, ConnectionCount)

    def ip_check(self, IP_Text):
        returnVal = False
        try:
            ipaddress.IPv4Address(IP_Text)
            returnVal = True
        except ValueError:
            QMessageBox.about(self,
                              "IP Error", "The IP address is not valid!")
        return returnVal

    def port_check(self, Port_Text):
        returnVal = False
        if int(Port_Text) > 0 and int(Port_Text) < 65536:
            returnVal = True
        else:
            QMessageBox.about(self,
                              "Port Error", "The Port doest not belong the legal domain! (1 - 65,535)")
        return returnVal


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
