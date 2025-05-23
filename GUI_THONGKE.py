import tkinter as tk
from tkinter import messagebox
import json
import datetime
from CRAWL import CRAWL

def show_statistics_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()


    try:
        with open("data/san-pham.json", "r", encoding="utf-8") as f:
            products = json.load(f)
        with open("data/khach-hang.json", "r", encoding="utf-8") as f:
            customers = json.load(f)
    except:
        products, customers = [], []

    trending = CRAWL()

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

   
    tk.Label(frame, text="--- Sản phẩm bán chạy tham khảo từ Long Châu:", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(anchor="w", padx=10, pady=(10, 2))
    for p in trending[:10]:
        tk.Label(frame, text="- " + p['tenSanPham'], bg="white", anchor="w").pack(anchor="w", padx=20)


    tk.Label(frame, text="--- Sản phẩm sắp hết hạn:", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(anchor="w", padx=10, pady=(10, 2))
    today = datetime.datetime.today()
    exp_list = []
    for sp in products:
        try:
            exp = datetime.datetime.strptime(sp['hanSuDung'], "%d-%m-%Y")
            if (exp - today).days <= 90:
                exp_list.append(f"{sp['tenSanPham']} (HSD: {sp['hanSuDung']})")
        except:
            continue
    for item in exp_list:
        tk.Label(frame, text="- " + item, bg="white", anchor="w").pack(anchor="w", padx=20)
    if not exp_list:
        tk.Label(frame, text="Không có sản phẩm nào sắp hết hạn.", bg="white", fg="gray").pack(anchor="w", padx=20)


    tk.Label(frame, text="--- Sản phẩm sắp hết hàng:", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(anchor="w", padx=10, pady=(10, 2))
    low_stock = [sp['tenSanPham'] for sp in products if sp.get('soLuong', 0) < 10]
    for name in low_stock:
        tk.Label(frame, text="- " + name, bg="white", anchor="w").pack(anchor="w", padx=20)
    if not low_stock:
        tk.Label(frame, text="Không có sản phẩm nào gần hết hàng.", bg="white", fg="gray").pack(anchor="w", padx=20)


    tk.Label(frame, text="--- Khách hàng thân thiết:", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(anchor="w", padx=10, pady=(10, 2))
    if customers:
        top_cust = max(customers, key=lambda x: x.get('soLanMuaHang', 0))
        info = f"{top_cust['tenKhachHang']} - Số lần mua: {top_cust['soLanMuaHang']}"
        tk.Label(frame, text=info, bg="white", fg="blue", anchor="w").pack(anchor="w", padx=20)
    else:
        tk.Label(frame, text="Không có dữ liệu khách hàng.", bg="white", fg="gray").pack(anchor="w", padx=20)

    