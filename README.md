# PassWord-Vault
 PassWord-Vault is a simple python CLI that allows you to securely store passwords.
 
 ## Features

 - Passwords are stored in an MySQL database.
 - Within the database, each password is encrypted with a unique salt using AES-128 encryption with [Python Cryptography Toolkit (pycrypto)](https://pypi.org/project/pycrypto/)
 - Multiple users account can be created.
 - Master key is hashed (SHA) with a random salt for each user.

## Basic usage
![Demo](https://github.com/dp-95/PassWord-Vault/blob/master/demo.gif?raw=true)

## Database
![Demo](https://github.com/dp-95/PassWord-Vault/blob/master/MySQL-DataBase.gif?raw=true)
