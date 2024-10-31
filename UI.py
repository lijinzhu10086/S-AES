import tkinter as tk
from extend import *
from main import *

# 创建主窗口
window = tk.Tk()
window.title('S-AES')
window.geometry('600x400')
window.configure(bg='#f0f0f0')  # 设置背景颜色

# 尺寸设计
header_label = tk.Label(window, text='S-AES 加解密', font=('Arial', 16, 'bold'), bg='#f0f0f0')
header_label.pack(pady=10)

# 选择模式部分
mode_frame = tk.Frame(window, bg='#f0f0f0')
mode_frame.pack(pady=10)

# 创建一个变量来存储选择的模式，默认为'二进制'
mode_var = tk.StringVar()
mode_var.set('二进制')

# 创建两个Radiobutton来选择模式
binary_mode_button = tk.Radiobutton(mode_frame, text='二进制', variable=mode_var, value='二进制', bg='#f0f0f0')
binary_mode_button.pack(side=tk.LEFT, padx=20)
text_mode_button = tk.Radiobutton(mode_frame, text='字符', variable=mode_var, value='字符', bg='#f0f0f0')
text_mode_button.pack(side=tk.LEFT)

# 输入部分
input_frame = tk.Frame(window, bg='#f0f0f0')
input_frame.pack(pady=10)

# 明文(密文)输入
input_label = tk.Label(input_frame, text='明文(or密文):', bg='#f0f0f0')
input_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')  # 右对齐
input_entry = tk.Entry(input_frame, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)

# 密钥输入
key_label = tk.Label(input_frame, text='密钥:', bg='#f0f0f0')
key_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')  # 右对齐
key_entry = tk.Entry(input_frame, width=50)
key_entry.grid(row=1, column=1, padx=5, pady=5)

# 输出部分
output_frame = tk.Frame(window, bg='#f0f0f0')
output_frame.pack(pady=10)

# 输出标签
output_label = tk.Label(output_frame, text='输出:', bg='#f0f0f0')
output_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
output_entry = tk.Entry(output_frame, width=50)
output_entry.grid(row=0, column=1, padx=5, pady=5)

# 加密解密逻辑
def encrypt():
    mode = mode_var.get()
    output_entry.delete(0, tk.END)
    if mode == '二进制':
        output_entry.insert(0, Encrypt(input_entry.get(), key_entry.get()))
    else:
        cipher_text = ascii_encrypt(input_entry.get(), key_entry.get())
        output_entry.insert(0, cipher_text)

def decrypt():
    mode = mode_var.get()
    output_entry.delete(0, tk.END)
    if mode == '二进制':
        output_entry.insert(0, Decrypt(input_entry.get(), key_entry.get()))
    else:
        decrypted_text = ascii_decrypt(input_entry.get(), key_entry.get())
        output_entry.insert(0, decrypted_text)

# 加密和解密按钮
button_frame = tk.Frame(window, bg='#f0f0f0')
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text='加密', command=encrypt, bg='#4CAF50', fg='white')
encrypt_button.pack(side=tk.LEFT, padx=10)

decrypt_button = tk.Button(button_frame, text='解密', command=decrypt, bg='#4CAF50', fg='white')
decrypt_button.pack(side=tk.LEFT, padx=10)

# 运行界面
window.mainloop()
