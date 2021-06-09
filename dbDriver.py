# -*- coding: utf-8 -*-
"""
Python 3.8
@author: juan.cruz2

"""

import mysql.connector

def error_handler(err, title):
    tkinter.messagebox.showerror("Report - Conn error: "+ title , err)

def success_handler(title,message):
    tkinter.messagebox.showinfo("Report - " + title,message)

def mysqlconnect(mysqlserver,mysqlusername,mysqlpsw):
    mysqldatabase = 'information_schema'
    config = {
    'user': mysqlusername,
    'database': mysqldatabase,
    'password': mysqlpsw,
    'host': mysqlserver,
    }

    try:
        mysqlconn = mysql.connector.connect(**config)
        return mysqlconn
    except mysql.connector.Error as err:
        error_handler(err,"Internal - Databases")
