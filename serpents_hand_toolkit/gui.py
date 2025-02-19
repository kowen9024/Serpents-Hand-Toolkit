import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from bfs_crawler import minimal_bfs_scrape, save_bfs_results
from image_downloader import download_images
from ocr import perform_ocr_on_directory, perform_ocr_in_browser
import logging

class SerpentsHandToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Serpents Hand Toolkit v2.2")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")

        self.nav_frame = tk.Frame(self, bg="#e0e0e0", width=200)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.container = tk.Frame(self, bg="#ffffff")
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frames = {}
        for F in (CrawlerFrame, ImageDownloaderFrame, OCRFrame, BrowserOCRFrame, DebugFrame):
            page_name = F.__name__
            frame = F(self.container, self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        nav_items = [
            ("Crawler", "CrawlerFrame"),
            ("Image Downloader", "ImageDownloaderFrame"),
            ("OCR", "OCRFrame"),
            ("Browser OCR", "BrowserOCRFrame"),
            ("Debug", "DebugFrame"),
        ]
        row = 0
        for label, page_name in nav_items:
            b = tk.Button(self.nav_frame, text=label, command=lambda pn=page_name: self.show_frame(pn))
            b.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
            row += 1

        self.show_frame("CrawlerFrame")

    def show_frame(self, page_name):
        f = self.frames[page_name]
        f.tkraise()

class CrawlerFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        tk.Label(self, text="BFS Crawler (with search)", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        desc = "Enter base URL + search term => BFS => store discovered links in CSV."
        tk.Label(self, text=desc, wraplength=600, bg="#f0f0f0").pack(pady=5)

        row_base = tk.Frame(self, bg="#f0f0f0")
        row_base.pack(pady=5)
        tk.Label(row_base, text="Base URL:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.E)
        self.base_url_var = tk.StringVar(value="https://example.com")
        tk.Entry(row_base, textvariable=self.base_url_var, width=40).grid(row=0, column=1, padx=5)

        row_search = tk.Frame(self, bg="#f0f0f0")
        row_search.pack(pady=5)
        tk.Label(row_search, text="Search Term:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.E)
        self.search_var = tk.StringVar(value="laptops")
        tk.Entry(row_search, textvariable=self.search_var, width=30).grid(row=0, column=1, padx=5)

        row_pg = tk.Frame(self, bg="#f0f0f0")
        row_pg.pack(pady=5)
        tk.Label(row_pg, text="Max Pages:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.E)
        self.pages_var = tk.IntVar(value=2)
        tk.Entry(row_pg, textvariable=self.pages_var, width=5).grid(row=0, column=1, padx=5)

        self.progress_var = tk.IntVar(value=0)
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode="determinate",
                                        variable=self.progress_var)
        self.progress.pack(pady=5)

        self.cancel_flag = False
        rowbtn = tk.Frame(self, bg="#f0f0f0")
        rowbtn.pack(pady=10)
        tk.Button(rowbtn, text="Start BFS", command=self.start_bfs).grid(row=0, column=0, padx=5)
        tk.Button(rowbtn, text="Cancel BFS", command=self.cancel_bfs).grid(row=0, column=1, padx=5)

    def cancel_bfs(self):
        self.cancel_flag = True

    def start_bfs(self):
        self.cancel_flag = False
        def run():
            base_url = self.base_url_var.get().strip()
            search = self.search_var.get().strip()
            pages = self.pages_var.get()
            discovered = minimal_bfs_scrape(base_url, search, pages)
            self.progress_var.set(100)
            save_bfs_results(discovered)
            messagebox.showinfo("BFS Complete", f"Discovered {len(discovered)} pages.\nCSV => bfs_search_results.csv")
            self.progress_var.set(0)
        threading.Thread(target=run, daemon=True).start()

class ImageDownloaderFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        tk.Label(self, text="Image Downloader", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        desc = ("Select CSV with 'image_url' col.\nChoose output folder => concurrency => store images.\nProgress + cancel.")
        tk.Label(self, text=desc, wraplength=600, bg="#f0f0f0").pack(pady=5)

        row_csv = tk.Frame(self, bg="#f0f0f0")
        row_csv.pack(pady=5)
        tk.Label(row_csv, text="CSV File:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.E)
        self.csv_file_var = tk.StringVar(value="")
        tk.Entry(row_csv, textvariable=self.csv_file_var, width=40).grid(row=0, column=1, padx=5)
        tk.Button(row_csv, text="Browse", command=self.browse_csv).grid(row=0, column=2, padx=5)

        row_out = tk.Frame(self, bg="#f0f0f0")
        row_out.pack(pady=5)
        tk.Label(row_out, text="Output Folder:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.E)
        self.out_dir_var = tk.StringVar(value="")
        tk.Entry(row_out, textvariable=self.out_dir_var, width=40).grid(row=0, column=1, padx=5)
        tk.Button(row_out, text="Browse", command=self.browse_out_folder).grid(row=0, column=2, padx=5)

        self.progress_var = tk.IntVar(value=0)
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode="determinate",
                                        variable=self.progress_var)
        self.progress.pack(pady=5)
        self.cancel_flag = False

        rowbtn = tk.Frame(self, bg="#f0f0f0")
        rowbtn.pack(pady=10)
        tk.Button(rowbtn, text="Download Images", command=self.start_download).grid(row=0, column=0, padx=5)
        tk.Button(rowbtn, text="Cancel", command=self.cancel_download).grid(row=0, column=1, padx=5)

    def browse_csv(self):
        p = filedialog.askopenfilename(title="Select CSV with image_url", filetypes=[("CSV", "*.csv")])
        if p:
            self.csv_file_var.set(p)

    def browse_out_folder(self):
        d = filedialog.askdirectory(title="Select output folder for images")
        if d:
            self.out_dir_var.set(d)

    def cancel_download(self):
        self.cancel_flag = True

    def start_download(self):
        self.cancel_flag = False
        def run():
            csv_path = self.csv_file_var.get().strip()
            if not csv_path or not os.path.isfile(csv_path):
                messagebox.showerror("Error", "Invalid CSV file.")
                return
            out_dir = self.out_dir_var.get().strip()
            if not out_dir:
                messagebox.showerror("Error", "Please select output folder.")
                return

            image_urls = []
            try:
                with open(csv_path, "r", encoding="utf-8") as f):
                    r = csv.DictReader(f)
                    if "image_url" not in r.fieldnames:
                        messagebox.showerror("Error", "CSV must have 'image_url' column.")
                        return
                    for row in r:
                        image_urls.append(row["image_url"])
            except Exception as e:
                messagebox.showerror("CSV Error", str(e))
                return

            total = len(image_urls)
            if total == 0:
                messagebox.showinfo("No Images", "No 'image_url' found in CSV.")
                return

            completed, success = download_images(image_urls, out_dir, progress_callback=self.update_progress)
            messagebox.showinfo("Download Complete", 
                                f"Processed {completed} of {total} image URLs.\nSuccess => {success}\nImages => {out_dir}/images")
            self.progress_var.set(0)
        threading.Thread(target=run, daemon=True).start()

    def update_progress(self, completed, total):
        if total > 0:
            pct = int((completed / total) * 100)
            self.progress_var.set(pct)

class OCRFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        tk.Label(self, text="OCR for Seagate S/N", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        desc = "Pick images folder => parse S/N => store in CSV. Pattern [A-Z0-9]{8,12}, with morphological ops."
        tk.Label(self, text=desc, wraplength=600, bg="#f0f0f0").pack(pady=5)

        row = tk.Frame(self, bg="#f0f0f0")
        row.pack(pady=5)
        tk.Label(row, text="Image Folder:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.E)
        self.folder_var = tk.StringVar(value="")
        tk.Entry(row, textvariable=self.folder_var, width=40).grid(row=0, column=1, padx=5)
        tk.Button(row, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=5)

        row2 = tk.Frame(self, bg="#f0f0f0")
        row2.pack(pady=5)
        tk.Label(row2, text="Output CSV:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.E)
        self.csv_var = tk.StringVar(value="")
        tk.Entry(row2, textvariable=self.csv_var, width=30).grid(row=0, column=1, padx=5)
        tk.Label(row2, text=".csv", bg="#f0f0f0").grid(row=0, column=2, sticky=tk.W)

        self.progress_var = tk.IntVar(value=0)
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode="determinate",
                                        variable=self.progress_var)
        self.progress.pack(pady=5)

        self.cancel_flag = False
        rowbtn = tk.Frame(self, bg="#f0f0f0")
        rowbtn.pack(pady=10)
        tk.Button(rowbtn, text="Run OCR", command=self.start_ocr).grid(row=0, column=0, padx=5)
        tk.Button(rowbtn, text="Cancel", command=self.cancel_ocr).grid(row=0, column=1, padx=5)

    def browse_folder(self):
        d = filedialog.askdirectory(title="Select folder with images")
        if d:
            self.folder_var.set(d)

    def cancel_ocr(self):
        self.cancel_flag = True

    def start_ocr(self):
        self.cancel_flag = False
        def run():
            folder =