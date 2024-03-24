import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pyAesCrypt

def encrypt_file():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    file_path = filedialog.askopenfilename(title="Select File to Encrypt",
                                            filetypes=[("All Files", "*.*")])
    if file_path:
        encrypted_file_path = file_path + ".aes"
        bufferSize = 64 * 1024
        pyAesCrypt.encryptFile(file_path, encrypted_file_path, password, bufferSize)
        show_completion_message("Encryption", encrypted_file_path)

def decrypt_file():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    file_path = filedialog.askopenfilename(title="Select File to Decrypt",
                                            filetypes=[("AES Encrypted Files", "*.aes")])
    if file_path:
        decrypted_file_path = file_path.replace(".aes", "")
        try:
            pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)
            show_completion_message("Decryption", decrypted_file_path)
        except ValueError:
            messagebox.showerror("Error", "Invalid password. Decryption failed.")

def show_completion_message(action, file_path):
    message = f"{action} completed successfully!\nFile created at:\n{file_path}"
    messagebox.showinfo("Success", message)

root = tk.Tk()
root.geometry("300x300")
#root.iconbitmap(default="favicon.ico") #windows
root.iconbitmap('favicon.ico') #mac
root.title("File En/Decryptor")

password_label = tk.Label(root, text="Enter Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_file)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_file)
decrypt_button.pack()

root.mainloop()
