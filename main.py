import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyAesCrypt
import threading
import platform
import os

# === Theme control ===
current_theme = "light"

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

def apply_theme():
    bg = "#2e2e2e" if current_theme == "dark" else "#ffffff"
    fg = "#006b17" if current_theme == "dark" else "#828282"
    entry_bg = "#2e2e2e" if current_theme == "dark" else "#ffffff"

    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", background=bg, foreground=fg)
    style.configure("TEntry", fieldbackground=entry_bg, foreground=fg)
    root.configure(background=bg)

    for widget in main_frame.winfo_children():
        if isinstance(widget, ttk.Entry):
            widget.configure(foreground=fg)

# === File Encryption ===
def encrypt_file():
    start_task("Encrypting...", _encrypt)

def decrypt_file():
    start_task("Decrypting...", _decrypt)

def _encrypt():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    file_path = filedialog.askopenfilename(title="Select File to Encrypt", filetypes=[("All Files", "*.*")])
    if file_path:
        encrypted_file_path = file_path + ".aes"
        bufferSize = 64 * 1024
        pyAesCrypt.encryptFile(file_path, encrypted_file_path, password, bufferSize)
        show_completion_message("Encryption", encrypted_file_path)

def _decrypt():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    file_path = filedialog.askopenfilename(title="Select File to Decrypt", filetypes=[("AES Encrypted Files", "*.aes")])
    if file_path:
        decrypted_file_path = file_path.replace(".aes", "")
        try:
            pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)
            show_completion_message("Decryption", decrypted_file_path)
        except ValueError:
            messagebox.showerror("Error", "Invalid password. Decryption failed.")

# === Threading for long operations ===
def start_task(label, task_func):
    progress_label.config(text=label)
    progress_bar.start()
    threading.Thread(target=run_task, args=(task_func,), daemon=True).start()

def run_task(task_func):
    try:
        task_func()
    finally:
        progress_bar.stop()
        progress_label.config(text="")

# === Completion message ===
def show_completion_message(action, file_path):
    message = f"{action} completed successfully!\nFile created at:\n{file_path}"
    messagebox.showinfo("Success", message)

# === UI ===
root = tk.Tk()
root.title("AES File En/Decryptor")
root.geometry("400x250")
root.resizable(False, False)

# Icon compatibility
if platform.system() == "Windows":
    try:
        root.iconbitmap("favicon.ico")
    except:
        pass
else:
    if os.path.exists("favicon.png"):
        icon_img = tk.PhotoImage(file="favicon.png")
        root.iconphoto(True, icon_img)

style = ttk.Style()
style.theme_use("clam")

# Main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky="NSEW")

title_label = ttk.Label(main_frame, text="AES File Encryptor/Decryptor", font=("Segoe UI", 12, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

ttk.Label(main_frame, text="Enter Password:").grid(row=1, column=0, sticky="E")
password_entry = ttk.Entry(main_frame, show="*", width=30)
password_entry.grid(row=1, column=1, pady=5, sticky="W")

encrypt_button = ttk.Button(main_frame, text="Encrypt File", command=encrypt_file)
encrypt_button.grid(row=2, column=0, columnspan=2, pady=(10, 5), sticky="EW")

decrypt_button = ttk.Button(main_frame, text="Decrypt File", command=decrypt_file)
decrypt_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="EW")

theme_button = ttk.Button(main_frame, text="White/Dark", command=toggle_theme)
theme_button.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="EW")

# Progress
progress_label = ttk.Label(main_frame, text="", font=("Segoe UI", 10, "italic"))
progress_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

progress_bar = ttk.Progressbar(main_frame, mode="indeterminate")
progress_bar.grid(row=6, column=0, columnspan=2, sticky="EW", pady=5)

main_frame.columnconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

apply_theme()
root.mainloop()
