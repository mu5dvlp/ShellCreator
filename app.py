import tkinter as tk
import subprocess
import os
import re
import platform

import config
import dataManager

# //＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
def is_valid_filename(filename):
    if platform.system() == "Windows":
        invalid_chars = r'<>:"/\\|?*'
    else:
        invalid_chars = r'/'
    
    if re.search(f'[{re.escape(invalid_chars)}]', filename):
        return False
    
    if platform.system() == "Windows":
        reserved_names = [
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
        ]
        if filename.upper().split('.')[0] in reserved_names:
            return False

    max_length = 255
    return 0<len(filename)<=255

# //〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
def create_shell_command_file():
    fileName = entry_fileName.get()
    if not is_valid_filename(fileName):
        print("ファイル名が無効です")
        return
    
    # コマンド用のディレクトリがなければ作成
    if not os.path.exists(config.COMMAND_FILE_ROOT_PATH):
        os.makedirs(config.COMMAND_FILE_ROOT_PATH)

    # 実行ファイルの既存確認
    filePath = f'{config.COMMAND_FILE_ROOT_PATH}/{fileName}'
    if os.path.exists(filePath):
        print(f"{filePath} は既に存在します。")
        return

    with open(filePath,'w') as f:
        code = "#!/bin/sh\n"
        code+=text_code.get("1.0", tk.END)
        f.write(code)
    
    subprocess.run(["chmod","755",filePath], capture_output=True, text=True)
    print(is_enable_open_editor)
    if is_enable_open_editor.get():
        subprocess.run(["open","-a",config.COMMAND_FILE_EDITOR,filePath])

# //〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
def open_command_directory_with_finder():
    subprocess.run(["open",config.COMMAND_FILE_ROOT_PATH])

# //ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
root = tk.Tk()
root.title("Shell Creator")
root.geometry("500x500")

# //〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
# ファイル名
frame_fileName = tk.Frame(root)
frame_fileName.pack(pady=10)
label_fileName = tk.Label(frame_fileName,text="ファイル名：")
label_fileName.pack(side=tk.LEFT)
entry_fileName = tk.Entry(frame_fileName)
entry_fileName.pack(side=tk.LEFT)
# label_fileNameExtension = tk.Label(frame_fileName,text=".sh")
# label_fileNameExtension.pack(side=tk.LEFT)

# コード
frame_code = tk.Frame(root)
frame_code.pack(pady=10)
label_code = tk.Label(frame_code,text="コード")
label_code.pack()
text_code = tk.Text(frame_code)
text_code.pack(padx=10)
is_enable_open_editor = tk.IntVar()
checkbutton_create = tk.Checkbutton(frame_code, text="VSCodeを開く", variable=is_enable_open_editor)
checkbutton_create.pack()
button_create = tk.Button(frame_code, text="作成",command=create_shell_command_file)
button_create.pack()

button_create = tk.Button(root, text="Reveal in Finder",command=open_command_directory_with_finder)
button_create.pack()

# //〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜
root.mainloop()