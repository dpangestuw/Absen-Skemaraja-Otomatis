# Absen Skemaraja Otomatis

Otomatisasi pengisian kehadiran untuk Skemaraja menggunakan Selenium dan Python. Script ini dapat mengirimkan pemberitahuan ke Telegram setelah pengisian berhasil dilakukan.

## Fitur

- Otomatis mengisi form kehadiran di Skemaraja.
- Mengatur geolokasi custom pada browser.
- Mengirim notifikasi ke Telegram setelah pengisian berhasil.
- Penanganan percobaan ulang jika terjadi kegagalan.

## Persyaratan

- Python 3.6 atau lebih baru
- Paket Python yang dibutuhkan:
  - selenium
  - requests
  - python-dotenv
  - webdriver-manager
- Browser Google Chrome

## Instalasi

1. Clone repositori ini:

    ```bash
    git clone https://github.com/username/skemaraja-attendance-automation.git
    cd skemaraja-attendance-automation
    ```

2. Instal dependensi:

    ```bash
    pip install -r requirements.txt
    ```

3. Buat file `config.csv` di direktori proyek dengan format berikut:

    ```csv
    NIP,password,name,telegram_chat_id,start_time
    12345678,password123,John Doe,123456789,08:00
    ```

## Penggunaan

1. Jalankan script dengan perintah berikut:

    ```bash
    python main.py
    ```

2. Script akan memulai proses pengisian form kehadiran dan mengirimkan notifikasi ke Telegram setelah berhasil.

## Konfigurasi

Script ini dapat dikonfigurasi melalui file `config.csv`:

- **NIP**: Nomor Induk Pegawai.
- **password**: Kata sandi untuk login.
- **name**: Nama pengguna.
- **telegram_chat_id**: ID chat Telegram untuk menerima notifikasi.
- **start_time**: Waktu mulai untuk menjalankan script (format 24 jam, misal `08:00`).

## Troubleshooting

- Pastikan versi Chrome dan ChromeDriver kompatibel.
- Pastikan ID chat Telegram sudah benar.
- Periksa kembali format `config.csv`.

