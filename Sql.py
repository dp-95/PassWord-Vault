# -*- coding: utf-8 -*-
# @Author: _dp95
import mysql.connector

connection_args = {
        'host' : 'localhost',
        'user' : 'root',
        'password' : '9867'
    }

def get_Connection():
    return mysql.connector.connect( **connection_args, raw=True )

def commit_changes( sql_connection ):
    sql_connection.commit()

def setup( sql_cursor ):
    sql_cursor.execute("""
    create database if not exists test;
    """)

    sql_cursor.execute("""
    use test;
    """)
    
    sql_cursor.execute("""
    create table if not exists users(
        username varchar(20) PRIMARY KEY,
        password_salt binary(16) NOT NULL,
        password char(40) NOT NULL );
    """)
    
    sql_cursor.execute("""
    create table if not exists datastore(
        username varchar(20),
        account_name varchar(40),
        account_pwd char(40),
        FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE );
    """)
