
from __future__ import annotations

import os
import threading
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

from crypto_engine import encrypt_file, decrypt_file, CryptoError

class MasterEncryptionApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.geometry("600x480")
        self.root.title("Master Encryption")

        # Theme
        self.fg_color = "#EEEEEE"
        self.primary = "#601E88"
        self.accent = "#E44982"
        self.border = "#D7D7D7"

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.configure(bg=self.fg_color)

        # Images (safe loader)
        def safe_ctk_image(path, size):
            try:
                img = Image.open(path)
                return ctk.CTkImage(dark_image=img, light_image=img, size=size)
            except Exception:
                return None

        self.side_img = safe_ctk_image("data/side-img2.png", (300, 480))
        self.password_icon = safe_ctk_image("data/password-icon.png", (17, 17))

        # Layout
        self.left = ctk.CTkFrame(self.root, width=300, corner_radius=0, fg_color="white")
        # self.left.pack(side="left", fill="y")  # optional
        self.right = ctk.CTkFrame(self.root, fg_color=self.fg_color)
        self.right.pack(side="right", fill="both", expand=True)

        if self.side_img:
            ctk.CTkLabel(self.left, image=self.side_img, text="").place(x=0, y=0, relwidth=1, relheight=1)
        else:
            ctk.CTkLabel(self.left, text="Master Encryption", text_color=self.primary,
                         font=ctk.CTkFont(size=24, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

        self.secret = tk.StringVar()
        self.cancel_event = None  # set during operations
        self.worker_thread = None

        self._build_unlock_screen()

    # -------- Screens --------
    def _build_unlock_screen(self):
        for w in self.right.winfo_children():
            w.destroy()

        wrapper = ctk.CTkFrame(self.right, fg_color="white", corner_radius=16,
                               border_color=self.border, border_width=1)
        wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.7)

        ctk.CTkLabel(wrapper, text="Enter Secret Key", text_color=self.primary,
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(24, 8))
        ctk.CTkLabel(wrapper, text="This key is required for encryption/decryption in this session.",
                     text_color="#666666").pack(pady=(0, 18))

        row = ctk.CTkFrame(wrapper, fg_color="white")
        row.pack(pady=(8, 4), padx=24, fill="x")

        if self.password_icon:
            ctk.CTkLabel(row, image=self.password_icon, text="").pack(side="left", padx=(0, 8))

        self.secret_entry = ctk.CTkEntry(row, placeholder_text="Secret key (password)",
                                         show="•", width=360, height=38)
        self.secret_entry.pack(side="left", fill="x", expand=True)

        self.show_var = tk.BooleanVar(value=False)
        def toggle_show():
            self.secret_entry.configure(show="" if self.show_var.get() else "•")
        ctk.CTkCheckBox(wrapper, text="Show key", command=toggle_show,
                        variable=self.show_var).pack(pady=(4, 16))

        ctk.CTkButton(wrapper, text="Unlock", fg_color=self.primary, hover_color=self.accent,
                      command=self._unlock).pack(pady=(6, 12))

        ctk.CTkLabel(wrapper, text="Tip: Keep your passphrase safe. Without it, data cannot be recovered.",
                     text_color="#888888", wraplength=420, justify="center").pack(pady=(6, 10))

    def _build_action_screen(self):
        for w in self.right.winfo_children():
            w.destroy()

        wrapper = ctk.CTkFrame(self.right, fg_color="white", corner_radius=16,
                               border_color=self.border, border_width=1)
        wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.7)

        # Back button (top-left inside card)
        self.back_btn = ctk.CTkButton(wrapper, text="← Back", width=80, fg_color="#AAAAAA",
                                      hover_color="#888888", command=self._go_back)
        self.back_btn.place(x=12, y=12)

        ctk.CTkLabel(wrapper, text="Choose an Action", text_color=self.primary,
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(24, 12))

        row = ctk.CTkFrame(wrapper, fg_color="white")
        row.pack(pady=12)

        self.encrypt_btn = ctk.CTkButton(row, text="Encryption", width=160, height=46,
                                         fg_color=self.primary, hover_color=self.accent,
                                         command=self._on_encrypt_clicked)
        self.encrypt_btn.grid(row=0, column=0, padx=12)

        self.decrypt_btn = ctk.CTkButton(row, text="Decryption", width=160, height=46,
                                         fg_color="#444444", hover_color="#111111",
                                         command=self._on_decrypt_clicked)
        self.decrypt_btn.grid(row=0, column=1, padx=12)

        # Progress + status + cancel
        self.progress = ctk.CTkProgressBar(wrapper)
        self.progress.pack(pady=(20, 6))
        self.progress.set(0)

        self.status_var = tk.StringVar(value="Ready.")
        ctk.CTkLabel(wrapper, textvariable=self.status_var, text_color="#666666").pack(pady=(4, 6))

        self.cancel_btn = ctk.CTkButton(wrapper, text="Cancel", fg_color="#C62828",
                                        hover_color="#8E0000", command=self._on_cancel)
        self.cancel_btn.pack()
        self.cancel_btn.configure(state="disabled")

    # -------- Helpers --------
    def _unlock(self):
        key = self.secret_entry.get().strip()
        if not key:
            messagebox.showwarning("Secret Key Required", "Please enter a non-empty secret key.")
            return
        self.secret.set(key)
        self._build_action_screen()

    def _go_back(self):
        # Return to login screen; clear secret field for safety
        self.secret.set("")
        self._build_unlock_screen()

    def _disable_actions(self):
        for w in (self.encrypt_btn, self.decrypt_btn):
            w.configure(state="disabled")
        # Disable Back during active work to avoid tearing down UI mid-operation
        if hasattr(self, "back_btn"):
            self.back_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.root.update_idletasks()

    def _enable_actions(self):
        for w in (self.encrypt_btn, self.decrypt_btn):
            w.configure(state="normal")
        if hasattr(self, "back_btn"):
            self.back_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.root.update_idletasks()

    def _choose_file(self, title: str) -> str | None:
        return filedialog.askopenfilename(title=title) or None

    # Thread-safe UI updates
    def _report_progress(self, value: float):
        def _apply():
            try:
                self.progress.set(max(0.0, min(1.0, value)))
            except Exception:
                pass
        self.root.after(0, _apply)

    def _set_status(self, text: str):
        def _apply():
            self.status_var.set(text)
        self.root.after(0, _apply)

    def _on_cancel(self):
        if self.cancel_event and not self.cancel_event.is_set():
            self.cancel_event.set()
            self._set_status("Cancelling...")

    def _run_worker(self, fn, *args, op_name="Operation",
                    source_path: str | None = None,
                    delete_source_on_success: bool = False):
        # Prepare cancel token
        self.cancel_event = threading.Event()

        def work():
            try:
                out_path = fn(
                    *args,
                    progress=self._report_progress,
                    is_cancelled=self.cancel_event.is_set,
                )

                # If decryption succeeded, optionally delete the source encrypted file
                deleted_note = ""
                if delete_source_on_success and source_path and os.path.isfile(source_path):
                    try:
                        os.remove(source_path)
                        deleted_note = "\n\nOriginal encrypted file was deleted."
                    except Exception as de:
                        deleted_note = f"\n\nNote: Couldn't delete the original encrypted file:\n{de}"

                self._set_status(f"{op_name} complete: {os.path.basename(out_path)}")
                messagebox.showinfo("Success", f"{op_name} completed.\n\nOutput:\n{out_path}{deleted_note}")

            except CryptoError as e:
                msg = str(e)
                if "cancelled" in msg.lower():
                    self._set_status("Cancelled.")
                    messagebox.showinfo("Cancelled", f"{op_name} was cancelled.")
                else:
                    self._set_status("Error")
                    messagebox.showerror("Error", msg)
            except Exception as e:
                self._set_status("Error")
                tb = traceback.format_exc(limit=2)
                messagebox.showerror("Unexpected Error", f"{e}\n\n{tb}")
            finally:
                self.cancel_event = None
                self._enable_actions()

        # Start worker
        self.worker_thread = threading.Thread(target=work, daemon=True)
        self.worker_thread.start()

    # -------- Button handlers --------
    def _on_encrypt_clicked(self):
        self._disable_actions()
        path = self._choose_file("Choose a file to ENCRYPT")
        self._enable_actions()
        if not path:
            self._set_status("Cancelled.")
            self.progress.set(0)
            return
        self.progress.set(0)
        self._set_status("Encrypting...")
        self._disable_actions()
        self._run_worker(encrypt_file, self.secret.get(), path, None, op_name="Encryption")

    def _on_decrypt_clicked(self):
        self._disable_actions()
        path = self._choose_file("Choose a file to DECRYPT (.enc)")
        self._enable_actions()
        if not path:
            self._set_status("Cancelled.")
            self.progress.set(0)
            return
        self.progress.set(0)
        self._set_status("Decrypting...")
        self._disable_actions()
        # Pass the source path and request deletion on success
        self._run_worker(decrypt_file, self.secret.get(), path, None,
                         op_name="Decryption", source_path=path, delete_source_on_success=True)


def main():
    root = ctk.CTk()
    app = MasterEncryptionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
