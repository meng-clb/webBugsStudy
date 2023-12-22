from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# 1. 创建des对象
des = DES.new(key=b'ahurt5h7', mode=DES.MODE_CBC, iv=b'hu765f3j')

# s = '需要加密的文字.'
# s = pad(s.encode('utf-8'), 8)
# 加密方法的使用
# mi = des.encrypt(s)
# print(mi)

# 解密
s = b'" u\xe2\x85oB/\xdf\xbfehq\x1eC\x08MZ\xdeVZ\xb7y\xba'
s = des.decrypt(s)
s = unpad(s, 8).decode('utf-8')
print(s)
