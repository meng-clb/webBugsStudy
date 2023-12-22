# Cipher包内有各种加密器
from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad, unpad

"""
# 1. 创建AES对象
# 最常使用的两个模式
# MODE_ECB -> 不需要iv
# MODE_CBC -> 需要iv
aes = AES.new(key=b'1234567890145632', mode=AES.MODE_CBC, iv=b'adghunheniuihdws')

# 2. 加密一段数据
s = '这是一段文字, 我要对其进行加密.'
bs = s.encode('utf-8')
# pad: 字节长度填充到16的倍数
bs = pad(bs, 16)
result = aes.encrypt(bs)  # 加密后的字节是杂乱无章的字节
# 加密后的字节转化为base64的字符串
ss = base64.b64encode(result).decode()
print(ss)
"""

# 加密后的数据: NFdFvIiNjx+xKLPC/aWN2nP1thoIYmC/6jJOitzmlhEITFsxSG9pApia+6m52WdL
# 解密
# 1. 创建aes对象
aes = AES.new(key=b'1234567890145632', mode=AES.MODE_CBC, iv=b'adghunheniuihdws')
s = 'NFdFvIiNjx+xKLPC/aWN2nP1thoIYmC/6jJOitzmlhEITFsxSG9pApia+6m52WdL'  # 加密后的数据
# 使用base64还原为原来的字节
s = base64.b64decode(s)
# 使用aes对其进行解密
result = aes.decrypt(s)
# 使用unpad还原原来的字节长度
result = unpad(result, 16).decode('utf-8')
print(result)
