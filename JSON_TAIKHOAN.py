# JSON_TAIKHOAN.py
import json

def JSON_R_TAIKHOAN():
    try:
        with open("data/tai-khoan.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []
