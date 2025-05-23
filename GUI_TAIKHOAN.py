import tkinter as tk
from tkinter import messagebox, ttk
import json

def show_account_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    try:
        with open("data/tai-khoan.json", "r", encoding="utf-8") as f:
            accounts = json.load(f)
    except:
        accounts = []

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Quản lý tài khoản", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=(10, 5))

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

    def save_accounts():
        with open("data/tai-khoan.json", "w", encoding="utf-8") as f:
            json.dump(accounts, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Thành công", "Đã cập nhật tài khoản.")

    for idx, acc in enumerate(accounts):
        row = tk.Frame(scrollable, bg="#f9f9f9", bd=1, relief="solid", pady=5)
        row.pack(fill="x", pady=5)

        tk.Label(row, text=f"Tài khoản: {acc['taiKhoan']}", bg="#f9f9f9", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)

        sub = tk.Frame(row, bg="#f9f9f9")
        sub.pack(fill="x", padx=10, pady=5)

        tk.Label(sub, text="Mật khẩu:", bg="#f9f9f9").grid(row=0, column=0, sticky="w")
        mk_var = tk.StringVar(value=acc['matKhau'])
        tk.Entry(sub, textvariable=mk_var, width=20).grid(row=0, column=1, padx=5)

        tk.Label(sub, text="Vai trò:", bg="#f9f9f9").grid(row=0, column=2, padx=(15, 0))
        role_var = tk.StringVar(value=acc['vaiTro'])
        role_menu = ttk.Combobox(sub, textvariable=role_var, values=["admin", "employee"], state="readonly", width=15)
        role_menu.grid(row=0, column=3, padx=5)

        def update_account(i=idx, mkv=mk_var, rv=role_var):
            new_password = mkv.get().strip()
            if len(new_password) < 5:
                messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 5 ký tự.")
                return
            accounts[i]['matKhau'] = new_password
            accounts[i]['vaiTro'] = rv.get()
            save_accounts()

        tk.Button(sub, text="Lưu", bg="blue", fg="white", command=update_account).grid(row=0, column=4, padx=10)

    if not accounts:
        tk.Label(scrollable, text="Không có tài khoản nào.", bg="white", fg="gray", font=("Arial", 11)).pack(pady=20)
