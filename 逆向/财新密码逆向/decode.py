from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad, unpad

aes = AES.new(key=b'G3JH98Y8MY9GWKWG', mode=AES.MODE_ECB)

t = '111111'
bs = t.encode('utf-8')
bs = pad(bs, 16)
result = aes.encrypt(bs)
b64 = base64.b64encode(result)
print(b64.decode())
