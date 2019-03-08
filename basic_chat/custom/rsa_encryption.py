from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from base64 import b64decode,b64encode

class RSAEncrypt(object):
	"""docstring for RSAEncrypt"""
	# by default a 1024 bit encryption if the bit size is not given
	def __init__(self, key_size=1024):
		super(RSAEncrypt, self).__init__()
		# key size is in number of bits
		self.key_size = key_size

	def setKeySize(self,key_size):
		self.key_size = key_size

	def getKeySize(self):
		return self.key_size

	def getKeySizeUnit(self):
		return 'bits'

	def generateKeyPair(self):
		# self.gen()
		# 1024 means the keysize will be 1024 bits
		key_pair = RSA.generate(self.key_size)
		# storing only the key value in the dictionary
		self.key_pair = [RSA.importKey(key_pair.exportKey()),RSA.importKey(key_pair.publickey().exportKey())]
		# self.key_pair = [key_pair.exportKey(),key_pair.publickey().exportKey()]
		return self.key_pair
	def gen(self):
		key_pair = RSA.generate(1024)
		private_key = open("privatekey.pem", "wb")
		private_key.write(key_pair.exportKey())
		private_key.close()
		public_key = open("public_key.pem", "wb")
		public_key.write(key_pair.publickey().exportKey())
		public_key.close()

	def setPrivateKey(self,private_key):
		self.key_pair[0] = private_key

	def setPublicKey(self,public_key):
		self.key_pair[1] = public_key

	def getPrivateKey(self):
		return self.key_pair[0]
		# return RSA.importKey(self.key_pair[0])

	def getPublicKey(self):
		return self.key_pair[1]
		# return RSA.importKey(self.key_pair[1])

	def encrypt(self,msg):

		# Encrypt the session key with the public RSA key
		cipher_rsa = PKCS1_OAEP.new(self.key_pair[1],hashAlgo=SHA256)
		encrypt_data = cipher_rsa.encrypt(msg)
		# msg = b64encode(msg)
		# encrypt_data = cipher_rsa.encrypt(msg)
		return encrypt_data
	def decrypt(self,msg):	
		key = self.key_pair[0]
		cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
		# decrypted_message = cipher.decrypt(b64decode(msg))
		decrypted_message = cipher.decrypt(msg)
		return decrypted_message
# def main():
	
# 	# rsa = RSAEncrypt()
# 	# rsa.generateKeyPair()

# 	# print(rsa.getPublicKey())
# 	# key = b"I love you you you you "
# 	# enc = rsa.encrypt(key)

# 	# print('encrypted data : ',enc)
# 	# dec = rsa.decrypt(enc)		
# 	# print('Decrypted data : ',dec)


# 	trydecrypt()
# main()

class PublicKey(object):
	"""docstring for PublicKey"""
	def __init__(self, key=None):
		super(PublicKey, self).__init__()
		self.public_key = key
	def setPublicKey(self,key):
		self.public_key = key