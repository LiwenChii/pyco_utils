import os
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA, SHA256
from Crypto.PublicKey import RSA
from base64 import encodebytes, decodebytes
from urllib.parse import quote_plus


def rsa_key(file, path=''):
    if path != '':
        file = os.path.join(path, file)
    with open(file) as f:
        key = f.read()
        return RSA.importKey(key)


def rsa_sign(content, private_key, type='SHA256'):
    """
    通过如下方法调试签名
    方法1
        key = rsa.PrivateKey.load_pkcs1(open(self._app_private_key_path).read())
        sign = rsa.sign(unsigned_string.encode("utf8"), key, "SHA-1")
        # base64 编码，转换为unicode表示并移除回车
        sign = base64.encodebytes(sign).decode("utf8").replace("\n", "")
    方法2
        key = RSA.importKey(open(self._app_private_key_path).read())
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
        # base64 编码，转换为unicode表示并移除回车
        sign = base64.encodebytes(signature).decode("utf8").replace("\n", "")
    方法3
        echo "abc" | openssl sha1 -sign alipay.key | openssl base64
    """
    content.encode('utf8')
    signer = PKCS1_v1_5.new(private_key)
    if type.upper() == 'SHA256':
        mhash = SHA256.new(content)
    else:
        mhash = SHA.new(content)
    bytes = signer.sign(mhash)
    text = encodebytes(bytes).decode("utf8").replace("\n", "")
    return text


def rsa_verify(content, signature, public_key, type='SHA256'):
    # 验证签名
    signer = PKCS1_v1_5.new(public_key)
    if type.upper() == 'SHA256':
        mhash = SHA256.new(content)
    else:
        mhash = SHA.new(content)
    s = decodebytes(signature.encode("utf8"))
    return signer.verify(mhash, s)


def sorted_fields(data):
    m = sorted([k, v] for k, v in data.items())
    return m


def signed_form(data, private_key):
    data.pop("sign", None)
    # 排序后的字符串
    fields = sorted_fields(data)
    unsigned_string = "&".join("{}={}".format(k, v) for k, v in fields)
    sign = rsa_sign(unsigned_string, private_key)

    # 获得最终的订单信息字符串
    quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in fields)
    signed_string = quoted_string + "&sign=" + quote_plus(sign)
    return signed_string
