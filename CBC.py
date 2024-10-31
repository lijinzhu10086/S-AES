import tkinter as tk
from tkinter import messagebox
from main import *

# 实现密码分组链模式，输入明文字符串，16位2进制密钥，16位2进制初始向量，输出密文字符串
def CBC_encrypt(plain_text, key, IV):
    # 将明文分组
    plain_text_list = [plain_text[i:i + 16] for i in range(0, len(plain_text), 16)]
    # 用于存储密文
    cipher_text_list = []
    # 对每个分组进行加密
    for plain_text_block in plain_text_list:
        # 执行加密
        cipher_text_block = Encrypt(XOR(plain_text_block, IV), key)
        # 更新初始向量
        IV = cipher_text_block
        # 将密文添加到密文列表
        cipher_text_list.append(cipher_text_block)
    # 将密文列表转换为字符串
    cipher_text = ''.join(cipher_text_list)
    return cipher_text

# 实现密码分组链模式的解密
def CBC_decrypt(cipher_text, key, IV):
    # 将密文分组
    cipher_text_list = [cipher_text[i:i + 16] for i in range(0, len(cipher_text), 16)]
    # 用于存储明文
    plain_text_list = []
    # 对每个分组进行解密
    for cipher_text_block in cipher_text_list:
        # 执行解密
        plain_text_block = XOR(Decrypt(cipher_text_block, key), IV)
        # 更新初始向量
        IV = cipher_text_block
        # 将明文添加到明文列表
        plain_text_list.append(plain_text_block)
    # 将明文列表转换为字符串
    plain_text = ''.join(plain_text_list)
    return plain_text

# 测试密码分组链模式加密解密
def test_CBC():
    # 获取用户输入
    plain_text = plain_text_entry.get()
    key = key_entry.get()
    IV = iv_entry.get()

    # 检查输入长度
    if len(plain_text) % 16 != 0 or len(key) != 16 or len(IV) != 16:
        messagebox.showerror("错误", "明文长度必须是16的倍数，密钥和初始向量必须是16位")
        return

    # 加密
    cipher_text = CBC_encrypt(plain_text, key, IV)
    cipher_text_entry.delete(0, tk.END)
    cipher_text_entry.insert(0, cipher_text)

    # 解密
    decrypted_text = CBC_decrypt(cipher_text, key, IV)
    decrypted_text_entry.delete(0, tk.END)
    decrypted_text_entry.insert(0, decrypted_text)

    # 比较
    if decrypted_text == plain_text:
        result_label.config(text="密码分组链模式加密解密成功")
    else:
        result_label.config(text="密码分组链模式加密解密失败")

# 替换或修改密文分组
def tamper_cipher_text():
    cipher_text = cipher_text_entry.get()
    position = int(position_entry.get())
    new_block = tamper_entry.get()

    if position < 0 or position >= len(cipher_text) // 16 or len(new_block) != 16:
        messagebox.showerror("错误", "位置或新分组不合法")
        return

    # 替换密文分组
    start = position * 16
    end = start + 16
    tampered_cipher_text = cipher_text[:start] + new_block + cipher_text[end:]
    cipher_text_entry.delete(0, tk.END)
    cipher_text_entry.insert(0, tampered_cipher_text)

    # 解密篡改后的密文
    key = key_entry.get()
    IV = iv_entry.get()
    tampered_decrypted_text = CBC_decrypt(tampered_cipher_text, key, IV)
    tampered_decrypted_text_entry.delete(0, tk.END)
    tampered_decrypted_text_entry.insert(0, tampered_decrypted_text)

    # 显示篡改后的密文
    tampered_cipher_text_entry.delete(0, tk.END)
    tampered_cipher_text_entry.insert(0, tampered_cipher_text)

# 创建主窗口
root = tk.Tk()
root.title("S-AES CBC 加密解密工具")

# 明文输入
tk.Label(root, text="明文：").grid(row=0, column=0, padx=10, pady=5)
plain_text_entry = tk.Entry(root, width=80)
plain_text_entry.grid(row=0, column=1, padx=10, pady=5)

# 密钥输入
tk.Label(root, text="密钥：").grid(row=1, column=0, padx=10, pady=5)
key_entry = tk.Entry(root, width=80)
key_entry.grid(row=1, column=1, padx=10, pady=5)

# 初始向量输入
tk.Label(root, text="初始向量：").grid(row=2, column=0, padx=10, pady=5)
iv_entry = tk.Entry(root, width=80)
iv_entry.grid(row=2, column=1, padx=10, pady=5)

# 加密按钮
encrypt_button = tk.Button(root, text="加密", command=test_CBC, bg='#4CAF50')
encrypt_button.grid(row=3, column=0, columnspan=2, pady=10)

# 密文显示
tk.Label(root, text="密文：").grid(row=4, column=0, padx=10, pady=5)
cipher_text_entry = tk.Entry(root, width=80)
cipher_text_entry.grid(row=4, column=1, padx=10, pady=5)

# 解密结果显示
tk.Label(root, text="解密结果：").grid(row=5, column=0, padx=10, pady=5)
decrypted_text_entry = tk.Entry(root, width=80)
decrypted_text_entry.grid(row=5, column=1, padx=10, pady=5)

# 结果标签
result_label = tk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=2, pady=10)

# 篡改密文
tk.Label(root, text="篡改位置（0-based）：").grid(row=7, column=0, padx=10, pady=5)
position_entry = tk.Entry(root, width=10)
position_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="新分组（16位）：").grid(row=8, column=0, padx=10, pady=5)
tamper_entry = tk.Entry(root, width=80)  # 将宽度调整为80
tamper_entry.grid(row=8, column=1, padx=10, pady=5)

tamper_button = tk.Button(root, text="篡改密文", command=tamper_cipher_text, bg='#4CAF50')
tamper_button.grid(row=9, column=0, columnspan=2, pady=10)

# 篡改后密文显示
tk.Label(root, text="篡改后密文：").grid(row=10, column=0, padx=10, pady=5)
tampered_cipher_text_entry = tk.Entry(root, width=80)
tampered_cipher_text_entry.grid(row=10, column=1, padx=10, pady=5)

# 篡改后解密结果显示
tk.Label(root, text="篡改后解密结果：").grid(row=11, column=0, padx=10, pady=5)
tampered_decrypted_text_entry = tk.Entry(root, width=80)
tampered_decrypted_text_entry.grid(row=11, column=1, padx=10, pady=5)

# 启动主循环
root.mainloop()