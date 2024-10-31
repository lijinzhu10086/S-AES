import tkinter as tk
from main import *

# 双重加密
def double_encrypt(plain_text, key1, key2):
    cipher_text1 = Encrypt(plain_text, key1)
    cipher_text2 = Encrypt(cipher_text1, key2)
    return cipher_text2

# 双重解密
def double_decrypt(cipher_text, key1, key2):
    plain_text1 = Decrypt(cipher_text, key2)
    plain_text2 = Decrypt(plain_text1, key1)
    return plain_text2

# 生成所有可能的密钥对
def generate_all_keys():
    for i in range(2 ** 32):
        key = bin(i)[2:].zfill(32)
        yield (key[:16], key[16:])

# 中间相遇攻击
def middle_meet_attack(known_plain_text_list, known_cipher_text_list):
    all_keys = generate_all_keys()
    for key1, key2 in all_keys:
        flag = True
        for known_plain_text, known_cipher_text in zip(known_plain_text_list, known_cipher_text_list):
            middle_text1 = Encrypt(known_plain_text, key1)
            middle_text2 = Encrypt(known_cipher_text, key2)
            if middle_text1 != middle_text2:
                flag = False
                break
        if flag:
            return [(key1, key2)]
    return []

# 三重加密
def triple_encrypt(plain_text, key1, key2):
    cipher_text1 = Encrypt(plain_text, key1)
    cipher_text2 = Decrypt(cipher_text1, key2)
    cipher_text3 = Encrypt(cipher_text2, key1)
    return cipher_text3

# 三重解密
def triple_decrypt(cipher_text, key1, key2):
    plain_text1 = Decrypt(cipher_text, key1)
    plain_text2 = Encrypt(plain_text1, key2)
    plain_text3 = Decrypt(plain_text2, key1)
    return plain_text3

# 创建主窗口
def main_menu():
    global main_window
    main_window = tk.Tk()
    main_window.title("加密解密工具")
    main_window.geometry("300x250")  # 设置窗口大小
    tk.Label(main_window, text="请选择功能:").pack(pady=10)

    tk.Button(main_window, text="   双重加密   ", command=double_encrypt_menu).pack(pady=5)
    tk.Button(main_window, text="中间相遇攻击", command=middle_meet_attack_menu).pack(pady=5)
    tk.Button(main_window, text="   三重加密   ", command=triple_encrypt_menu).pack(pady=5)

    main_window.mainloop()

def double_encrypt_menu():
    def perform_double_encrypt():
        plain_text = plain_text_entry.get()
        key1 = key1_entry.get()
        key2 = key2_entry.get()
        result = double_encrypt(plain_text, key1, key2)
        result_text.delete(1.0, tk.END)  # 清空之前的结果
        result_text.insert(tk.END, result)  # 显示新的结果

    menu_window = tk.Toplevel(main_window)
    menu_window.title("双重加密")
    menu_window.geometry("400x400")  # 增加窗口高度以容纳新的组件
    menu_window.configure(bg="#f0f0f0")

    tk.Label(menu_window, text="明文:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    plain_text_entry = tk.Entry(menu_window, width=40, font=("Helvetica", 12))
    plain_text_entry.pack(pady=5)

    tk.Label(menu_window, text="密钥1:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    key1_entry = tk.Entry(menu_window, width=20, font=("Helvetica", 12))
    key1_entry.pack(pady=5)

    tk.Label(menu_window, text="密钥2:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    key2_entry = tk.Entry(menu_window, width=20, font=("Helvetica", 12))
    key2_entry.pack(pady=5)

    tk.Button(menu_window, text="执行加密", command=perform_double_encrypt,
              bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=15)

    # 增加一个用于显示加密结果的文本框
    tk.Label(menu_window, text="加密结果:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    result_text = tk.Text(menu_window, height=1.5, width=40, font=("Helvetica", 12), wrap=tk.WORD)
    result_text.pack(pady=5)

def middle_meet_attack_menu():
    def perform_middle_attack():
        known_plain_texts = known_plain_entry.get().split(',')
        known_cipher_texts = known_cipher_entry.get().split(',')
        keys = middle_meet_attack(known_plain_texts, known_cipher_texts)
        if keys:
            result_text.delete(1.0, tk.END)  # 清空之前的结果
            result_text.insert(tk.END, f" {keys}")  # 显示新的结果
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "未找到密钥对")  # 显示没有找到密钥的消息

    menu_window = tk.Toplevel(main_window)
    menu_window.title("中间相遇攻击")
    menu_window.geometry("400x400")  # 增加窗口高度以容纳新的组件
    menu_window.configure(bg="#f0f0f0")

    tk.Label(menu_window, text="已知明文（以逗号分隔）:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    known_plain_entry = tk.Entry(menu_window, width=40, font=("Helvetica", 12))
    known_plain_entry.pack(pady=5)

    tk.Label(menu_window, text="已知密文（以逗号分隔）:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    known_cipher_entry = tk.Entry(menu_window, width=40, font=("Helvetica", 12))
    known_cipher_entry.pack(pady=5)

    tk.Button(menu_window, text="执行攻击", command=perform_middle_attack,
              bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=15)

    # 增加一个用于显示密钥对的文本框
    tk.Label(menu_window, text="攻击结果:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    result_text = tk.Text(menu_window, height=2, width=40, font=("Helvetica", 12), wrap=tk.WORD)
    result_text.pack(pady=5)
# 三重加密界面
def triple_encrypt_menu():
    def perform_triple_encrypt():
        plain_text = plain_text_entry.get()
        key1 = key1_entry.get()
        key2 = key2_entry.get()
        result = triple_encrypt(plain_text, key1, key2)
        result_text.delete(1.0, tk.END)  # 清空之前的结果
        result_text.insert(tk.END, f"加密结果: {result}")  # 显示新的结果

    menu_window = tk.Toplevel(main_window)
    menu_window.title("三重加密")
    menu_window.geometry("400x400")  # 设置窗口大小
    menu_window.configure(bg="#f0f0f0")  # 设置背景色

    tk.Label(menu_window, text="明文:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    plain_text_entry = tk.Entry(menu_window, width=40, font=("Helvetica", 12))
    plain_text_entry.pack(pady=5)

    tk.Label(menu_window, text="密钥1:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    key1_entry = tk.Entry(menu_window, width=20, font=("Helvetica", 12))
    key1_entry.pack(pady=5)

    tk.Label(menu_window, text="密钥2:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    key2_entry = tk.Entry(menu_window, width=20, font=("Helvetica", 12))
    key2_entry.pack(pady=5)

    tk.Button(menu_window, text="执行加密", command=perform_triple_encrypt,
              bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=15)

    # 增加一个用于显示加密结果的文本框
    tk.Label(menu_window, text="加密结果:", bg="#f0f0f0", font=("Helvetica", 12)).pack(pady=10)
    result_text = tk.Text(menu_window, height=2, width=40, font=("Helvetica", 12), wrap=tk.WORD)
    result_text.pack(pady=5)
# 启动主菜单
main_menu()
