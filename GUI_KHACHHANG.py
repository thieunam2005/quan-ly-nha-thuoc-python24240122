import tkinter as tk
from tkinter import messagebox
import json

def show_customer_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    try:
        with open("data/khach-hang.json", "r", encoding="utf-8") as f:
            customers = json.load(f)
    except:
        customers = []

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Danh sách khách hàng", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=(10, 0))

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
        with open("data/khach-hang.json", "w", encoding="utf-8") as f:
            json.dump(customers, f, ensure_ascii=False, indent=2)
        show_customer_tab(parent)

    def delete_customer(ma):
        nonlocal customers
        customers = [c for c in customers if c["maKhachHang"] != ma]
        save_all()

    def open_edit_popup(cus):
        popup = tk.Toplevel()
        popup.title("Chỉnh sửa khách hàng")
        popup.geometry("300x250")

        ten_var = tk.StringVar(value=cus['tenKhachHang'])
        sdt_var = tk.StringVar(value=cus['soDienThoai'])
        slm_var = tk.StringVar(value=str(cus['soLanMuaHang']))

        tk.Label(popup, text="Tên khách hàng:").pack()
        tk.Entry(popup, textvariable=ten_var).pack()

        tk.Label(popup, text="Số điện thoại:").pack()
        tk.Entry(popup, textvariable=sdt_var).pack()

        tk.Label(popup, text="Số lần mua hàng:").pack()
        tk.Entry(popup, textvariable=slm_var).pack()

        def save_edit():
            cus['tenKhachHang'] = ten_var.get()
            cus['soDienThoai'] = sdt_var.get()
            try:
                cus['soLanMuaHang'] = int(slm_var.get())
            except:
                messagebox.showerror("Lỗi", "Số lần mua phải là số")
                return
            save_all()
            popup.destroy()

        tk.Button(popup, text="Lưu", bg="blue", fg="white", command=save_edit).pack(pady=10)

    def open_add_popup():
        popup = tk.Toplevel()
        popup.title("Thêm khách hàng")
        popup.geometry("300x250")

        ten_var = tk.StringVar()
        sdt_var = tk.StringVar()

        tk.Label(popup, text="Tên khách hàng:").pack()
        tk.Entry(popup, textvariable=ten_var).pack()

        tk.Label(popup, text="Số điện thoại:").pack()
        tk.Entry(popup, textvariable=sdt_var).pack()

        def save_add():
            if not ten_var.get().strip() or not sdt_var.get().strip():
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ")
                return
            new = {
                "maKhachHang": str(max([int(c['maKhachHang']) for c in customers] + [0]) + 1).zfill(5),
                "tenKhachHang": ten_var.get().strip(),
                "soDienThoai": sdt_var.get().strip(),
                "soLanMuaHang": 0
            }
            customers.append(new)
            save_all()
            popup.destroy()

        tk.Button(popup, text="Thêm", bg="green", fg="white", command=save_add).pack(pady=10)

    for cus in customers:
        row = tk.Frame(scrollable, bg="#f9f9f9", bd=1, relief="solid", pady=5)
        row.pack(fill="x", pady=5)

        info = f"Tên: {cus['tenKhachHang']}\nMã: {cus['maKhachHang']}\nSĐT: {cus['soDienThoai']}\nSL mua: {cus['soLanMuaHang']}"
        tk.Label(row, text=info, bg="#f9f9f9", justify="left", font=("Arial", 10)).pack(side="left", padx=10)

        tk.Button(row, text="Sửa", bg="blue", fg="white", command=lambda c=cus: open_edit_popup(c)).pack(side="right", padx=5)
        tk.Button(row, text="Xóa", bg="red", fg="white", command=lambda m=cus['maKhachHang']: delete_customer(m)).pack(side="right", padx=5)

    tk.Button(frame, text="Thêm khách hàng", bg="green", fg="white", font=("Arial", 10), command=open_add_popup).pack(pady=10)

