import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from configparser import ConfigParser

config_parser = ConfigParser()
authenication_parser = ConfigParser()

# config.ini location:
config_parser.read(
    'D:\Program Files (x86)\PythonApps\FileSharingProject\config.ini')

authenication_parser.read(
    'D:\Program Files (x86)\PythonApps\FileSharingProject\Authenication.ini')

server_IP = config_parser.get('server', 'IP')
server_Port = config_parser.get('server', 'Port')
root_dir = config_parser.get('server', 'root_dir')

# generate an authorizer
authorizer = DummyAuthorizer()


def printStartup():
    print("FFFFFFFFFFFFFFFFFFFFFFTTTTTTTTTTTTTTTTTTTTTTTPPPPPPPPPPPPPPPPP   \n"
          "F::::::::::::::::::::FT:::::::::::::::::::::TP::::::::::::::::P  \n"
          "F::::::::::::::::::::FT:::::::::::::::::::::TP::::::PPPPPP:::::P \n"
          "FF::::::FFFFFFFFF::::FT:::::TT:::::::TT:::::TPP:::::P     P:::::P\n"
          "  F:::::F       FFFFFFTTTTTT  T:::::T  TTTTTT  P::::P     P:::::P\n"
          "  F:::::F                     T:::::T          P::::P     P:::::P\n"
          "  F::::::FFFFFFFFFF           T:::::T          P::::PPPPPP:::::P \n"
          "  F:::::::::::::::F           T:::::T          P:::::::::::::PP  \n"
          "  F:::::::::::::::F           T:::::T          P::::PPPPPPPPP    \n"
          "  F::::::FFFFFFFFFF           T:::::T          P::::P            \n"
          "  F:::::F                     T:::::T          P::::P            \n"
          "  F:::::F                     T:::::T          P::::P            \n"
          "FF:::::::FF                 TT:::::::TT      PP::::::PP          \n"
          "F::::::::FF                 T:::::::::T      P::::::::P          \n"
          "F::::::::FF                 T:::::::::T      P::::::::P          \n"
          "FFFFFFFFFFF                 TTTTTTTTTTT      PPPPPPPPPP          \n")

# Pulls user info from the config.ini file and adds the users to the server.
# note this is only done during the startup of the server, and thus if you
# add a new user during runtime, you won't be able to connect to the server


def generateUsers():
    user_count = int(authenication_parser.get('user_count', 'num_of_users'))
    count = 1
    check = 0
    feedback = input("Would you like to enable anonymous users?(y/n)\n")
    if feedback.lower() == 'y':
        authorizer.add_anonymous(root_dir)
        check = 1
    print("\n Adding users:\n")
    while int(count) <= user_count:
        username = authenication_parser.get('user' + str(count), 'user')
        # print(username + "\n") #Debugging Purposes
        password = authenication_parser.get('user' + str(count), 'pass')
        # print(password + "\n") #Debugging Purposes
        permission = authenication_parser.get(
            'user' + str(count), 'permission')
        authorizer.add_user(username, password, root_dir, permission)
        print("User: " + username + " added!")
        int(count)
        count += 1
    if check == 1:
        print("Anonymous users added!")


def printInfo():
    print("\nIP: " + server_IP)
    print("Port: " + server_Port)
    print("\n")


def main():
    printStartup()
    generateUsers()

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "Welcome to FTPD server!"

    address = (server_IP, server_Port)
    server = FTPServer(address, handler)
    printInfo()

    # set a limit for connections
    server.max_cons = int(config_parser.get("settings", "max_connections"))
    server.max_cons_per_ip = int(config_parser.get(
        "settings", "max_connections_per_ip"))

    # start ftp server
    server.serve_forever()


if __name__ == '__main__':
    main()
