# -*- coding: utf-8 -*-
# @Author: _dp95
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA

IV_SIZE = 16    
KEY_SIZE = 16
SALT_SIZE = 16

class EnCrypt:

    def __init__(self, password, salt):
        derived = hashlib.pbkdf2_hmac('sha1', password, salt, 100000,dklen=IV_SIZE + KEY_SIZE)
        self.iv = derived[0:IV_SIZE]
        self.key = derived[IV_SIZE:]
        self.salt = salt

    def get_encrypted( self, text ):
        encrypted = self.salt + AES.new( self.key, AES.MODE_CFB, self.iv).encrypt( text )
        return base64.b64encode(encrypted)

    def get_decrypted( self, text ):
        text = base64.b64decode(text)
        text = AES.new(self.key, AES.MODE_CFB, self.iv).decrypt(text[SALT_SIZE:])
        return  text

    def p(self):
        print("OK:)")
        return

def get_hashed_pwd( salt, password ):
	salt_password = password + str(salt)
	return SHA.new(salt_password.encode()).hexdigest()
