from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

# 创建秘钥
# key = RSA.generate(2048)  # 创建秘钥
# private_key = key.export_key()  # 导出私钥
# public_key = key.public_key().export_key()  # 导出公钥
# print(private_key.decode())
# print(public_key.decode())

# 公钥存入文件, 用来加密数据
# with open('public_key.pem', 'w', encoding='utf-8') as f:
# 	f.write(public_key.decode())

# 用来加密数据
s = '我是要加密的数据.'
# 加载秘钥(公钥)
public_key = RSA.import_key(open('public_key.pem', 'rb').read())
# 创建加密器
rsa = PKCS1_v1_5.new(public_key)
# 加密数据
result = rsa.encrypt(s.encode('utf-8'))
# 对加密的数据进行bs64编码
bs = base64.b64encode(result)
print(bs.decode())
