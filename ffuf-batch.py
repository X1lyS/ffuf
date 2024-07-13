import subprocess
import os
import sys

def print_art():
    art = """
░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░   
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░        
"""
    print(art)

def list_dict_files():
    dict_dir = "./dict"
    dict_files = [f for f in os.listdir(dict_dir) if f.endswith('.txt')]
    if not dict_files:
        print("没有找到字典文件，请在./dict目录下添加字典。")
        exit(1)
    print("可用字典文件:")
    for idx, file in enumerate(dict_files):
        print(f"{idx + 1}: {file}")
    return dict_files

def get_ffuf_parameters():
    params = input("请输入ffuf参数（例如：-af -t -p -recursion -recursion-depth -mc all -o -c -v -sf -fs -fc ……）：")
    return params.strip()

def single_target_scan(url, dict_file, params):
    command = f"ffuf -u {url}/FUZZ -w ./dict/{dict_file} {params}"
    print(f"\n执行命令：{command}\n")

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    with open("single_target_result.txt", "w") as result_file:
        for line in process.stdout:
            line = line.strip()
            if "Progress:" in line:
                sys.stdout.write("\r" + " " * 80 + "\r")
                sys.stdout.write(line)
                sys.stdout.flush()
            elif line and "Status:" in line:
                sys.stdout.write("\r" + " " * 80 + "\r")
                print(line)
                result_file.write(line + "\n")

def multiple_target_scan(dict_file, params):
    if not os.path.exists("urls.txt"):
        print("urls.txt 文件不存在，请创建并添加目标URL。")
        return
    with open("urls.txt", "r") as f:
        urls = f.readlines()
    for url in urls:
        url = url.strip()
        if url:
            command = f"ffuf -u {url}/FUZZ -w ./dict/{dict_file} {params}"
            print(f"\n执行命令：{command}\n")

            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            with open("multiple_target_result.txt", "a") as result_file:
                result_file.write(f"目标URL: {url}\n")
                for line in process.stdout:
                    line = line.strip()
                    if "Progress:" in line:
                        sys.stdout.write("\r" + " " * 80 + "\r")
                        sys.stdout.write(line)
                        sys.stdout.flush()
                    elif line and "Status:" in line:
                        sys.stdout.write("\r" + " " * 80 + "\r")
                        print(line)
                        result_file.write(line + "\n")

def main():
    print_art()
    print("选择扫描模式：")
    print("1. 单个目标扫描")
    print("2. 多个目标扫描")
    choice = input("请输入您的选择（1 或 2）：")

    dict_files = list_dict_files()
    dict_choice = input("请选择字典文件（输入对应的数字）：")
    dict_file = dict_files[int(dict_choice) - 1]

    params = get_ffuf_parameters()

    if choice == '1':
        url = input("请输入目标URL：")
        single_target_scan(url, dict_file, params)
    elif choice == '2':
        multiple_target_scan(dict_file, params)
    else:
        print("无效选择，请输入1或2。")

if __name__ == "__main__":
    main()
