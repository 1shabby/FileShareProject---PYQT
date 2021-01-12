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
import Functions

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


class Functions_Page(QtWidgets.QMainWindow, Functions.Ui_FunctionWIndow):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Functions_Page, self).__init__(parent)
        self.setupUi(self)
        self.DisconnectButton.clicked.connect(self.DisconnectPressed)
        self.FunctionsController = Controller()

    def DisconnectPressed(self):
        self.hide()
        self.FunctionsController.ShowConnectPage()


class Connect_Page(QtWidgets.QMainWindow, Connect.Ui_ConnectWindow):

    switch_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Connect_Page, self).__init__(parent)
        self.setupUi(self)
        self.AddConnections()
        self.BackPushButton.clicked.connect(self.BackButtonPressed)
        self.ClearButton.clicked.connect(self.ClearButtonClicked)
        self.ConnectButton.clicked.connect(self.ConnectToServer)

        ConfigFilePath = self.Config_check()
        self.SavedConnectionComboBox.currentIndexChanged.connect(
            self.FillEntries)
        self.ConnectController = Controller()

    def OpenFunctions(self):
        self.hide()
        self.ConnectController.ShowFunctionsPage()

    def BackButtonPressed(self):
        self.hide()
        self.ConnectController.ShowHomePage()

    def AddConnections(self):
        Config_Parser = CONFIG_PARSER
        ConfigFilePath = self.Config_check()
        Config_Parser.read(ConfigFilePath)
        AutoLoad = Config_Parser.get('settings', 'auto_connect')

        ConnectionCount = Config_Parser.get('Connection Count', 'count')
        count = 1
        if AutoLoad == "True":
            self.SavedConnectionComboBox.addItem("Select a Connection...")
            while count <= int(ConnectionCount):
                header = "Connection " + str(count)
                ConnectionIP = Config_Parser.get(header, "ip")
                ConnectionPort = Config_Parser.get(header, "port")
                line = "Connection " + \
                    str(count) + ": IP: " + str(ConnectionIP) + \
                    " Port: " + str(ConnectionPort)
                self.SavedConnectionComboBox.addItem(line)
                count += 1

        if AutoLoad == "False":
            self.SavedConnectionComboBox.addItem(
                "Enable Auto Load in Config Modify.")
            self.SavedConnectionComboBox.setEnabled(False)

    def FillEntries(self):
        Config_Parser = CONFIG_PARSER
        ConfigFilePath = self.Config_check()
        Config_Parser.read(ConfigFilePath)

        index = self.SavedConnectionComboBox.currentIndex()
        if index > 0:
            IPAddress = Config_Parser.get('Connection ' + str(index), 'ip')
            PortAddress = Config_Parser.get('Connection ' + str(index), 'port')

            self.ServerIPLineEdit.setText(IPAddress)
            self.ServerPortLineEdit.setText(PortAddress)
        elif index == 0:
            self.ServerIPLineEdit.setText("")
            self.ServerPortLineEdit.setText("")

    def ClearButtonClicked(self):
        self.ServerPortLineEdit.setText("")
        self.ServerIPLineEdit.setText("")
        self.UsernameLineEdit.setText("")
        self.PasswordLineEdit.setText("")

    def Config_check(self):
        ConfigFilePath = os.path.join(sys.path[0], "config.ini")
        isFile = os.path.isfile(ConfigFilePath)
        if isFile == False:
            QMessageBox.about(
                self, "Critical Error!", "Config.ini file not found in the same dir of this application!")
            QMessageBox.setIcon(QMessageBox.Critical)
            QMessageBox.show()
            exit()

        return ConfigFilePath

    def ConnectToServer(self):
        Server = FTP('')
        ServerIP = self.ServerIPLineEdit.text()
        ServerPort = self.ServerPortLineEdit.text()

        Username = self.UsernameLineEdit.text()
        Password = self.PasswordLineEdit.text()

        try:
            Server.connect(ServerIP, int(ServerPort))
        except:
            QMessageBox.about(
                self, 'Connect Failed', 'IP and or Port does not have a server hosted on it.')
        try:
            Server.login(user=Username, passwd=Password)
            self.OpenFunctions()

        except:
            QMessageBox.about(
                self, 'Login Failed', 'Username or Password provided was not correct.'
            )


