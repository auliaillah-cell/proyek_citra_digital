
from ultralytics import YOLO
import cv2


# Memuat model YOLO
model = YOLO("yolo26n.pt")

# Kelas buah yang didukung model
KELAS_BUAH = {
    "apple": "Apel",
    "banana": "Pisang",
    "orange": "Jeruk"
}


def deteksi_buah(lokasi_foto):
    """
    Mendeteksi buah pada foto dan menampilkan
    kotak serta label yang lebih mudah dibaca.
    """

    # Memastikan foto bisa dibaca
    gambar = cv2.imread(lokasi_foto)

    if gambar is None:
        raise ValueError("Foto tidak ditemukan atau tidak bisa dibaca.")

    # Memilih ID kelas buah yang tersedia pada model
    kelas_model = model.names

    id_buah = [
        nomor
        for nomor, nama in kelas_model.items()
        if nama in KELAS_BUAH
    ]

    # Deteksi hanya kelas buah yang didukung
    hasil = model.predict(
        source=gambar,
        classes=id_buah,
        conf=0.35,
        iou=0.50,
        max_det=30,
        verbose=False
    )

    daftar_buah = []

    for prediksi in hasil:
        for kotak in prediksi.boxes:
            nomor_kelas = int(kotak.cls[0])
            nama_inggris = model.names[nomor_kelas]

            if nama_inggris not in KELAS_BUAH:
                continue

            koordinat = (
                kotak.xyxy[0]
                .cpu()
                .numpy()
                .astype(int)
            )

            keyakinan = float(kotak.conf[0])

            daftar_buah.append({
                "nama": KELAS_BUAH[nama_inggris],
                "koordinat": koordinat.tolist(),
                "keyakinan_deteksi": keyakinan
            })

    # Menggambar kotak dan label yang lebih rapi
    for nomor, buah in enumerate(daftar_buah, start=1):
        x1, y1, x2, y2 = buah["koordinat"]

        # Kotak hijau yang lebih tipis
        cv2.rectangle(
            gambar,
            (x1, y1),
            (x2, y2),
            (0, 200, 0),
            2
        )

        # Label singkat dengan ukuran lebih kecil
        label = (
            f"{nomor}. {buah['nama']} "
            f"{buah['keyakinan_deteksi']:.0%}"
        )

        ukuran_teks, baseline = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            1
        )

        lebar_teks, tinggi_teks = ukuran_teks

        # Label diletakkan di atas kotak jika memungkinkan
        label_y = max(y1, tinggi_teks + 10)

        # Latar belakang hijau agar tulisan jelas
        cv2.rectangle(
            gambar,
            (x1, label_y - tinggi_teks - 8),
            (x1 + lebar_teks + 8, label_y + baseline - 4),
            (0, 160, 0),
            -1
        )

        # Tulisan putih agar kontras
        cv2.putText(
            gambar,
            label,
            (x1 + 4, label_y - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    return gambar, daftar_buah
