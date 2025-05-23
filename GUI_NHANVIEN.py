import tkinter as tk
from tkinter import messagebox
import json
import os
from PIL import Image, ImageTk

def show_employee_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    try:
        with open("data/nhan-vien.json", "r", encoding="utf-8") as f:
            employees = json.load(f)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không đọc được dữ liệu: {e}")
        employees = []

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Danh sách nhân viên", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=(10, 0))

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

    def delete_employee(ma):
        nonlocal employees
        employees = [nv for nv in employees if nv["maNhanVien"] != ma]
        with open("data/nhan-vien.json", "w", encoding="utf-8") as f:
            json.dump(employees, f, ensure_ascii=False, indent=2)

        try:
            with open("data/tai-khoan.json", "r", encoding="utf-8") as f:
                accounts = json.load(f)
        except:
            accounts = []
        accounts = [acc for acc in accounts if acc["taiKhoan"] != ma]
        with open("data/tai-khoan.json", "w", encoding="utf-8") as f:
            json.dump(accounts, f, ensure_ascii=False, indent=2)

        show_employee_tab(parent)

    if not employees:
        tk.Label(scrollable, text="Không có nhân viên nào.", font=("Arial", 11), bg="white", fg="gray").pack(pady=20)
    else:
        for idx, nv in enumerate(employees):
            row = tk.Frame(scrollable, bg="#f9f9f9", bd=1, relief="solid", pady=5)
            row.pack(fill="x", pady=5)

            img_path = f"profile-img/employee.png"
            try:
                img = Image.open(img_path).resize((60, 60))
            except:
                img = Image.new("RGB", (60, 60), color="gray")
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(row, image=img_tk, bg="#f9f9f9")
            img_label.image = img_tk
            img_label.pack(side="left", padx=10)

            info = f"Tên: {nv['tenNhanVien']}\nMã: {nv['maNhanVien']}\nSĐT: {nv['SDT']}\nVai trò: {nv['vaiTro']}"
            tk.Label(row, text=info, bg="#f9f9f9", justify="left", font=("Arial", 10)).pack(side="left", padx=10)

            tk.Button(row, text="Xóa", bg="red", fg="white", command=lambda m=nv['maNhanVien']: delete_employee(m)).pack(side="right", padx=10)

    def open_add_popup():
        popup = tk.Toplevel()
        popup.title("Thêm nhân viên")
        popup.geometry("300x250")

        tk.Label(popup, text="Mã nhân viên:").pack()
        ma_var = tk.StringVar()
        tk.Entry(popup, textvariable=ma_var).pack()

        tk.Label(popup, text="Tên nhân viên:").pack()
        ten_var = tk.StringVar()
        tk.Entry(popup, textvariable=ten_var).pack()

        tk.Label(popup, text="SĐT:").pack()
        sdt_var = tk.StringVar()
        tk.Entry(popup, textvariable=sdt_var).pack()

        def save_new():
            ma = ma_var.get().strip()
            ten = ten_var.get().strip()
            sdt = sdt_var.get().strip()

            if not ma or not ten or not sdt:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
                return

            new_nv = {
                "maNhanVien": ma,
                "tenNhanVien": ten,
                "SDT": sdt,
                "vaiTro": "Nhân viên"
            }
            employees.append(new_nv)
            with open("data/nhan-vien.json", "w", encoding="utf-8") as f:
                json.dump(employees, f, ensure_ascii=False, indent=2)

            try:
                with open("data/tai-khoan.json", "r", encoding="utf-8") as f:
                    accounts = json.load(f)
            except:
                accounts = []
            accounts.append({
                "taiKhoan": ma,
                "matKhau": "12345",
                "vaiTro": "employee"
            })
            with open("data/tai-khoan.json", "w", encoding="utf-8") as f:
                json.dump(accounts, f, ensure_ascii=False, indent=2)

            popup.destroy()
            show_employee_tab(parent)

        tk.Button(popup, text="Lưu", bg="green", fg="white", command=save_new).pack(pady=10)

    tk.Button(frame, text="Thêm nhân viên", bg="green", fg="white", font=("Arial", 10), command=open_add_popup).pack(pady=10)
