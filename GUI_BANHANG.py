import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import datetime
import random

def show_sale_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    try:
        with open("data/san-pham.json", "r", encoding="utf-8") as f:
            products = json.load(f)
        with open("data/khach-hang.json", "r", encoding="utf-8") as f:
            khach_hang = json.load(f)
    except:
        messagebox.showerror("Lỗi", "Không thể đọc dữ liệu!")
        return

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)


    control_frame = tk.Frame(frame, bg="white")
    control_frame.pack(fill="x", padx=10, pady=5)

    tk.Button(control_frame, text="Bán", bg="green", fg="white", font=("Arial", 10), command=lambda: process_sale()).pack(side="right", padx=5)

    tk.Label(control_frame, text="Tìm kiếm:", bg="white").pack(side="left")
    keyword_var = tk.StringVar()
    keyword_entry = tk.Entry(control_frame, textvariable=keyword_var)
    keyword_entry.pack(side="left", padx=5)

    tk.Label(control_frame, text="Danh mục:", bg="white").pack(side="left", padx=10)
    category_var = tk.StringVar()
    category_menu = ttk.Combobox(control_frame, textvariable=category_var, state="readonly")
    category_menu.pack(side="left")
    category_menu['values'] = [""] + sorted(set(p['danhMuc'] for p in products))


    tk.Label(frame, text="Khách hàng:", bg="white").pack(anchor="w", padx=10, pady=(5, 0))
    khach_var = tk.StringVar()
    khach_menu = ttk.Combobox(frame, textvariable=khach_var, state="readonly")
    khach_menu['values'] = [f"{k['maKhachHang']} - {k['tenKhachHang']}" for k in khach_hang]
    khach_menu.pack(fill="x", padx=10)

 
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

    headers = ["Tên sản phẩm", "Giá", "Tồn kho", "SL mua"]
    for i, h in enumerate(headers):
        tk.Label(product_frame, text=h, font=("Arial", 10, "bold"), bg="#ddd", relief="solid", width=20).grid(row=0, column=i)

    entry_map = {}
    qty_labels = {}

    def render_table():
        for widget in product_frame.winfo_children():
            if int(widget.grid_info().get('row', 1)) > 0:
                widget.destroy()

        for idx, p in enumerate(products):
            if keyword_var.get() and keyword_var.get().lower() not in p['tenSanPham'].lower():
                continue
            if category_var.get() and p['danhMuc'] != category_var.get():
                continue

            tk.Label(product_frame, text=p['tenSanPham'], anchor="w", relief="solid", width=20).grid(row=idx+1, column=0)
            tk.Label(product_frame, text=p['giaSanPham'], relief="solid", width=20).grid(row=idx+1, column=1)
            qty_lbl = tk.Label(product_frame, text=p['soLuong'], relief="solid", width=20)
            qty_lbl.grid(row=idx+1, column=2)
            qty_labels[p['maSanPham']] = qty_lbl

            e = tk.Entry(product_frame, width=5)
            e.insert(0, "0")
            e.grid(row=idx+1, column=3)
            entry_map[p['maSanPham']] = (p, e)

    keyword_var.trace_add("write", lambda *a: render_table())
    category_menu.bind("<<ComboboxSelected>>", lambda e: render_table())

    def process_sale():
        ma_khach = khach_var.get().split(" - ")[0] if khach_var.get() else "KH000"
        try:
            with open("data/san-pham.json", "r", encoding="utf-8") as f:
                all_products = json.load(f)
        except:
            messagebox.showerror("Lỗi", "Không đọc được dữ liệu sản phẩm.")
            return

        hoa_don = {
            "maHoaDon": str(random.randint(1000000000, 9999999999)),
            "maKhachHang": ma_khach,
            "ngayBan": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "danhSachSanPham": [],
            "tongTien": 0
        }

        for msp, (prod, entry) in entry_map.items():
            try:
                sl = int(entry.get())
            except:
                sl = 0
            if sl > 0:
                sp = next((x for x in all_products if x['maSanPham'] == msp), None)
                if sp and sp['soLuong'] >= sl:
                    sp['soLuong'] -= sl
                    tt = sl * prod['giaSanPham']
                    hoa_don['danhSachSanPham'].append({
                        "tenSanPham": prod['tenSanPham'],
                        "soLuong": sl,
                        "giaTien": prod['giaSanPham'],
                        "thanhTien": tt
                    })
                    hoa_don['tongTien'] += tt
                    qty_labels[msp].config(text=sp['soLuong'])  
                else:
                    messagebox.showwarning("Không đủ hàng", f"{prod['tenSanPham']} không đủ hàng.")
                    return

        try:
            with open("data/hoa-don.json", "r", encoding="utf-8") as f:
                ds = json.load(f)
        except:
            ds = []
        ds.append(hoa_don)
        with open("data/hoa-don.json", "w", encoding="utf-8") as f:
            json.dump(ds, f, ensure_ascii=False, indent=2)

        with open("data/san-pham.json", "w", encoding="utf-8") as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)

        for kh in khach_hang:
            if kh['maKhachHang'] == ma_khach:
                kh['soLanMuaHang'] = kh.get('soLanMuaHang', 0) + 1
                break

        with open("data/khach-hang.json", "w", encoding="utf-8") as f:
            json.dump(khach_hang, f, ensure_ascii=False, indent=2)


        messagebox.showinfo("Thành công", "Đã bán hàng và cập nhật hóa đơn.")

    render_table()

def show_detail(product):
    top = tk.Toplevel()
    top.title("Chi tiết sản phẩm")
    top.geometry("400x500")

    text = tk.Text(top, wrap="word")
    text.pack(expand=True, fill="both")

    for key, value in product.items():
        if key != "URL":
            text.insert("end", f"{key}: {value}\n")
