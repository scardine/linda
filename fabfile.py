#!/usr/bin/env python

from fabric.api import run, env
import sqlsoup
import sqlalchemy
import time
import sys
import random


def _connect(**kwargs):
    url = "{driver}://{username}:{password}@{dbhost}/{database}".format(**kwargs)
    print("Connecting to {}".format(url))
    return sqlsoup.SQLSoup(url)


def setup(driver='mysql', username='root', password='', dbhost='localhost',
            port='3307', database='test', table='users', howmany=2000):
    """Creates table if it does not exist, and create 2000 fake users."""
    db = _connect(driver=driver, username=username, password=password,
                  dbhost=dbhost, port=port, database=database)
    try:
        users = getattr(db, table)
    except sqlalchemy.exc.NoSuchTableError:
        db.execute("""CREATE TABLE {} (
            user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(30),
            last_name VARCHAR(50)
        );""".format(table))
        while True:
            try:
                users = getattr(db, table)
            except sqlsoup.SQLSoupError:
                sys.stdout.write('.')
                sys.stdout.flush()
                db = _connect(driver=driver, username=username,
                              password=password, dbhost=dbhost, port=port,
                              database=database)
                time.sleep(1)
            else:
                print("")
                break

    with open("male-names") as fn:
        first_names = fn.readlines()
    with open("other-names") as on:
        last_names = on.readlines()

    for i in range(int(howmany)):
        user = users.insert(
            first_name=random.choice(first_names).strip().title(),
            last_name=random.choice(last_names).strip().title()
        )
        db.flush()
        print("Created user {}: {} {}".format(
            user.user_id,
            user.first_name,
            user.last_name
        ))
    db.commit()


def drop(driver='mysql', username='root', password='', dbhost='localhost',
         port='3307', database='test', table='users'):
    """Drop table"""
    db = _connect(driver=driver, username=username, password=password,
                  dbhost=dbhost, port=port, database=database)
    db.execute("""DROP TABLE {};""".format(table))


def _get_user_range_generator(users, start, end):
    """Assignment requires a generator. Boring... :-)"""
    user_id = users.c['user_id']
    for user in users.filter(user_id<=end).filter(user_id>=start)\
        .order_by(users.first_name, users.last_name).all():
        yield user


def getrange(driver='mysql', username='root', password='', dbhost='localhost',
            port='3307', database='test', table='users', start=1234, end=1334):
    """Get a range of users based on user_id, default between 1234 and 1334"""
    db = _connect(driver=driver, username=username, password=password,
                  dbhost=dbhost, port=port, database=database)
    users = getattr(db, table)
    for user in _get_user_range_generator(users, start, end):
        print("{}\t{} {}".format(
            user.user_id,
            user.first_name,
            user.last_name
        ))

def arguments():
    """List arguments and defaults"""
    print(
"""
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
"""
    )