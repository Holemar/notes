/**
 * RC4 加解密
 * Created on 2018/6/11
 * Updated on 2018/6/11
 * @author: 冯万里 Holemar
 * 交流QQ群:26651479
 *
 * 加密后转成16进制字符串存储
 */


function rc4(data, key) {
    /**
     * rc4加解密的核心算法
     */
    var x = 0;
    var box = Array(256);
    var das = Array(data.length);
    for (var i = 0; i < 256; i++) {
        box[i] = i;
    }
    for (var i = 0; i < 256; i++) {
        x = (x + box[i] + key.charCodeAt(i % key.length)) % 256;
        var temp = box[i];
        box[i] = box[x];
        box[x] = temp;
    }
    for (var i = 0; i < data.length; i++) {
        das[i] = data.charCodeAt(i)
    }
    var i = 0;
    var j = 0;
    for (var x = 0; x < das.length; x++) {
        i = (i + 1) % 256;
        j = (j + box[i]) % 256;
        var temp = box[i];
        box[i] = box[j];
        box[j] = temp;
        var k = (box[i] + (box[j] % 256)) % 256;
        das[x] = String.fromCharCode(das[x] ^ box[k])
    }
    return das.join('');
}

function str2hex(str) {
    /**字符串转换为十六进制*/
    var val = Array();
    for(var i = 0;i < str.length; i++){
        var hex_dig = str.charCodeAt(i).toString(16);
        if (hex_dig.length == 1) {
            hex_dig = "0" + hex_dig
        }
        val.push(hex_dig);
    }
    return val.join('');
}

function hex2str(str) {
    /**十六进制转换为字符串*/
    var val = Array();
    var arr = str.split("");
    for(var i = 0;i < arr.length; i++){
        var hex_dig = String.fromCharCode(parseInt(arr[i] + arr[i+1], 16));
        val.push(hex_dig);
        i++;
    }
    return val.join('');
}

function to_utf8(text) {
    /**
     * 中文转换，将 unicode 编码转成 utf-8 编码
     * @param {string} text: 原字符串
     * @return {string}: 返回转换后的字符串
     */
    var val = Array();
    var arr = encodeURIComponent(text);
    for(var i = 0;i < arr.length; i++) {
        var value = arr[i];
        var hex_dig = value;
        if (value == '%') {
            value = arr.slice(i+1,i+3);
            hex_dig = String.fromCharCode(parseInt(value, 16));
            i += 2;
        }
        val.push(hex_dig);
    }
    return val.join('');
}

function to_unicode(text) {
    /**
     * 中文转换，将 utf-8 编码转成 unicode 编码
     * @param {string} text: 原字符串
     * @return {string}: 返回转换后的字符串
     */
    var val = Array();
    for (var i = 0;i < text.length; i++) {
        var hex_dig = text.charCodeAt(i).toString(16);
        val.push('%'+hex_dig);
    }
    return decodeURIComponent(val.join(''));
}

function decode(rc4_txt, key) {
    /**
     * 将rc4加密后的密文，解密出来
     * @param {string} rc4_txt: RC4加密后的密文
     * @param {string} key: 加密/解密的key值
     * @return {string}: 返回解密后的明文
     */
    key = to_utf8(key) // 为了兼容中文密钥的加解密
    real_text = rc4(hex2str(rc4_txt), key)
    // 如果加密字符串里面没有中文，上面的结果 real_text 已经可以直接返回。下面为了兼容中文内容。
    return to_unicode(real_text);
}

function encode(real_text, key) {
    /**
     * 将明文字符串，用RC4加密成密文
     * @param {string} real_text: 明文的字符串
     * @param {string} key: 加密/解密的key值
     * @return {string}: 返回加密后的密文
     */
    real_text = to_utf8(real_text) // 为了兼容中文的加密
    key = to_utf8(key) // 为了兼容中文密钥的加解密
    return str2hex(rc4(real_text, key))
}


/* 测试代码
var key = "1bb76哼2哈f7ce24ceee"
var txt = '1哼23哈哈e'

var secret_txt = encode(txt, key)
alert(secret_txt);

var rc4_txt = decode(secret_txt, key)
alert(rc4_txt);
alert(txt == rc4_txt);

*/