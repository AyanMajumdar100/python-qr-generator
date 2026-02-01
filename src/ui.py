import logging
import threading
from typing import Optional
from urllib.parse import urlparse

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

from src.logic import (
    QRCodeGenerator,
    QRCodeDataTooLargeError,
    QRCodeGenerationError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QRCodeApp(tk.Tk):
    PREVIEW_SIZE = (300, 300)
    SMALL_SIZE = "760x520"
    FULL_SIZE = "1150x620"

    def __init__(self) -> None:
        super().__init__()

        self.title("QR Code Generator")
        self.geometry(self.SMALL_SIZE)
        self.minsize(740, 500)
        self.configure(bg="#f8f9fb")
        self.resizable(True, True)

        self._qr_image_original: Optional[Image.Image] = None
        self._qr_image_preview: Optional[ImageTk.PhotoImage] = None
        self._active_tab = "URL"
        self._preview_visible = False

        self._setup_root_grid()
        self._build_tabs()
        self._build_main_area()

    def _setup_root_grid(self) -> None:
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _build_tabs(self) -> None:
        self.tab_bar = tk.Frame(self, bg="#f5f7fa", height=60)
        self.tab_bar.grid(row=0, column=0, sticky="ew")
        self.tab_bar.grid_propagate(False)

        self.tabs = {}

        for name in ("URL", "WiFi", "WhatsApp", "Text", "Email"):
            btn = tk.Button(
                self.tab_bar,
                text=name,
                font=("Poppins", 11, "bold"),
                padx=26,
                pady=14,
                relief="flat",
                bg="#e9edf2",
                fg="#333",
                cursor="hand2",
                command=lambda n=name: self._switch_tab(n),
            )
            btn.pack(side=tk.LEFT, padx=8, pady=10)
            self.tabs[name] = btn

        self._set_active_tab("URL")

    def _set_active_tab(self, name: str) -> None:
        for tab, btn in self.tabs.items():
            btn.configure(
                bg="#0d6efd" if tab == name else "#e9edf2",
                fg="white" if tab == name else "#333",
            )

    def _switch_tab(self, name: str) -> None:
        self._active_tab = name
        self._set_active_tab(name)
        self._hide_preview()

        for widget in self.left_panel.winfo_children():
            widget.destroy()

        if name == "URL":
            self._render_url_form()
        else:
            self._render_placeholder(name)

    def _build_main_area(self) -> None:
        self.main = tk.Frame(self, bg="#f8f9fb")
        self.main.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)

        self.main.columnconfigure(0, weight=1)
        self.main.columnconfigure(1, weight=1)
        self.main.rowconfigure(0, weight=1)

        self.left_panel = tk.Frame(self.main, bg="white")
        self.left_panel.grid(row=0, column=0, sticky="nw", padx=(20, 40), pady=20)

        self.right_panel = tk.Frame(self.main, bg="white")

        self._render_url_form()
        self._build_preview()

    def _render_placeholder(self, name: str) -> None:
        tk.Label(
            self.left_panel,
            text=f"{name} QR coming soon",
            font=("Poppins", 16, "bold"),
            bg="white",
        ).pack(padx=40, pady=60)

    def _render_url_form(self) -> None:
        tk.Label(
            self.left_panel,
            text="Generate URL QR Code",
            font=("Poppins", 20, "bold"),
            bg="white",
        ).pack(anchor="w", padx=40, pady=(30, 24))

        tk.Label(
            self.left_panel,
            text="Enter URL",
            font=("Poppins", 10),
            fg="#555",
            bg="white",
        ).pack(anchor="w", padx=40)

        self.input_entry = ttk.Entry(self.left_panel, width=44)
        self.input_entry.pack(padx=40, pady=12, ipady=6)

        tk.Button(
            self.left_panel,
            text="Generate QR Code",
            font=("Poppins", 11, "bold"),
            bg="#0d6efd",
            fg="white",
            activebackground="#0b5ed7",
            activeforeground="white",
            padx=22,
            pady=12,
            relief="flat",
            cursor="hand2",
            command=self._on_generate,
        ).pack(anchor="w", padx=40, pady=22)

    def _build_preview(self) -> None:
        self.preview_container = tk.Frame(
            self.right_panel,
            bg="#f8f9fb",
            width=340,
            height=340,
        )
        self.preview_container.pack(padx=40, pady=(30, 20))
        self.preview_container.pack_propagate(False)

        self.preview_label = tk.Label(self.preview_container, bg="#f8f9fb")
        self.preview_label.pack(expand=True)

        self.save_btn = tk.Button(
            self.right_panel,
            text="⬇ Download QR Code",
            font=("Poppins", 11, "bold"),
            bg="#198754",
            fg="white",
            activebackground="#157347",
            activeforeground="white",
            disabledforeground="white",
            padx=22,
            pady=12,
            relief="flat",
            cursor="hand2",
            state=tk.DISABLED,
            command=self._on_save,
        )
        self.save_btn.pack(pady=10)

    def _show_preview(self) -> None:
        if not self._preview_visible:
            self.geometry(self.FULL_SIZE)
            self.right_panel.grid(row=0, column=1, sticky="n", padx=(40, 20), pady=20)
            self._preview_visible = True

    def _hide_preview(self) -> None:
        if self._preview_visible:
            self.right_panel.grid_remove()
            self.geometry(self.SMALL_SIZE)
            self._preview_visible = False

    def _validate_url(self, raw: str) -> Optional[str]:
        raw = raw.strip()
        if not raw:
            return None
        parsed = urlparse(raw if "://" in raw else f"https://{raw}")
        return parsed.geturl() if parsed.netloc else None

    def _on_generate(self) -> None:
        url = self._validate_url(self.input_entry.get())
        if not url:
            messagebox.showwarning("Invalid URL", "Please enter a valid URL.")
            return

        self.save_btn.config(state=tk.DISABLED)

        threading.Thread(
            target=self._run_generation,
            args=(url,),
            daemon=True,
        ).start()

    def _run_generation(self, data: str) -> None:
        try:
            img = QRCodeGenerator.generate_qr(data)
            preview = img.resize(self.PREVIEW_SIZE, Image.LANCZOS)

            self._qr_image_original = img
            self._qr_image_preview = ImageTk.PhotoImage(preview)

            self.after(0, self._update_preview)

        except (QRCodeDataTooLargeError, QRCodeGenerationError) as exc:
            self.after(0, lambda: messagebox.showerror("Error", str(exc)))

    def _update_preview(self) -> None:
        self.preview_label.configure(image=self._qr_image_preview)
        self.save_btn.config(state=tk.NORMAL)
        self._show_preview()

    def _on_save(self) -> None:
        if not self._qr_image_original:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
        )
        if path:
            self._qr_image_original.save(path, format="PNG")
