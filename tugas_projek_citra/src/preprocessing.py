
import cv2


def baca_dan_proses_foto(lokasi_foto):
    """
    Membaca foto pisang, mengubah ukurannya,
    dan mengurangi noise menggunakan Gaussian Blur.
    """

    # Membaca foto dari lokasi file
    gambar = cv2.imread(lokasi_foto)

    # Memeriksa apakah foto berhasil dibaca
    if gambar is None:
        raise ValueError(
            f"Foto tidak ditemukan atau tidak bisa dibaca: {lokasi_foto}"
        )

    # Mengubah ukuran foto menjadi 256 x 256 piksel
    gambar_resize = cv2.resize(gambar, (256, 256))

    # Mengurangi noise pada foto
    gambar_blur = cv2.GaussianBlur(
        gambar_resize, (5, 5), 0
    )

    # Mengubah format BGR menjadi RGB
    gambar_rgb = cv2.cvtColor(
        gambar_blur, cv2.COLOR_BGR2RGB
    )

    # Mengembalikan hasil pemrosesan foto
    return gambar_rgb
