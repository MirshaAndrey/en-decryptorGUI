import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyAesCrypt
import threading
import platform
import os
import time
from pathlib import Path


class AESEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.current_theme = "light"
        self.setup_window()
        self.create_styles()
        self.create_widgets()
        self.apply_theme()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("AES File Encryptor/Decryptor Pro")
        self.root.geometry("500x400")
        self.root.resizable(True, False)
        self.root.minsize(500, 600)

        # Icon compatibility
        if platform.system() == "Windows":
            try:
                self.root.iconbitmap("favicon.ico")
            except:
                pass
        else:
            if os.path.exists("favicon.png"):
                icon_img = tk.PhotoImage(file="favicon.png")
                self.root.iconphoto(True, icon_img)

    def create_styles(self):
        """Create custom styles for the application"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Custom styles
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"))
        self.style.configure("Theme.TButton", font=("Segoe UI", 9))
        self.style.configure("Status.TLabel", font=("Segoe UI", 9, "italic"))

    def create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="25")
        self.main_frame.grid(row=0, column=0, sticky="NSEW")

        # Header section
        self.create_header()

        # File selection section
        self.create_file_section()

        # Password section
        self.create_password_section()

        # Action buttons section
        self.create_action_section()

        # Progress section
        self.create_progress_section()

        # Footer section
        self.create_footer()

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def create_header(self):
        """Create header section with title and subtitle"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="EW")

        title_label = ttk.Label(header_frame, text="🔒 AES File Encryptor", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2)

        subtitle_label = ttk.Label(header_frame, text="Secure your files with military-grade AES-256 encryption",
                                   style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))

    def create_file_section(self):
        """Create file selection section"""
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="EW")
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text="Selected File:").grid(row=0, column=0, sticky="W", padx=(0, 10))

        self.file_path_var = tk.StringVar(value="No file selected")
        self.file_label = ttk.Label(file_frame, textvariable=self.file_path_var,
                                    foreground="gray", font=("Segoe UI", 9))
        self.file_label.grid(row=0, column=1, sticky="W")

        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="EW")

        ttk.Button(button_frame, text="📁 Browse File",
                   command=self.browse_file).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="🗑️ Clear",
                   command=self.clear_file).grid(row=0, column=1)

    def create_password_section(self):
        """Create password input section"""
        password_frame = ttk.LabelFrame(self.main_frame, text="Security", padding="10")
        password_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15), sticky="EW")
        password_frame.columnconfigure(1, weight=1)

        ttk.Label(password_frame, text="Password:").grid(row=0, column=0, sticky="W", padx=(0, 10))

        self.password_entry = ttk.Entry(password_frame, show="*", width=25, font=("Segoe UI", 10))
        self.password_entry.grid(row=0, column=1, sticky="EW", padx=(0, 10))

        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(password_frame, text="Show",
                                                   variable=self.show_password_var,
                                                   command=self.toggle_password_visibility)
        self.show_password_check.grid(row=0, column=2)

        # Password strength indicator
        self.strength_var = tk.StringVar(value="Enter password")
        self.strength_label = ttk.Label(password_frame, textvariable=self.strength_var,
                                        font=("Segoe UI", 8))
        self.strength_label.grid(row=1, column=0, columnspan=3, pady=(5, 0), sticky="W")

        self.password_entry.bind('<KeyRelease>', self.check_password_strength)

    def create_action_section(self):
        """Create action buttons section"""
        action_frame = ttk.LabelFrame(self.main_frame, text="Actions", padding="10")
        action_frame.grid(row=3, column=0, columnspan=2, pady=(0, 15), sticky="EW")
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        self.encrypt_button = ttk.Button(action_frame, text="🔒 Encrypt File",
                                         command=self.encrypt_file, style="Action.TButton")
        self.encrypt_button.grid(row=0, column=0, padx=(0, 5), sticky="EW")

        self.decrypt_button = ttk.Button(action_frame, text="🔓 Decrypt File",
                                         command=self.decrypt_file, style="Action.TButton")
        self.decrypt_button.grid(row=0, column=1, padx=(5, 0), sticky="EW")

    def create_progress_section(self):
        """Create progress section"""
        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.grid(row=4, column=0, columnspan=2, pady=(0, 15), sticky="EW")
        progress_frame.columnconfigure(0, weight=1)

        self.progress_label = ttk.Label(progress_frame, text="", style="Status.TLabel")
        self.progress_label.grid(row=0, column=0, sticky="W")

        self.progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate")
        self.progress_bar.grid(row=1, column=0, sticky="EW", pady=(5, 0))

    def create_footer(self):
        """Create footer section"""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.grid(row=5, column=0, columnspan=2, sticky="EW")
        footer_frame.columnconfigure(0, weight=1)

        theme_button = ttk.Button(footer_frame, text="🌓 Toggle Theme",
                                  command=self.toggle_theme, style="Theme.TButton")
        theme_button.grid(row=0, column=0, sticky="W")

        info_button = ttk.Button(footer_frame, text="ℹ️ About",
                                 command=self.show_about, style="Theme.TButton")
        info_button.grid(row=0, column=1, sticky="E")

    def browse_file(self):
        """Browse and select a file"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"),
                ("Document Files", "*.pdf;*.doc;*.docx"),
                ("AES Encrypted Files", "*.aes")
            ]
        )
        if file_path:
            self.file_path_var.set(os.path.basename(file_path))
            self.selected_file_path = file_path
            self.file_label.configure(foreground="black" if self.current_theme == "light" else "white")

    def clear_file(self):
        """Clear selected file"""
        self.file_path_var.set("No file selected")
        self.selected_file_path = None
        self.file_label.configure(foreground="gray")

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def check_password_strength(self, event=None):
        """Check and display password strength"""
        password = self.password_entry.get()
        if not password:
            self.strength_var.set("Enter password")
            self.strength_label.configure(foreground="gray")
            return

        strength = 0
        feedback = []

        if len(password) >= 8:
            strength += 1
        else:
            feedback.append("8+ chars")

        if any(c.isupper() for c in password):
            strength += 1
        else:
            feedback.append("uppercase")

        if any(c.islower() for c in password):
            strength += 1
        else:
            feedback.append("lowercase")

        if any(c.isdigit() for c in password):
            strength += 1
        else:
            feedback.append("number")

        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength += 1
        else:
            feedback.append("special char")

        if strength <= 2:
            self.strength_var.set("⚠️ Weak - Add: " + ", ".join(feedback[:2]))
            self.strength_label.configure(foreground="red")
        elif strength <= 3:
            self.strength_var.set("🔶 Medium - Add: " + ", ".join(feedback[:1]))
            self.strength_label.configure(foreground="orange")
        elif strength <= 4:
            self.strength_var.set("✅ Strong")
            self.strength_label.configure(foreground="green")
        else:
            self.strength_var.set("🔒 Very Strong")
            self.strength_label.configure(foreground="darkgreen")

    def encrypt_file(self):
        """Start file encryption"""
        if not self.validate_inputs():
            return
        self.start_task("🔒 Encrypting file...", self._encrypt)

    def decrypt_file(self):
        """Start file decryption"""
        if not self.validate_inputs():
            return
        self.start_task("🔓 Decrypting file...", self._decrypt)

    def validate_inputs(self):
        """Validate user inputs"""
        if not hasattr(self, 'selected_file_path') or not self.selected_file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return False

        if not os.path.exists(self.selected_file_path):
            messagebox.showerror("Error", "Selected file does not exist.")
            return False

        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return False

        if len(password) < 4:
            messagebox.showwarning("Warning",
                                   "Password is very short. Consider using a longer password for better security.")

        return True

    def _encrypt(self):
        """Perform file encryption"""
        try:
            password = self.password_entry.get()
            file_path = self.selected_file_path
            encrypted_file_path = file_path + ".aes"

            # Check if encrypted file already exists
            if os.path.exists(encrypted_file_path):
                result = messagebox.askyesno("File Exists",
                                             f"Encrypted file already exists:\n{os.path.basename(encrypted_file_path)}\n\nOverwrite?")
                if not result:
                    return

            buffer_size = 64 * 1024
            pyAesCrypt.encryptFile(file_path, encrypted_file_path, password, buffer_size)

            file_size = os.path.getsize(encrypted_file_path)
            self.show_completion_message("Encryption", encrypted_file_path, file_size)

        except Exception as e:
            messagebox.showerror("Encryption Error", f"An error occurred during encryption:\n{str(e)}")

    def _decrypt(self):
        """Perform file decryption"""
        try:
            password = self.password_entry.get()
            file_path = self.selected_file_path

            if not file_path.endswith('.aes'):
                messagebox.showwarning("Warning", "Selected file doesn't appear to be an AES encrypted file.")

            decrypted_file_path = file_path.replace(".aes", "")

            # Check if decrypted file already exists
            if os.path.exists(decrypted_file_path):
                result = messagebox.askyesno("File Exists",
                                             f"Decrypted file already exists:\n{os.path.basename(decrypted_file_path)}\n\nOverwrite?")
                if not result:
                    return

            pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)

            file_size = os.path.getsize(decrypted_file_path)
            self.show_completion_message("Decryption", decrypted_file_path, file_size)

        except ValueError as e:
            messagebox.showerror("Decryption Error", "Invalid password or corrupted file. Decryption failed.")
        except Exception as e:
            messagebox.showerror("Decryption Error", f"An error occurred during decryption:\n{str(e)}")

    def start_task(self, label, task_func):
        """Start a long-running task with progress indication"""
        self.progress_label.config(text=label)
        self.progress_bar.start(10)
        self.encrypt_button.configure(state="disabled")
        self.decrypt_button.configure(state="disabled")

        threading.Thread(target=self.run_task, args=(task_func,), daemon=True).start()

    def run_task(self, task_func):
        """Run task in separate thread"""
        try:
            task_func()
        finally:
            self.root.after(0, self.task_completed)

    def task_completed(self):
        """Called when task is completed"""
        self.progress_bar.stop()
        self.progress_label.config(text="")
        self.encrypt_button.configure(state="normal")
        self.decrypt_button.configure(state="normal")

    def show_completion_message(self, action, file_path, file_size):
        """Show completion message with file info"""
        file_size_mb = file_size / (1024 * 1024)
        size_text = f"{file_size_mb:.2f} MB" if file_size_mb >= 1 else f"{file_size / 1024:.1f} KB"

        message = (f"{action} completed successfully!\n\n"
                   f"File: {os.path.basename(file_path)}\n"
                   f"Size: {size_text}\n"
                   f"Location: {os.path.dirname(file_path)}")

        messagebox.showinfo("Success", message)

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme"""
        if self.current_theme == "dark":
            bg = "#2b2b2b"
            fg = "#ffffff"
            entry_bg = "#404040"
            select_bg = "#0d7377"
        else:
            bg = "#f0f0f0"
            fg = "#333333"
            entry_bg = "#ffffff"
            select_bg = "#0078d4"

        # Configure styles
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TLabelframe", background=bg, foreground=fg)
        self.style.configure("TLabelframe.Label", background=bg, foreground=fg)
        self.style.configure("TButton", background=bg, foreground=fg)
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=fg)
        self.style.configure("TCheckbutton", background=bg, foreground=fg)

        self.root.configure(background=bg)

        # Update file label color if file is selected
        if hasattr(self, 'selected_file_path') and self.selected_file_path:
            self.file_label.configure(foreground=fg)

    def show_about(self):
        """Show about dialog"""
        about_text = """AES File Encryptor/Decryptor Pro v2.0

A secure file encryption tool using AES-256 encryption.

Features:
• Military-grade AES-256 encryption
• Password strength indicator
• Dark/Light theme support
• File overwrite protection
• Detailed completion messages
• Modern, user-friendly interface

Developed with Python & Tkinter
Uses pyAesCrypt library for encryption"""

        messagebox.showinfo("About", about_text)


def main():
    root = tk.Tk()
    app = AESEncryptorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
