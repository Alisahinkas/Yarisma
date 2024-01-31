import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import time
import fitz

class ChronometerApp:
    def __init__(self, master):
        self.running = False

        self.master = master

        self.master.title("QuizShow")
        self.master.configure(bg='#2E2E2E')
        self.master.geometry("1000x600")

        # Görseli yükle
        image = Image.open("alis.png")
        image = image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(image)

        # Görsel
        self.image_label = tk.Label(master, image=self.photo, bg='#2E2E2E')
        self.image_label.place(x=40, y=40)

        self.amal_label = tk.Label(master, text="AMAL Yazılım Geliştirme Ekibi", font=("Arial", 12),
                                   bg='#2E2E2E', fg='#30D5C8')
        self.amal_label.place(x=20, y=200)  # Konum

        self.amal_label = tk.Label(master, text="QUIZ SHOW", font=("Impact", 25), bg='#2E2E2E', fg='white')
        self.amal_label.place(x=20, y=250)

        # Timer girişi
        self.entry_time = tk.Entry(master, bg='#2E2E2E', fg='white')
        self.entry_time.place(x=20, y=320)

        # Geri sayım
        self.countdown_frame = tk.Frame(master, bg='#404040')
        self.countdown_frame.place(x=20, y=360)
        self.countdown_var = tk.StringVar()
        self.countdown_label = tk.Label(self.countdown_frame, textvariable=self.countdown_var, font=("Arial", 24),
                                        bg='#2E2E2E', fg='white')
        self.countdown_label.pack()

        # Başlat
        self.start_button = tk.Button(master, text="Kronometreyi Başlat", command=self.start_chronometer,
                                      bg='#404040', fg='white', height=3, width=30)
        self.start_button.place(x=20, y=420)

        # Sıfırla
        self.reset_button = tk.Button(master, text="Sıfırla", command=self.reset_chronometer, bg='red', fg='white',
                                      height=3, width=15)
        self.reset_button.place(x=260, y=420)
        self.reset_button.config(state=tk.DISABLED)

        self.label_time = tk.Label(master, text="Süre girin:", font=("Arial", 14), bg='#2E2E2E', fg='white')
        self.label_time.place(x=20, y=290)


        # Puan Değişim Miktarı etiketi
        self.label_point_change = tk.Label(master, text="Puan Değişim Miktarı:", bg='#2E2E2E', fg='white')
        self.label_point_change.place(x=1580, y=80)  # Sağa kaydır, sağdan 20 piksel boşluk

        # Puan Değişim Miktarı girişi
        self.entry_point_change = tk.Entry(master, bg='#2E2E2E', fg='white')
        self.entry_point_change.place(x=1580, y=110)  # Sağa kaydır, sağdan 20 piksel boşluk

        self.team_scores = [0, 0, 0, 0, 0]

        self.team_labels = []
        self.team_buttons_plus = []
        self.team_buttons_minus = []

        for i in range(5):
            frame = tk.Frame(master, bg='#2E2E2E')
            frame.place(x=1500, y=150 + i * 100)

            label = tk.Label(frame, text=f"Takım {i + 1}", bg='#2E2E2E', fg='white')
            label.pack(side=tk.LEFT)

            button_minus = tk.Button(frame, text="-", command=lambda idx=i: self.update_score(idx, -self.get_point_change()),
                                     bg='#404040', fg='white', height=4, width=10)
            button_minus.pack(side=tk.LEFT)

            score_label = tk.Label(frame, text=str(self.team_scores[i]), bg='#2E2E2E', fg='white')
            score_label.pack(side=tk.LEFT)

            button_plus = tk.Button(frame, text="+", command=lambda idx=i: self.update_score(idx, self.get_point_change()),
                                    bg='#404040', fg='white', height=4, width=10)
            button_plus.pack(side=tk.LEFT)

            self.team_labels.append(score_label)
            self.team_buttons_plus.append(button_plus)
            self.team_buttons_minus.append(button_minus)

        # PDF Görüntüleyici
        self.pdf_viewer_frame = tk.Frame(master, bg='#2E2E2E')
        self.pdf_viewer_frame.place(x=500, y=200)

        self.pdf_viewer = tk.Canvas(self.pdf_viewer_frame, bg='white', width=800, height=550)
        self.pdf_viewer.pack()

        self.load_pdf_button = tk.Button(master, text="PDF Yükle", command=self.load_pdf, bg='#404040', fg='white',
                                         height=2, width=15)
        self.load_pdf_button.place(x=500, y=760)

        self.pdf_path = None  # PDF dosyasının adını saklamak için üye eklendi
        self.current_page = 0  # Şu anki sayfanın indeksi

        self.next_page_button = tk.Button(master, text="Sonraki Sayfa", command=self.show_next_page,
                                          bg='#404040', fg='white', height=2, width=15)
        self.next_page_button.place(x=630, y=760)

        self.master.attributes("-fullscreen", True)  # Tam ekran modu

    def load_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.show_pdf()

    def show_pdf(self):
        pdf_doc = fitz.open(self.pdf_path)
        total_pages = pdf_doc.page_count

        while self.current_page < total_pages:
            page = pdf_doc[self.current_page]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            tk_img = ImageTk.PhotoImage(img)
            self.pdf_viewer.create_image(0, 0, anchor="nw", image=tk_img)
            self.master.update()

            time.sleep()  # Her sayfayı yarım saniye göster




            self.pdf_viewer.delete("all")
            self.current_page += 1

    def show_next_page(self):
        if self.pdf_path:
            pdf_doc = fitz.open(self.pdf_path)
            total_pages = pdf_doc.page_count

            if self.current_page < total_pages - 1:
                self.current_page += 1
                self.show_pdf()

    def start_chronometer(self):
        if not self.running:
            try:
                target_time = float(self.entry_time.get())
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli bir süre girin.")
                return

            self.label_time.config(text="Kronometre çalışıyor...")
            self.start_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)

            start_time = time.time()
            self.running = True

            while self.running:
                elapsed_time = time.time() - start_time
                remaining_time = max(0, target_time - elapsed_time)

                if remaining_time == 0:
                    messagebox.showinfo("Süre doldu", "Süre doldu.")
                    self.running = False
                    break

                self.countdown_var.set(f"Kalan süre: {remaining_time:.2f} saniye")
                self.master.update()

                time.sleep(0.01)

            self.label_time.config(text="Süre girin:")
            self.start_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.DISABLED)
            self.countdown_var.set("")

    def reset_chronometer(self):
        self.entry_time.delete(0, tk.END)
        self.label_time.config(text="Süre girin:")
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.running = False
        self.countdown_var.set("")


if __name__ == "__main__":
    root = tk.Tk(screenName=None, baseName=None, className="QuizShow", useTk=1)
    app = ChronometerApp(root)
    root.mainloop()