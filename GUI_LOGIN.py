import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
from JSON_TAIKHOAN import JSON_R_TAIKHOAN

def toggle_password():
    if show_password.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")

def sign_in():
    username = entry_email.get().strip()
    password = entry_password.get().strip()

    ds_taikhoan = JSON_R_TAIKHOAN()
    if not ds_taikhoan:
        messagebox.showerror("Lỗi", "Không đọc được dữ liệu tài khoản!")
        return

    for acc in ds_taikhoan:
        if acc["taiKhoan"] == username and acc["matKhau"] == password:
            role = acc.get("vaiTro", "").lower()
            root.destroy()  

            if role == "admin":
                import GUI_ADMIN
            elif role == "employee":
                import GUI_EMPLOYEE
            else:
                messagebox.showerror("Lỗi", f"Không xác định vai trò: {role}")
            return

    messagebox.showerror("Đăng nhập thất bại", "Tài khoản hoặc mật khẩu không đúng.")


def main():
    global root, entry_email, entry_password, show_password  
    root = tk.Tk()
    root.title("Đăng nhập")
    root.geometry("300x400")
    root.configure(bg="black")
    root.resizable(False, False)


    logo_img = Image.open("img/logo.png")
    logo_img = logo_img.resize((90, 30))
    logo_tk = ImageTk.PhotoImage(logo_img)
    tk.Label(root, image=logo_tk, bg="black").pack(pady=(30, 10))

    frame = tk.Frame(root, bg="white", padx=20, pady=20)
    frame.pack(pady=10)

    tk.Label(frame, text="ĐĂNG NHẬP", font=("Helvetica", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 20))
    tk.Label(frame, text="Tài khoản:", bg="white").grid(row=1, column=0, sticky="w")
    entry_email = tk.Entry(frame, width=30)
    entry_email.grid(row=2, column=0, columnspan=2, pady=(0, 10))

    tk.Label(frame, text="Mật khẩu:", bg="white").grid(row=3, column=0, sticky="w")
    entry_password = tk.Entry(frame, width=30, show="*")
    entry_password.grid(row=4, column=0, columnspan=2, pady=(0, 10))

    show_password = tk.BooleanVar()
    tk.Checkbutton(frame, text="Hiển thị mật khẩu", variable=show_password, command=toggle_password, bg="white").grid(row=5, column=0, columnspan=2, sticky="w")

    tk.Button(frame, text="Đăng nhập", bg="black", fg="white", width=25, pady=5, command=sign_in).grid(row=7, column=0, columnspan=2, pady=(10, 0))

    root.mainloop()
if __name__ == "__main__":
    main()

