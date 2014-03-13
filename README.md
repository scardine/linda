Linda
=====

Linda's assignment for oDesk interview.

Raison d'etre
-------------

My name is Paulo Scardine and I live at Sao Paulo, Brazil. A few months ago I decided I don't
want to have 10 million neighbours anymore, so I'm pursuing the "digital nomad" errand in order to
move to a small town. So far I'm doing great at oDesk.

Linda Lo is a recruiter from oDesk (is she aware that her name means "pretty" in Portuguese?).

As part of a recruitment proccess I received the following assignment:

> This should take you less than 20 minutes to reply.

> 1. Please provide a code sample in Python showing a moderately complicated operation in the context of a consumer app.  It can be the RESTful interface, some data manipulation in response to user input, or processing and output based on the user’s data.  Whichever it is, please provide a sample of of a few hundred lines of code from one of your projects.

This one is tough... Most of the code I write is covered by some NDA, is smaller than a few hundred lines or is obsolete by now.

> 2. Write a small program that I could install on my AWS server that is a generator that gives the firstname of subscribers from a MySQL table, with user_id #s between 1234 and 1334, and that produces the name in English alphabetical order. The structure of the MySQL table can be anything you suggest.

I hope this serves as an answer for number 1 and 2; it is not a few hundred lines of code but Python being as concise as it is, a few hundred lines of Python are more in the 20 hours range than 20 minutes.

> 3. How many ways can you append or concatenate strings? Which of these ways is fastest? Easiest to read? Does your answer change based on count of strings? Or size of strings?

There are two idiomatic ways to concatenate strings.

```python
# A
"a" + "b"
# B
"".(["a", "b"])
```

Short answer is... does it matter? Premature optimization is the root of all evil. That said, A is pretty ok for small strings and B performs better for a big number of strings.

Long answer is: performance can vary both in speed and memory consumption based on implementation, size of strings, number of strings, if they are bytecode or unicode and so on. Always profile.


Instructions
------------

This works for any database supported by SQLAlchemy, not only for MySQL (you may have to install other database drivers). I assume you have the development libraries for MySQL client (on ubuntu, `sudo apt-get install libmysqlclient-dev`). 

Clone the repo:

    git clone https://github.com/scardine/linda
    cd linda

Install requirements (creating a virtualenv before may be a good idea). 

    pip install -r requirements.txt
    
List commands:
    
    $ fab -l
    
    Available commands:

    arguments  List arguments and defaults
    drop       Drop table
    getrange   Get a range of users based on user_id, default between 1234 and 1334
    setup      Creates table if it does not exist, and create 2000 fake users.

Get the list of arguments:

    $ fab arguments
    
    Arguments and defaults are:

        driver:   'mysql'
        username: 'root'
        password: ''
        dbhost:   'localhost'
        port:     '3307'
        database: 'test'
        table:    'users'

    Usage:

        fab command:arg1=value1,arg2=value2,argN=valueN

I assume your users table has a field called `user_id`. If you don't have such a table yet, run the `setup` command in order to create the table and some fake users:

    $ fab setup:driver=mysql,username=paulos,password=test,howmany=1500
    
    Created user 1: Aldin Sutija
    Created user 2: David Jaijeet
    Created user 3: Conroy Clarise
    Created user 4: Aldrich Neyer
    Created user 5: Ransell Hella
    ...
    
And finally the assignment:

    $ fab getrange:driver=mysql,username=paulos,password=test,start=1234,end=1244
    
    Connecting to mysql://paulos:test@db/test
    1234    Ulises Kuo-Chuan
    1235    Waverley Shing
    1236    Hollis Haibo
    1237    Courtney Tijeun
    1238    Stephan Merritt
    1239    Ring Arno
    1240    Peter Huichaun
    1241    Roberto Moni
    1242    Vincent Thersa
    1243    Dare Daesik
    1244    Jarret Ta

    Done.
    
    


    


