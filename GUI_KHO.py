import tkinter as tk
from tkinter import messagebox, ttk
import json

def show_warehouse_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    try:
        with open("data/san-pham.json", "r", encoding="utf-8") as f:
            products = json.load(f)
    except:
        products = []

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Quản lý kho hàng", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=(10, 5))

    filter_frame = tk.Frame(frame, bg="white")
    filter_frame.pack(fill="x", padx=10)

    tk.Label(filter_frame, text="Tìm kiếm:", bg="white").pack(side="left")
    keyword_var = tk.StringVar()
    tk.Entry(filter_frame, textvariable=keyword_var).pack(side="left", padx=5)

    tk.Label(filter_frame, text="Danh mục:", bg="white").pack(side="left", padx=10)
    category_var = tk.StringVar()
    category_menu = ttk.Combobox(filter_frame, textvariable=category_var, state="readonly")
    category_menu.pack(side="left")

    category_menu['values'] = [""] + sorted(set(p['danhMuc'] for p in products))

    list_frame = tk.Frame(frame, bg="white")
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(list_frame, bg="white")
    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas, bg="white")

    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def save_all():
        with open("data/san-pham.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        show_warehouse_tab(parent)

    def delete_product(ma):
        nonlocal products
        products = [p for p in products if p['maSanPham'] != ma]
        save_all()

    def open_edit_popup(prod):
        popup = tk.Toplevel()
        popup.title("Sửa sản phẩm")
        popup.geometry("400x400")

        fields = {
            "tenSanPham": "Tên sản phẩm",
            "giaSanPham": "Giá bán",
            "danhMuc": "Danh mục",
            "soLuong": "Số lượng"
        }
        entries = {}
        for key, label in fields.items():
            tk.Label(popup, text=label).pack()
            var = tk.StringVar(value=str(prod[key]))
            entry = tk.Entry(popup, textvariable=var)
            entry.pack()
            entries[key] = var

        def save():
            try:
                prod['tenSanPham'] = entries['tenSanPham'].get()
                prod['giaSanPham'] = int(entries['giaSanPham'].get())
                prod['danhMuc'] = entries['danhMuc'].get()
                prod['soLuong'] = int(entries['soLuong'].get())
                save_all()
                popup.destroy()
            except:
                messagebox.showerror("Lỗi", "Giá và số lượng phải là số")

        tk.Button(popup, text="Lưu", bg="blue", fg="white", command=save).pack(pady=10)

    def open_add_popup():
        popup = tk.Toplevel()
        popup.title("Thêm sản phẩm")
        popup.geometry("400x400")

        ma_var = tk.StringVar()
        ten_var = tk.StringVar()
        gia_var = tk.StringVar()
        loai_var = tk.StringVar()
        sl_var = tk.StringVar()

        tk.Label(popup, text="Mã sản phẩm (8 chữ số):").pack()
        tk.Entry(popup, textvariable=ma_var).pack()
        tk.Label(popup, text="Tên sản phẩm:").pack()
        tk.Entry(popup, textvariable=ten_var).pack()
        tk.Label(popup, text="Giá bán:").pack()
        tk.Entry(popup, textvariable=gia_var).pack()
        tk.Label(popup, text="Danh mục:").pack()
        tk.Entry(popup, textvariable=loai_var).pack()
        tk.Label(popup, text="Số lượng:").pack()
        tk.Entry(popup, textvariable=sl_var).pack()

        def save():
            ma = ma_var.get()
            if not (ma.isdigit() and len(ma) == 8):
                messagebox.showerror("Lỗi", "Mã sản phẩm phải là 8 chữ số")
                return
            if any(p['maSanPham'] == ma for p in products):
                messagebox.showerror("Lỗi", "Mã sản phẩm đã tồn tại")
                return
            try:
                new = {
                    "maSanPham": ma,
                    "tenSanPham": ten_var.get(),
                    "giaSanPham": int(gia_var.get()),
                    "danhMuc": loai_var.get(),
                    "soLuong": int(sl_var.get())
                }
                products.append(new)
                save_all()
                popup.destroy()
            except:
                messagebox.showerror("Lỗi", "Giá và số lượng phải là số")

        tk.Button(popup, text="Thêm", bg="green", fg="white", command=save).pack(pady=10)

    def render():
        for widget in scrollable.winfo_children():
            widget.destroy()
        for prod in products:
            if keyword_var.get() and keyword_var.get().lower() not in prod['tenSanPham'].lower():
                continue
            if category_var.get() and prod['danhMuc'] != category_var.get():
                continue

            row = tk.Frame(scrollable, bg="#f9f9f9", bd=1, relief="solid", pady=5)
            row.pack(fill="x", pady=5)

            info = f"{prod['tenSanPham']}\nMã: {prod['maSanPham']} | Giá: {prod['giaSanPham']} | SL: {prod['soLuong']}"
            tk.Label(row, text=info, bg="#f9f9f9", justify="left", font=("Arial", 10)).pack(side="left", padx=10)
            tk.Button(row, text="Sửa", bg="blue", fg="white", command=lambda p=prod: open_edit_popup(p)).pack(side="right", padx=5)
            tk.Button(row, text="Xóa", bg="red", fg="white", command=lambda m=prod['maSanPham']: delete_product(m)).pack(side="right")

    keyword_var.trace_add("write", lambda *a: render())
    category_menu.bind("<<ComboboxSelected>>", lambda e: render())

    render()
    tk.Button(frame, text="Thêm sản phẩm", bg="green", fg="white", font=("Arial", 10), command=open_add_popup).pack(pady=10)

