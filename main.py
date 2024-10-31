# 定义S盒
S = [[9, 4, 10, 11],
     [13, 1, 8, 5],
     [6, 2, 0, 3],
     [12, 14, 15, 7]]

# 定义逆S盒
IS = [[10, 5, 9, 11],
      [1, 7, 8, 15],
      [6, 0, 2, 3],
      [12, 4, 13, 14]]

# 定义轮常数
RCON1 = '10000000'
RCON2 = '00110000'

# 实现异或运算，输入两个字符串，输出一个字符串
def XOR(bits1, bits2):
    new = ''
    for bit1, bit2 in zip(bits1, bits2):
        new += str(((int(bit1) + int(bit2)) % 2))
    return new


# 实现密钥加，输入两个字符串，输出一个字符串
def AddRoundKey(bits1, bits2):
    new = ''
    for bit1, bit2 in zip(bits1, bits2):
        new += str(((int(bit1) + int(bit2)) % 2))
    return new

# 实现半字节代替，输入一个16位字符串，输出一个16位字符串
def SubNib(bits):
    new = ''
    for i in range(0, len(bits), 4):
        new += str(bin(S[int(bits[i:i + 2], 2)]
                   [int(bits[i + 2:i + 4], 2)])[2:].zfill(4))
    return new

# 实现逆半字节代替，输入一个16位字符串，输出一个16位字符串
def InvSubNib(bits):
    new = ''
    for i in range(0, len(bits), 4):
        new += str(bin(IS[int(bits[i:i + 2], 2)]
                   [int(bits[i + 2:i + 4], 2)])[2:].zfill(4))
    return new

# 实现行移位，输入一个16位字符串，输出一个16位字符串
def ShiftRows(bits):
    new = bits[0:4] + bits[12:16] + bits[8:12] + bits[4:8]
    return new

# 实现左移，输入一个8位字符串，输出一个8位字符串
def RotNib(bits):
    new = bits[4:8] + bits[0:4]
    return new

# 实现GF(2^4)上的乘法，输入两个4位字符串，输出一个4位字符串
def GF(a, b):
    # 定义GF(2^4)上的乘法表
    mul_table = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [0, 2, 4, 6, 8, 10, 12, 14, 3, 1, 7, 5, 11, 9, 15, 13],
        [0, 3, 6, 5, 12, 15, 10, 9, 11, 8, 13, 14, 7, 4, 1, 2],
        [0, 4, 8, 12, 3, 7, 11, 15, 6, 2, 14, 10, 5, 1, 13, 9],
        [0, 5, 10, 15, 7, 2, 13, 8, 14, 11, 4, 1, 9, 12, 3, 6],
        [0, 6, 12, 10, 11, 13, 7, 1, 5, 3, 9, 15, 14, 8, 2, 4],
        [0, 7, 14, 9, 15, 8, 1, 6, 13, 10, 3, 4, 2, 5, 12, 11],
        [0, 8, 3, 11, 6, 14, 5, 13, 12, 4, 15, 7, 10, 2, 9, 1],
        [0, 9, 1, 8, 2, 11, 3, 10, 4, 13, 5, 12, 6, 15, 7, 14],
        [0, 10, 7, 13, 14, 4, 9, 3, 15, 5, 8, 2, 1, 11, 6, 12],
        [0, 11, 5, 14, 10, 1, 15, 4, 7, 12, 2, 9, 13, 6, 8, 3],
        [0, 12, 11, 7, 5, 9, 14, 2, 10, 6, 1, 13, 15, 3, 4, 8],
        [0, 13, 9, 4, 1, 12, 8, 5, 2, 15, 11, 6, 3, 14, 10, 7],
        [0, 14, 15, 1, 13, 3, 2, 12, 9, 7, 6, 8, 4, 10, 11, 5],
        [0, 15, 13, 2, 9, 6, 4, 11, 1, 14, 12, 3, 8, 7, 5, 10]
    ]
    # 执行乘法运算
    result_int = mul_table[int(a, 2)][int(b, 2)]
    # 将结果转换为4位的二进制字符串
    result_str = bin(result_int)[2:].zfill(4)
    return result_str

def MixColumns(bits):
    new = XOR(bits[0:4], GF('0100', bits[4:8])) + XOR(GF('0100', bits[0:4]), bits[4:8]) + \
        XOR(bits[8:12], GF('0100', bits[12:16])) + \
        XOR(GF('0100', bits[8:12]), bits[12:16])
    return new

def InvMixColumns(bits):
    new = XOR(GF('1001', bits[0:4]), GF('0010', bits[4:8])) + XOR(GF('0010', bits[0:4]), GF('1001', bits[4:8])) + XOR(
        GF('1001', bits[8:12]), GF('0010', bits[12:16])) + XOR(GF('0010', bits[8:12]), GF('1001', bits[12:16]))
    return new

# 实现密钥扩展，输入一个16位字符串，输出一个列表，列表中的每个元素为一个16位字符串
def KeyExpansion(key):
    [w0, w1] = [key[0:8], key[8:16]]
    w2 = XOR(w0, XOR(RCON1, SubNib(RotNib(w1))))
    w3 = XOR(w2, w1)
    w4 = XOR(w2, XOR(RCON2, SubNib(RotNib(w3))))
    w5 = XOR(w4, w3)
    return [w0 + w1, w2 + w3, w4 + w5]

# 实现加密
def Encrypt(plain_text, key):
    # 密钥扩展
    expanded_key = KeyExpansion(key)
    # 密钥加
    cipher_text = AddRoundKey(plain_text, expanded_key[0])
    # 轮函数
    cipher_text = SubNib(cipher_text)
    cipher_text = ShiftRows(cipher_text)
    cipher_text = MixColumns(cipher_text)
    # 密钥加
    cipher_text = AddRoundKey(cipher_text, expanded_key[1])
    # 轮函数
    cipher_text = SubNib(cipher_text)
    cipher_text = ShiftRows(cipher_text)
    # 密钥加
    cipher_text = AddRoundKey(cipher_text, expanded_key[2])
    return cipher_text

# 实现解密
def Decrypt(cipher_text, key):
    # 密钥扩展
    expanded_key = KeyExpansion(key)
    # 密钥加
    plain_text = AddRoundKey(cipher_text, expanded_key[2])
    # 轮函数
    plain_text = ShiftRows(plain_text)
    plain_text = InvSubNib(plain_text)
    # 密钥加
    plain_text = AddRoundKey(plain_text, expanded_key[1])
    plain_text = InvMixColumns(plain_text)
    # 轮函数
    plain_text = ShiftRows(plain_text)
    plain_text = InvSubNib(plain_text)
    # 密钥加
    plain_text = AddRoundKey(plain_text, expanded_key[0])
    return plain_text


