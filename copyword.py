import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


def copy_doc_files(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    copied_files = []
    skipped_files = []
    error_files = []

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.doc', '.docx')):
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_dir, file)

                if os.path.exists(target_file_path):
                    skipped_files.append(file)
                else:
                    try:
                        shutil.copy2(source_file_path, target_file_path)
                        copied_files.append(file)
                    except Exception as e:
                        error_files.append((file, str(e)))

    result_msg = ""
    if copied_files:
        result_msg += f"成功复制 {len(copied_files)} 个文件。\n"
    if skipped_files:
        result_msg += f"跳过 {len(skipped_files)} 个已存在的文件。\n"
    if error_files:
        result_msg += f"复制 {len(error_files)} 个文件时出错：\n"
        for file, error in error_files:
            result_msg += f"  - {file}: {error}\n"

    if not result_msg:
        result_msg = "未找到需要复制的文件。"

    messagebox.showinfo("复制结果", result_msg)


def select_source_directory():
    source_dir = filedialog.askdirectory()
    if source_dir:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, source_dir)


def select_target_directory():
    target_dir = filedialog.askdirectory()
    if target_dir:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, target_dir)


def start_copying():
    source_dir = source_entry.get()
    target_dir = target_entry.get()
    if not source_dir or not target_dir:
        messagebox.showerror("错误", "请选择源目录和目标目录。")
        return
    copy_doc_files(source_dir, target_dir)


# 创建主窗口
root = tk.Tk()
root.title("文档文件复制工具")

# 创建源目录选择部分
source_label = tk.Label(root, text="源目录:")
source_label.pack(pady=5)
source_entry = tk.Entry(root, width=50)
source_entry.pack(pady=5)
source_button = tk.Button(root, text="选择源目录", command=select_source_directory)
source_button.pack(pady=5)

# 创建目标目录选择部分
target_label = tk.Label(root, text="目标目录:")
target_label.pack(pady=5)
target_entry = tk.Entry(root, width=50)
target_entry.pack(pady=5)
target_button = tk.Button(root, text="选择目标目录", command=select_target_directory)
target_button.pack(pady=5)

# 创建开始复制按钮
start_button = tk.Button(root, text="开始复制", command=start_copying)
start_button.pack(pady=20)

# 运行主循环
root.mainloop()
