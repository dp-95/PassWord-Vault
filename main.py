# -*- coding: utf-8 -*-
# @Author: _dp95
# @Date:   2020-08-23 17:53:23

import Cypher
import Sql
import os

cypher = None
username = None
sql_connection = None
cursor = None

def clear_screen():
	os.system("clear")

def view_details( one ):
    clear_screen()
    global username
    global cypher
    global cursor
    print("-----------------------------")
    print("          RECORDS")
    print("-----------------------------")
    if one == True:
        account_name = input("Enter account name : ")
        query = "select * from datastore where username=%s and account_name= %s;"
        vals = (username,account_name,)
    else:
        query = "select * from datastore where username=%s ;"
        vals = (username,)
    cursor.execute(query,vals)
    result = cursor.fetchall()
    row = cursor.rowcount
    if row==0:
        print("NO MATCHING RECORDS FOUND!!")
        print("-----------------------------")
        tmp = input("PRESS ENTER TO CONTINUE")
        return
    clear_screen()
    print("-----------------------------")
    print("          RECORDS")
    print("-----------------------------")
    for item in result:
        username,account_name,account_pwd = item
        account_name = bytes(account_name).decode()
        account_pwd = cypher.get_decrypted(account_pwd).decode()
        print("Account_name :", account_name )
        print("Account_pwd  :", account_pwd  )
        print("     ----------------        ")
    print("-----------------------------")
    tmp = input("PRESS ENTER TO CONTINUE")

def insert_details( ):
    clear_screen()
    global username
    global cypher
    global cursor
    print("-----------------------------")
    print("          INSERT")
    print("-----------------------------")
    account_name = input("Account_name : ")
    account_pwd = input( "Account_pwd : ")
    query = "insert into datastore values (%s,%s,%s);"
    account_pwd = cypher.get_encrypted(account_pwd)
    vals = (username,account_name,account_pwd,)
    cursor.execute(query,vals)
    rows = cursor.rowcount
    if rows==0:
        print("INSERT FAILED !!")
        return
    else:
        print("INSERT SUCCESSFULL")
    print("-----------------------------")
    tmp = input("PRESS ENTER TO CONTINUE")

def update_details( ):
    global username
    global cypher
    global cursor
    clear_screen()
    print("-----------------------------")
    print("          UPDATE")
    print("-----------------------------")
    prev_account_name = input("Account_name : ")
    account_name = input("New Account_name : ")
    account_pwd = input("New Account_pwd : ")
    account_pwd = cypher.get_encrypted(account_pwd)
    query = """
        update datastore
        set account_name = %s, account_pwd = %s 
        where username = %s and account_name = %s ;
        """;
    vals = (account_name,account_pwd,username,prev_account_name,)
    cursor.execute(query,vals)
    rows = cursor.rowcount
    if rows==0:
        print("NO SUCH RECORDS FOUND!!")
        return
    else:
        print("UPDATE SUCCESSFULL")
    print("-----------------------------")
    tmp = input("PRESS ENTER TO CONTINUE")

def delete_details( ):
    global username
    global cursor
    clear_screen()
    print("-----------------------------")
    print("          DELETE")
    print("-----------------------------")
    account_name = input("Account_name : ")
    query = "Delete from datastore where username=%s and account_name=%s;"
    vals = (username,account_name,)
    cursor.execute(query,vals)
    rows = cursor.rowcount
    if rows==0:
        print("NO SUCH RECORDS FOUND!!")
        return
    else:
        print("DELETE SUCCESSFULL")
    print("-----------------------------")
    tmp = input("PRESS ENTER TO CONTINUE")


def home( ):
	global cursor
	while True:
		clear_screen()
		print("-----------------------------")
		print("          MENU")
		print("-----------------------------")
		print("1. View single account details\n2. View all account details")
		print("3. Insert new account\n4. Delete an account\n5. Update an account\n6. LOG-OUT")
		print("-----------------------------")
		choice = int(input())
		if choice==1:
			view_details( True )
		elif choice==2:
			view_details( False )
		elif choice==3:
			insert_details( )
		elif choice==4:
			delete_details( )
		elif choice==5:
			update_details( )
		elif choice==6:
			return
		else:
			print("Enter a valid choice!!")

def login( ):
    clear_screen()
    global cypher
    global username
    global cursor
    print("-----------------------------")
    print("          LOGIN")
    print("-----------------------------")
    username = input("Username : ")
    password = input("Password : ")
    query = "select * from users where username = %s ;"
    val = (username,)
    cursor.execute(query,val)
    result = cursor.fetchone()

    if result is None:
        print("INVALID USERNAME OR PASSWORD !!!")
        print("-----------------------------")
        tmp = input("PRESS ENTER TO RETURN TO MAIN MENU")
        return

    salt = bytes(result[1])
    stored_pwd = bytes(result[2]).decode()
    hashed_pwd = Cypher.get_hashed_pwd( salt, password )
    if hashed_pwd==stored_pwd:
        cypher = Cypher.EnCrypt( password.encode(), salt )
        password = None
        home()
        cypher = None
    else:
        print("INVALID USERNAME OR PASSWORD !!!")
        print("-----------------------------")
        tmp = input("PRESS ENTER TO RETURN TO MAIN MENU")

def show_users( ):
	global cursor
	clear_screen()
	cursor.execute("""
		select username from users;
		""")
	index=1
	print("-----------------------------")
	print("          USERS")
	print("-----------------------------")
	for item in cursor:
		print(str(index)+") "+item[0].decode())
		index+=1
	print("-----------------------------")
	tmp = input("PRESS ENTER TO CONTINUE")

def sign_up( ):
	global cursor
	clear_screen()
	print("-----------------------------")
	print("          SIGN-UP")
	print("-----------------------------")
	username = input("Username : ")
	password1 = input("Password : ")
	password2 = input( "Verify Password : ")
	if password1!=password2:
		print("Passwords do not match!!")
		return
	salt = Crypto.Random.get_random_bytes(16)
	password = password1+str(salt)
	password = SHA.new(password.encode()).hexdigest()
	val = (username,salt,password)
	query = "insert into users values(%s,%s,%s);"
	cursor.execute(query,val)
	rows = cursor.rowcount
	print("-----------------------------")
	if rows==0:
		print("SIGN_UP FAILED!! PLEASE TRY AGAIN :(")
		return
	else:
		print("SIGN_UP SUCCESSFULL")
	print("-----------------------------")
	tmp = input("PRESS ENTER TO CONTINUE")

sql_connection = Sql.get_Connection()
cursor = sql_connection.cursor()
Sql.setup(cursor)

while True:
	clear_screen()
	cypher = None
	username = None
	choice = int(input("1. LOGIN\n2. SIGN-UP\n3. SHOW USERS\n4. EXIT\n"))
	if choice==1:
		login()
	elif choice==2:
		sign_up()
	elif choice==3:
		show_users()
	elif choice==4:
		Sql.commit_changes(sql_connection)
		exit(0)
	else:
		print("Please Enter a valid option!!\n")