class Edit_Config_Page(QtWidgets.QMainWindow, EditConfig.Ui_EditConfigWindow):

    switch_window = QtCore.pyqtSignal()

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
        self.AddNewConnectionButton.clicked.connect(self.AddConnection)
        self.RemoveButton.clicked.connect(self.RemoveConnection)
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
            line = "Connection " + \
                str(count) + ": IP: " + str(ConnectionIP) + \
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

    def RemoveConnection(self):
        ConfigFilePath = self.config_check()
        Config_Parser = CONFIG_PARSER

        Config_Parser.read(ConfigFilePath)
        ConnectionCount = Config_Parser.get("Connection Count", "count")
        NewConnectionCount = int(ConnectionCount) - 1
        removeIndex = self.DisplayListWidget.currentRow() + 1
        print(removeIndex)
        print(ConnectionCount)
        # Checking to see if we want to remove the last item. If so remove it from the ini file and GUI and done.
        if removeIndex == int(ConnectionCount):
            print('first if')
            removeSection = 'Connection ' + str(removeIndex)
            print(removeSection)
            Config_Parser.remove_section(removeSection)
            self.DisplayListWidget.takeItem(
                self.DisplayListWidget.currentRow())

            Config_Parser.set('Connection Count', 'Count',
                              str(NewConnectionCount))
            with open(ConfigFilePath, 'w') as configfile:
                Config_Parser.write(configfile)
        # Checks to see if the index we want to remove is one that is not the last position.
        elif removeIndex < int(ConnectionCount):
            print('first elif')
            nextIndex = removeIndex + 1
            currentIndex = removeIndex
            # While the current index is not equal to the last connection do:
            while currentIndex < int(ConnectionCount):
                # Update the target section headers.
                CurrentSection = 'Connection ' + str(currentIndex)
                NextSection = 'Connection ' + str(nextIndex)
                # If the current selected section is not the last section do:
                if nextIndex < int(ConnectionCount):
                    print("second if")
                    print("next Index = " + str(nextIndex))
                    # Get the IP of the connection below the current connection in the file.
                    NextIP = Config_Parser.get(NextSection, 'ip')
                    print("next ip = " + NextIP)
                    # Get the port of the connection below the current COnnection in the file.
                    NextPort = Config_Parser.get(NextSection, 'port')
                    print("next port = " + NextPort)

                    # Set the current sections ip and port equal to the next sections ip and port
                    Config_Parser.set(CurrentSection, 'ip', NextIP)
                    Config_Parser.set(CurrentSection, 'port', NextPort)
                    # Write the changes to the file.
                    with open(ConfigFilePath, 'w') as configfile:
                        Config_Parser.write(configfile)
                # If the next index is equal to the last connection do:
                elif nextIndex == int(ConnectionCount):
                    NextIP = Config_Parser.get(NextSection, 'ip')
                    NextPort = Config_Parser.get(NextSection, 'port')
                    Config_Parser.set(CurrentSection, 'ip', NextIP)
                    Config_Parser.set(CurrentSection, 'port', NextPort)

                    Config_Parser.remove_section('Connection' + str(nextIndex))

                    Config_Parser.set('Connection Count',
                                      'Count', str(NewConnectionCount))

                    with open(ConfigFilePath, 'w') as configfile:
                        Config_Parser.write(configfile)

                currentIndex = currentIndex + 1
                nextIndex = nextIndex + 1

            """ self.DisplayListWidget.clear()
            count = 1
            while count <= int(ConnectionCount):
                header = "Connection " + str(count)
                ConnectionIP = Config_Parser.get(header, "ip")
                ConnectionPort = Config_Parser.get(header, "port")
                line = "Connection " + \
                    str(count) + ": IP: " + str(ConnectionIP) + \
                    " Port: " + str(ConnectionPort)
                self.DisplayListWidget.insertItem(count, line)
                count += 1 """

    def AddConnection(self):
        ConfigFilePath = self.config_check()
        Config_Parser = CONFIG_PARSER
        connectionCount = Config_Parser.get("Connection Count", "count")
        UpdatedConnectionCount = int(connectionCount) + 1
        ServerIP = self.ServerIPLineEdit.text()
        ServerPort = self.lineEdit_2.text()
        SectionHeader = 'Connection ' + str(UpdatedConnectionCount)

        Config_Parser.read(ConfigFilePath)
        # Adds a new section to the ini file in accordance to our setup.
        Config_Parser.add_section(SectionHeader)
        Config_Parser.set(SectionHeader, 'ip', ServerIP)
        Config_Parser.set(SectionHeader, 'port', ServerPort)
        # Updates the count to ensure all the connections get shown everytime you navigate to this page.
        Config_Parser.set('Connection Count', 'count',
                          str(UpdatedConnectionCount))
        with open(ConfigFilePath, 'w') as configfile:
            Config_Parser.write(configfile)

        line = SectionHeader + ": IP: " + \
            str(ServerIP) + " Port: " + str(ServerPort)
        self.DisplayListWidget.insertItem(UpdatedConnectionCount, line)
        self.ServerIPLineEdit.setText("")
        self.lineEdit_2.setText("")

    def EditConnection(self):
        ServerIP = self.ServerIPLineEdit.text()
        ServerPort = self.lineEdit_2.text()
        IPValid = self.ip_check(ServerIP)
        PortValid = self.port_check(ServerPort)
        SelectedRow = self.DisplayListWidget.currentRow() + 1

        Config_Parser = CONFIG_PARSER
        ConfigFilePath = self.config_check()
        ConnectionCount = Config_Parser.get("Connection Count", "count")

        if IPValid == True and PortValid == True:
            Config_Parser.set(
                'Connection ' + str(SelectedRow), 'ip', str(ServerIP))
            Config_Parser.set('Connection ' + str(SelectedRow),
                              'port', str(ServerPort))
            with open(ConfigFilePath, 'w') as configfile:
                Config_Parser.write(configfile)
            self.DisplayListWidget.clear()
            count = 1
            while count <= int(ConnectionCount):
                header = "Connection " + str(count)
                ConnectionIP = Config_Parser.get(header, "ip")
                ConnectionPort = Config_Parser.get(header, "port")
                line = "Connection " + \
                    str(count) + ": IP: " + str(ConnectionIP) + \
                    " Port: " + str(ConnectionPort)
                self.DisplayListWidget.insertItem(count, line)
                count += 1

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

    def ShowFunctionsPage(self):
        self.FunctionsPage = Functions_Page()
        self.FunctionsPage.show()


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.ShowHomePage()
    app.exec_()


if __name__ == '__main__':
    main()
