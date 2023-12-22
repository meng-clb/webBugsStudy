/**
 * 网站: https://bqcm0.cavip1.com/
 * 功能: 登录加密模拟
 * 在当前文件夹下安装js模块
 * 安装crypto-js模块, npm install crypto-js 加密模块
 * */

// 安装crypto-js模块, npm install crypto-js 加密模块
var CryptoJS = require('crypto-js')

// 获取到一个随机值, 随机值可以固定
function random_i() {
    for (var e = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz", t = "", n = 0; n < 16; n++) {
        var a = Math.floor(Math.random() * e.length);
        t += e.substring(a, a + 1)
    }
    return t
}

// 加密过程
function encrypt(e, t) {
    var n = CryptoJS.enc.Utf8.parse(t);
    return CryptoJS.DES.encrypt(e, n, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    }).toString()
}

e = '{"username":"fsa2134234","password":"123dsfg","captcha":"95178"}'
t = "bpCkd1QvTqG9321C"  // random_i
code = encrypt(e,t)
console.log(code)


