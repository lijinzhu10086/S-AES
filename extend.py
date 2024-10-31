from main import *

# 将ASCII字符串转换为二进制字符串
def ascii_to_binary(ascii_text):
    binary_text = ''
    for char in ascii_text:
        binary_char = bin(ord(char))[2:].zfill(8)
        binary_text += binary_char
    return binary_text

# 将二进制字符串转换为ASCII字符串
def binary_to_ascii(binary_text):
    ascii_text = ''
    for i in range(0, len(binary_text), 8):
        ascii_char = chr(int(binary_text[i:i+8], 2))
        ascii_text += ascii_char
    return ascii_text

# 实现扩展加密功能，输入是16位ASCII码字符串，密钥是16位2进制字符串，输出是16位ASCII码字符串
def ascii_encrypt(plain_text, key):
    new = ''
    for i in range(0, len(plain_text), 2):
        # 将明文转换为2进制字符串
        char = ascii_to_binary(plain_text[i])
        char += ascii_to_binary(plain_text[i+1])
        # 执行加密
        char = Encrypt(char, key)
        # 将密文转换为ASCII码字符串
        char = binary_to_ascii(char)
        new += char
    return new

# 实现解密功能，输入是16位ASCII码字符串，密钥是16位2进制字符串，输出是16位ASCII码字符串
def ascii_decrypt(cipher_text, key):
    new = ''
    for i in range(0, len(cipher_text), 2):
        # 将密文转换为2进制字符串
        char = ascii_to_binary(cipher_text[i])
        char += ascii_to_binary(cipher_text[i+1])
        # 执行解密
        char = Decrypt(char, key)
        # 将明文转换为ASCII码字符串
        char = binary_to_ascii(char)
        new += char
    return new

