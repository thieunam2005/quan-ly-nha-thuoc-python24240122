import tkinter as tk
from tkinter import ttk, Toplevel
import json

def show_product_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    try:
        with open("data/san-pham.json", "r", encoding="utf-8") as f:
            products = json.load(f)
    except:
        products = []

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    filter_frame = tk.Frame(frame, bg="white")
    filter_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(filter_frame, text="Tìm kiếm:", bg="white").pack(side="left")
    keyword_var = tk.StringVar()
    keyword_entry = tk.Entry(filter_frame, textvariable=keyword_var)
    keyword_entry.pack(side="left", padx=5)

    tk.Label(filter_frame, text="Danh mục:", bg="white").pack(side="left", padx=10)
    category_var = tk.StringVar()
    category_menu = ttk.Combobox(filter_frame, textvariable=category_var, state="readonly")
    category_menu.pack(side="left")
    category_menu['values'] = [""] + sorted(set(p['danhMuc'] for p in products))

    canvas = tk.Canvas(frame)
    canvas.pack(fill="both", expand=True, side="left")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    product_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=product_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    product_frame.bind("<Configure>", on_configure)

    headers = ["Tên sản phẩm", "Giá", "Danh mục", "Chi tiết"]
    for i, h in enumerate(headers):
        tk.Label(product_frame, text=h, font=("Arial", 10, "bold"), bg="#ddd", relief="solid", width=25).grid(row=0, column=i)

    def render_table():
        for widget in product_frame.winfo_children()[len(headers):]:
            widget.destroy()

        for idx, p in enumerate(products):
            if keyword_var.get() and keyword_var.get().lower() not in p['tenSanPham'].lower():
                continue
            if category_var.get() and p['danhMuc'] != category_var.get():
                continue

            tk.Label(product_frame, text=p['tenSanPham'], anchor="w", relief="solid", width=25).grid(row=idx+1, column=0)
            tk.Label(product_frame, text=p['giaSanPham'], relief="solid", width=25).grid(row=idx+1, column=1)
            tk.Label(product_frame, text=p['danhMuc'], relief="solid", width=25).grid(row=idx+1, column=2)
            tk.Button(product_frame, text="Xem", command=lambda p=p: show_detail(p)).grid(row=idx+1, column=3)

    def show_detail(product):
        top = Toplevel()
        top.title("Chi tiết sản phẩm")
        top.geometry("400x500")

        text = tk.Text(top, wrap="word")
        text.pack(expand=True, fill="both")

        for key, value in product.items():
            if key != "URL":
                text.insert("end", f"{key}: {value}\n")

    keyword_var.trace_add("write", lambda *a: render_table())
    category_menu.bind("<<ComboboxSelected>>", lambda e: render_table())
    render_table()
