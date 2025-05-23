import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime

def show_invoice_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    try:
        with open("data/hoa-don.json", "r", encoding="utf-8") as f:
            invoices = json.load(f)
    except:
        invoices = []

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)


    filter_frame = tk.Frame(frame, bg="white")
    filter_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(filter_frame, text="Tổng tiền >=", bg="white").pack(side="left")
    tong_tien_var = tk.StringVar()
    tk.Entry(filter_frame, textvariable=tong_tien_var, width=10).pack(side="left", padx=5)

    tk.Label(filter_frame, text="Số SP >=", bg="white").pack(side="left")
    so_sp_var = tk.StringVar()
    tk.Entry(filter_frame, textvariable=so_sp_var, width=5).pack(side="left", padx=5)

    tk.Label(filter_frame, text="Từ ngày (YYYY-MM-DD):", bg="white").pack(side="left")
    from_date_var = tk.StringVar()
    tk.Entry(filter_frame, textvariable=from_date_var, width=12).pack(side="left", padx=5)

    tk.Label(filter_frame, text="Đến ngày:", bg="white").pack(side="left")
    to_date_var = tk.StringVar()
    tk.Entry(filter_frame, textvariable=to_date_var, width=12).pack(side="left", padx=5)


    canvas = tk.Canvas(frame)
    canvas.pack(fill="both", expand=True, side="left")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    list_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=list_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    list_frame.bind("<Configure>", on_configure)

    def delete_invoice(ma):
        nonlocal invoices
        invoices = [hd for hd in invoices if hd["maHoaDon"] != ma]
        with open("data/hoa-don.json", "w", encoding="utf-8") as f:
            json.dump(invoices, f, ensure_ascii=False, indent=2)
        render_table()

    def render_table():
        for widget in list_frame.winfo_children():
            widget.destroy()

        for idx, hd in enumerate(invoices):
            if tong_tien_var.get():
                try:
                    if hd['tongTien'] < int(tong_tien_var.get()):
                        continue
                except: pass
            if so_sp_var.get():
                try:
                    if len(hd['danhSachSanPham']) < int(so_sp_var.get()):
                        continue
                except: pass
            if from_date_var.get():
                try:
                    if hd['ngayBan'] < from_date_var.get():
                        continue
                except: pass
            if to_date_var.get():
                try:
                    if hd['ngayBan'] > to_date_var.get():
                        continue
                except: pass

            row = tk.Frame(list_frame, bg="white", relief="solid", bd=1)
            row.pack(fill="x", padx=5, pady=3)

            info = f"Mã: {hd['maHoaDon']} | KH: {hd['maKhachHang']} | Ngày: {hd['ngayBan']} | SP: {len(hd['danhSachSanPham'])} | Tổng: {hd['tongTien']}đ"
            tk.Label(row, text=info, anchor="w", bg="white").pack(side="left", padx=10)

            tk.Button(row, text="Xóa", bg="red", fg="white", command=lambda ma=hd['maHoaDon']: delete_invoice(ma)).pack(side="right", padx=10)

    for var in [tong_tien_var, so_sp_var, from_date_var, to_date_var]:
        var.trace_add("write", lambda *a: render_table())

    render_table()
