
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from src.deteksi_buah import deteksi_buah


class AplikasiDeteksiBuah:
    def __init__(self, root):
        self.root = root
        self.root.title("FruitVision - Deteksi Buah")
        self.root.geometry("1000x700")
        self.root.configure(bg="#F3F6F4")

        self.lokasi_foto = None
        self.foto_tampil = None

        # Judul aplikasi
        tk.Label(
            root,
            text="FRUITVISION",
            font=("Segoe UI", 23, "bold"),
            bg="#F3F6F4",
            fg="#176B45"
        ).pack(pady=(18, 3))

        tk.Label(
            root,
            text="Sistem Deteksi Buah Berbasis Citra Digital",
            font=("Segoe UI", 11),
            bg="#F3F6F4",
            fg="#52645A"
        ).pack(pady=(0, 15))

        # Tombol pilih foto
        tk.Button(
            root,
            text="Pilih Foto Buah",
            command=self.pilih_foto,
            font=("Segoe UI", 11, "bold"),
            bg="#176B45",
            fg="white",
            activebackground="#238657",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(pady=5)

        # Tombol deteksi
        tk.Button(
            root,
            text="Deteksi Buah",
            command=self.proses_deteksi,
            font=("Segoe UI", 11, "bold"),
            bg="#E5A93D",
            fg="#222222",
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(pady=5)

        # Area gambar
        self.label_gambar = tk.Label(
            root,
            text="Belum ada foto dipilih",
            font=("Segoe UI", 12),
            bg="white",
            fg="#66756B",
            width=75,
            height=20
        )
        self.label_gambar.pack(
            padx=20, pady=15, fill="both", expand=True
        )

        # Area informasi hasil
        self.label_hasil = tk.Label(
            root,
            text="Silakan pilih foto buah dari laptop.",
            font=("Segoe UI", 11),
            bg="#F3F6F4",
            fg="#263D30",
            justify="left",
            wraplength=900
        )
        self.label_hasil.pack(pady=(0, 18))

    def pilih_foto(self):
        lokasi = filedialog.askopenfilename(
            title="Pilih Foto Buah",
            filetypes=[
                ("File gambar", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("Semua file", "*.*")
            ]
        )

        if not lokasi:
            return

        # Simpan lokasi foto yang dipilih
        self.lokasi_foto = lokasi
        self.label_hasil.config(
            text="Foto dipilih. Klik Deteksi Buah untuk menganalisis."
        )

        # Tampilkan foto sebelum deteksi
        try:
            foto = Image.open(lokasi)
            foto.thumbnail((850, 400))

            self.foto_tampil = ImageTk.PhotoImage(foto)
            self.label_gambar.config(
                image=self.foto_tampil,
                text=""
            )
        except Exception as error:
            messagebox.showerror(
                "Kesalahan Foto",
                f"Foto tidak dapat dibuka:\n{error}"
            )

    def proses_deteksi(self):
        if not self.lokasi_foto:
            messagebox.showwarning(
                "Foto Belum Dipilih",
                "Silakan pilih foto terlebih dahulu."
            )
            return

        try:
            gambar, daftar_buah = deteksi_buah(
                self.lokasi_foto
            )

            jumlah = len(daftar_buah)
            informasi = [
                f"Total buah terdeteksi: {jumlah}"
            ]

            if jumlah == 0:
                informasi.append(
                    "Buah tidak ditemukan pada gambar."
                )
            else:
                jumlah_jenis = {}

                for nomor, buah in enumerate(
                    daftar_buah, start=1
                ):
                    nama = buah["nama"]
                    jumlah_jenis[nama] = (
                        jumlah_jenis.get(nama, 0) + 1
                    )

                    informasi.append(
                        f"{nomor}. {nama} | "
                        f"Keyakinan deteksi: "
                        f"{buah['keyakinan_deteksi']:.1%}"
                    )

                informasi.append("")
                informasi.append("Ringkasan jenis buah:")

                for nama, total in jumlah_jenis.items():
                    informasi.append(
                        f"- {nama}: {total} buah"
                    )

            # Konversi gambar untuk ditampilkan di Tkinter
            gambar_rgb = cv2.cvtColor(
                gambar, cv2.COLOR_BGR2RGB
            )

            foto_hasil = Image.fromarray(gambar_rgb)
            foto_hasil.thumbnail((850, 400))

            self.foto_tampil = ImageTk.PhotoImage(
                foto_hasil
            )

            self.label_gambar.config(
                image=self.foto_tampil,
                text=""
            )

            self.label_hasil.config(
                text="\n".join(informasi)
            )

        except Exception as error:
            messagebox.showerror(
                "Deteksi Gagal",
                str(error)
            )


if __name__ == "__main__":
    root = tk.Tk()
    aplikasi = AplikasiDeteksiBuah(root)
    root.mainloop()
