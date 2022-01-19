# 110-1 Database System Final Project

## Team members
- 108590050 李浩銘
- 108590004 謝宗麟
- 108590029 朱欣雨
- 108590049 符芷琪
- 108590056 鄭琳玲
- 108590061 黃聖耀
- 110AEM001 盧佩怡
- 110AEM002 譚永駿

### Note for Team Members
> PLEASE DO NOT ADD ';' TO PYTHON CODE AT THE END OF SENTENCE

Scrum developing procedure:
1. Take a task you are interested in from [Miro](https://miro.com/welcomeonboard/MkF1UFZBb2tJeHM4Nmxtc0lueTZ3b3lJZXQ0TWFWc1lOb25FemFacVB3WVJ3NVlrSWZqTFRuT0xvQ2d6OGYyTHwzMDc0NDU3MzYyMDA0NjQyMjM2?invite_link_id=149965833091)
2. Develop your part on your branch
3. Create a Pull Request(PR) after you finish developing your part
4. Your PR will be reviewed in the Sprint Review
5. Fix your PR if necessary
5. Your PR will be merged into master branch after reviewed
6. Pull and merge master branch into your branch
7. Fix conflict if necessary  
*Pay attention to the compatibility of each function during fixing conflict*

Sprint Review #1: 13 Oct (Wed) at 18:10 @Google Meet  
Sprint Review #2: 29 Oct (Fri) at 13:10 @TB6-327  
Sprint Review #3: 5 Nov (Fri) at 13:10 @TB6-327  
Sprint Review #4: 26 Nov (Fri) at 13:10 @TB6-327  
Sprint Review #5: 3 Dec (Fri) at 13:10 @TB6-327  
Sprint Review #6: 7 Dec (Tue) at 13:10 @TB6-327  
Sprint Review #7: 14 Dec (Tue) at 13:10 @TB6-327  
Sprint Review #8: 7 Jan (Fri) at 13:10 @TB6-327  
Sprint Review #9: TBD

### Deploy
#### Development Enverinment
 - OS: Ubuntu 18.04
 - Memory: 8 GB
 - Processors: 4
 - Hard Disk: 100 GB
 - DBMS: MariaDB

#### Install dependencies
In the terminal
``` bash
> pip3 install -r requirements.txt
```

#### Setup config.py
Create a python file in `./instance/config.py`
> Project
> └ app
> └ document
> └ instance
> └ tests

``` python
import os;

DEBUG = True;
SECRET_KEY = os.urandom(32);
SESSION_PROTECTION = 'strong';

# Database config
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<DBMS username>:<DBMS password>@localhost:3306/<database>';
''' REMEMBER TO CHANGE < > '''

SQLALCHEMY_TRACK_MODIFICATIONS = True;

# Mail Server config
MAIL_SERVER = 'smtp.gmail.com';
MAIL_PORT = 465;
MAIL_USE_SSL = True;
MAIL_USERNAME = 't108xxxxxx@ntut.org.tw';
MAIL_PASSWORD = '<gmail password>';
''' REMEMBER TO CHANGE < > '''
```

#### Initialize database
In the terminal
``` bash
> flask init-db
```

#### Run Web Server
In the terminal
``` bash
> flask run
```

