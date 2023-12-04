import tkinter as tk
import pyAesCrypt
from tkinter import filedialog
from tkinter import messagebox

# Функция для шифрования файла
def encrypt_file():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    file_path = filedialog.askopenfilename()
    if file_path:
        encrypted_file_path = file_path + ".aes"
        pyAesCrypt.encryptFile(file_path, encrypted_file_path, password)
        messagebox.showinfo("Success", "File encrypted successfully!")

# Функция для дешифрования файла
def decrypt_file():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    file_path = filedialog.askopenfilename()
    if file_path:
        decrypted_file_path = file_path.replace(".aes", "")
        pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)
        messagebox.showinfo("Success", "File decrypted successfully!")

# Создание графического интерфейса
root = tk.Tk()
root.geometry("300x250")
#root.iconbitmap(default="favicon.ico") #windows
root.iconbitmap('favicon.ico') #mac
root.title("File En/Decryptor")

password_label = tk.Label(root, text="Enter Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*")  # Пароль будет скрыт
password_entry.pack()

encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_file)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_file)
decrypt_button.pack()

root.mainloop()
