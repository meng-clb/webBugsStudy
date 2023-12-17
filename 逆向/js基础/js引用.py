# 在python中链接CMD的那个东西是subprocess里面的Popen
# 解决execjs的问题
# 在引入execjs之前, 加上以下代码
import subprocess
from functools import partial  # 作用, 用来锁定某个参数的固定值

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

import execjs  # 用的是node.js

f = open('test.js', 'r', encoding='utf-8')
all_js_code = f.read()
# 加载js
js = execjs.compile(all_js_code)
# 调用该函数
r = js.call('fn', 'clb_jj_cc')
print(r)
