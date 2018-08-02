#!/usr/bin/env python3
# 同步香港中文與台灣中文的翻譯 for Android Strings.
# 若有香港朋友想要協助「香港化」，可逕行移除此程式。
import os, shutil, json, sys

# 定義變數
zh_TW = "values-zh-rTW"
zh_HK = "values-zh-rHK"
glossary_file = "hk_glossary.json"
# 最大讀取大小，預設 3145728 bytes (3MB)
filesize = 3145728

def Exists(filename, type):
    '''
    filename:   檔案名稱
    type:       檔案類型 (file, dir)
    若 filename 存在，並符合 type 類型則回傳 True，
    其餘回傳 False。
    '''
    if type == "file":
        if os.path.exists(filename) and os.path.isfile(filename):
            return True
        else:
            return False
    elif type == "dir":
        if os.path.exists(filename) and os.path.isdir(filename):
            return True
        else:
            return False
    else:
        return False

# 讀取台灣與香港中文轉換字彙表
if Exists(glossary_file, "file"):
    print("[INFO] 已找到香港台灣中文字彙表 json。")
else:
    raise Exception("[ERR] 未找到所需的字彙表，程式被迫中止。")

# 檢查正體與香港中文的語言目錄
if Exists(zh_TW, "dir"):
    print("[INFO] 已找到台灣中文翻譯。")
    TWFileRaw = os.open(zh_TW + "/strings.xml", os.O_RDONLY)
else:
    raise Exception("[ERR] 未找到所需的台灣中文翻譯，程式被迫中止。")

if Exists(zh_HK, "dir"):
    input("[INFO] 已找到原始香港中文翻譯，按下 enter 移除，按下 ctrl-c 中止作業。")
    shutil.rmtree(zh_HK)
elif Exists(zh_HK, "file"):
    input("[INFO] 程式期望 {0} 是資料夾，但只找到了 {0} 檔案，按下 enter 移除，按下 ctrl-c 中止作業。".format(zh_HK))
    os.remove(zh_HK)

# 開始解析 json 檔案
try:
    glossary_file_raw = os.open(glossary_file, os.O_RDONLY)
    glossary_file = os.read(glossary_file_raw, filesize).decode("UTF-8")
    glossary_json = json.loads(glossary_file)
    os.close(glossary_file_raw)
except:
    print("[ERR] 讀取字彙表檔案時發生錯誤，請開 Issue 以聯絡開發者。")
    print("並提供這些資訊：" + sys.exc_info())

# 開始讀取 TW 語系資料
TWFile = os.read(TWFileRaw, filesize).decode("UTF-8")
os.close(TWFileRaw)
for loop in glossary_json:
    TWFile = TWFile.replace(loop, glossary_json[loop])

# 寫入到 values-zh-rHK 檔案中
os.mkdir(zh_HK)
HKFileRaw = os.open(zh_HK + "/strings.xml", os.O_WRONLY|os.O_CREAT)
os.write(HKFileRaw, TWFile.encode("UTF-8"))
print("[INFO] 成功轉換台灣語系檔案到香港語系檔案！")
os.close(HKFileRaw)

# 離開程式，回傳 0
exit(0)