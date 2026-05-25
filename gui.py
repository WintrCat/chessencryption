import os
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from encode import encode
from decode import decode


def encode_file_to_pgn(path: str) -> str:
    return encode(path)


def decode_pgn_to_bytes(pgn_text: str) -> bytes:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".bin")
    tmp.close()
    try:
        decode(pgn_text, tmp.name)
        with open(tmp.name, "rb") as f:
            return f.read()
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


class EncodeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)

        file_row = ttk.Frame(self)
        file_row.pack(fill="x", pady=(0, 8))
        ttk.Label(file_row, text="Input file:").pack(side="left")
        self.path_var = tk.StringVar()
        ttk.Entry(file_row, textvariable=self.path_var).pack(
            side="left", fill="x", expand=True, padx=6
        )
        ttk.Button(file_row, text="Browse…", command=self._browse).pack(side="left")

        btn_row = ttk.Frame(self)
        btn_row.pack(fill="x", pady=(0, 8))
        self.encode_btn = ttk.Button(btn_row, text="Encode → PGN", command=self._encode)
        self.encode_btn.pack(side="left")
        ttk.Button(btn_row, text="Copy PGN", command=self._copy).pack(side="left", padx=4)
        ttk.Button(btn_row, text="Save PGN As…", command=self._save).pack(side="left")
        ttk.Button(btn_row, text="Clear", command=self._clear).pack(side="left", padx=4)

        ttk.Label(self, text="PGN output:").pack(anchor="w")
        self.pgn = ScrolledText(self, wrap="word", height=20, font=("Consolas", 10))
        self.pgn.pack(fill="both", expand=True, pady=(2, 6))

        self.status = ttk.Label(self, text="Ready.", foreground="gray")
        self.status.pack(anchor="w")

    def _browse(self):
        path = filedialog.askopenfilename(title="Select file to encode")
        if path:
            self.path_var.set(path)

    def _encode(self):
        path = self.path_var.get().strip()
        if not path:
            messagebox.showwarning("No file", "Pick an input file first.")
            return
        if not os.path.isfile(path):
            messagebox.showerror("Not found", f"File does not exist:\n{path}")
            return

        self.encode_btn.config(state="disabled")
        self.status.config(text="Encoding…", foreground="gray")

        def worker():
            try:
                pgn_text = encode_file_to_pgn(path)
                self.after(0, lambda: self._on_done(pgn_text, None))
            except Exception as e:
                self.after(0, lambda: self._on_done(None, e))

        threading.Thread(target=worker, daemon=True).start()

    def _on_done(self, pgn_text, err):
        self.encode_btn.config(state="normal")
        if err is not None:
            self.status.config(text=f"Error: {err}", foreground="red")
            messagebox.showerror("Encode failed", str(err))
            return
        self.pgn.delete("1.0", "end")
        self.pgn.insert("1.0", pgn_text)
        games = pgn_text.count("[Event ") or 1
        self.status.config(
            text=f"Encoded {games} game(s), {len(pgn_text):,} chars.",
            foreground="green",
        )

    def _copy(self):
        text = self.pgn.get("1.0", "end-1c")
        if not text:
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        self.status.config(text="PGN copied to clipboard.", foreground="green")

    def _save(self):
        text = self.pgn.get("1.0", "end-1c")
        if not text:
            messagebox.showinfo("Nothing to save", "Encode a file first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pgn",
            filetypes=[("PGN", "*.pgn"), ("All files", "*.*")],
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        self.status.config(text=f"Saved → {path}", foreground="green")

    def _clear(self):
        self.pgn.delete("1.0", "end")
        self.status.config(text="Cleared.", foreground="gray")


class DecodeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)

        ttk.Label(self, text="PGN input (paste or load):").pack(anchor="w")

        btn_row = ttk.Frame(self)
        btn_row.pack(fill="x", pady=(2, 6))
        ttk.Button(btn_row, text="Paste", command=self._paste).pack(side="left")
        ttk.Button(btn_row, text="Load PGN file…", command=self._load).pack(
            side="left", padx=4
        )
        ttk.Button(btn_row, text="Clear", command=self._clear).pack(side="left")
        self.decode_btn = ttk.Button(
            btn_row, text="Decode → Save As…", command=self._decode
        )
        self.decode_btn.pack(side="right")

        self.pgn = ScrolledText(self, wrap="word", height=22, font=("Consolas", 10))
        self.pgn.pack(fill="both", expand=True)

        self.status = ttk.Label(self, text="Ready.", foreground="gray")
        self.status.pack(anchor="w", pady=(6, 0))

    def _paste(self):
        try:
            text = self.clipboard_get()
        except tk.TclError:
            self.status.config(text="Clipboard is empty.", foreground="red")
            return
        self.pgn.delete("1.0", "end")
        self.pgn.insert("1.0", text)
        self.status.config(text=f"Pasted {len(text):,} chars.", foreground="green")

    def _load(self):
        path = filedialog.askopenfilename(
            title="Load PGN", filetypes=[("PGN", "*.pgn"), ("All files", "*.*")]
        )
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        self.pgn.delete("1.0", "end")
        self.pgn.insert("1.0", text)
        self.status.config(text=f"Loaded {path}", foreground="green")

    def _clear(self):
        self.pgn.delete("1.0", "end")
        self.status.config(text="Cleared.", foreground="gray")

    def _decode(self):
        text = self.pgn.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("No PGN", "Paste or load a PGN first.")
            return
        out_path = filedialog.asksaveasfilename(
            title="Save decoded output as",
            filetypes=[("All files", "*.*")],
        )
        if not out_path:
            return

        self.decode_btn.config(state="disabled")
        self.status.config(text="Decoding…", foreground="gray")

        def worker():
            try:
                data = decode_pgn_to_bytes(text)
                with open(out_path, "wb") as f:
                    f.write(data)
                self.after(0, lambda: self._on_done(out_path, len(data), None))
            except Exception as e:
                self.after(0, lambda: self._on_done(None, 0, e))

        threading.Thread(target=worker, daemon=True).start()

    def _on_done(self, path, n_bytes, err):
        self.decode_btn.config(state="normal")
        if err is not None:
            self.status.config(text=f"Error: {err}", foreground="red")
            messagebox.showerror("Decode failed", str(err))
            return
        self.status.config(
            text=f"Decoded {n_bytes:,} bytes → {path}", foreground="green"
        )


def main():
    root = tk.Tk()
    root.title("Chess Encryption")
    root.geometry("820x600")

    nb = ttk.Notebook(root)
    nb.add(EncodeTab(nb), text="Encode")
    nb.add(DecodeTab(nb), text="Decode")
    nb.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
