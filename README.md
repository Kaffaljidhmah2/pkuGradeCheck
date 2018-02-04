# pkuGradeCheck
Peking University grades auto-checker using data from http://dean.pku.edu.cn

Many students are having a hard time checking their grades after final exams. They nervously login to check whether new grades come out every minute.
This program written in Python will automatically recognize the validation code, login, check if there are changes in the grade list, and send an e-mail to you if necessary.

### Environment
Python 3
requests
numpy
PIL or pillow

### Main Parameters
in getGrade.py:
1.sender: mailbox uesrname.
2.passcode: mailbox password.
3.smtpserver: smtp server of your mailbox.
4.receiver: mailbox address you want to receive an email indicating new grades sent by the program.
5.pku_username: your pku school number.
6.pku_password: your pku_dean password.
7.interval: the time interval between two auto-checks.

### Validation Code Recognition
The **proc.py** module helps you recognize the specific dean validation code. Here is how it works:
1. Split characters
2. Construct e-vector, which tells you the number of the connected "black" pixels of each row.
3. Using **k-NearestNeighbour** to fulfill prediction.

Accuracy: around 20%, enough for auto-login because it can retry several times.

### Finite State Machine
The program features a **finite state machine** to maintain the states, which can increase the stability.
There are three states, namely **login**, **query wait**, and **send email**. 
1.**login** The program is trying to login using the pku username and password provided.
2.**query wait** The program is waiting for the next check. The interval is 60 seconds by default.
3.**send mail** The program is trying to send and e-mail to you using the mailbox address and password provided.
