==============================================================
          _____  ______          _____  __  __ ______  
         |  __ \|  ____|   /\   |  __ \|  \/  |  ____| 
         | |__) | |__     /  \  | |  | | \  / | |__    
         |  _  /|  __|   / /\ \ | |  | | |\/| |  __|   
         | | \ \| |____ / ____ \| |__| | |  | | |____  
         |_|  \_\______/_/    \_\_____/|_|  |_|______| 
                                               
==============================================================
Installation: Ensure that you have python installed
on your computer and ensure that Path is added to 
system variables when setting it up. Once python is
installed open your command prompt and run the following
to ensure that it is installed properly.

python --version

Your current version should be displayed below. If it 
displays the version now input

pip --version

This should output the version number followed by the path 
to the install directory. If this does not display properly 
try re-installing pip through python.

Once we know that python and pip are working as they should
we need to install a library that is used for the client
code. To install the library run:

pip install pyftpdlib

If you encounter any errors when running this I recommend 
visiting the documentation here:

https://pyftpdlib.readthedocs.io/en/latest/install.html

==============================================================
Setup: Once you download the files, you should have Main.py,
server.py, and cofig.ini. You NEED to ensure that all three 
files are contained in the same directory as Main.py runs 
server.py if you want to host the server through the client. 
In the Config.ini file you need to set the IP and Port that
you want to run the server through along with where you want 
the root of the directory that is shared to be.

You also are able to add users to the server via the config
file by following the example user provided. If you would like
to add additional users ensure that the sections are all
lowercase and the user section is added like: 
[user1]
user: username
pass: password

also ensure that anytime you add or remove a user that you 
change:

[user_count]
num_of_users = x

where x is the current number of users in the config file.
==============================================================
Usage: If you would like to, you may use alternitive file apps
to connect to the server, the key is that only users on the
same network as your computer hosting the server will be able
to connect to the server and access the files. If you
experience any crashes, look at any error codes that the
server provides. Also ensure that you are using the exact case
when chaning directories, adding or removing directories or
any other input that requires a file name.