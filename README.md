# Absen Skemaraja Otomatis

Otomatisasi pengisian kehadiran untuk Skemaraja menggunakan Selenium dan Python. Script ini dapat mengirimkan pemberitahuan ke Telegram setelah pengisian berhasil dilakukan.

## Fitur

- Otomatis mengisi Absen di Skemaraja pada hari kerja.
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
    git clone https://github.com/dpangestuw/Absen-Skemaraja.git
    cd Absen-Skemeraja
    ```

2. Instal dependensi:

    ```bash
    pip install -r requirements.txt
    ```

3. Buat file `config.csv` di direktori proyek dengan format berikut:

    ```csv
    NIP,password,name,telegram_chat_id,pagi,siang,sore
    12345678,password123,John Doe,123456789,07:00,12:00,16:30
    ```

## Penggunaan

1. Jalankan script dengan perintah berikut:

    ```bash
    python pagi.py
    ```
    ```bash
    python seninpagi.py
    ```
    ```bash
    python siang.py
    ```
    ```bash
    python sore.py
    ```

2. Script akan memulai proses pengisian form kehadiran dan mengirimkan notifikasi ke Telegram setelah berhasil.

## Cara Mendapatkan Telegram Chat ID

### Menggunakan Bot @userinfobot

1. Buka Telegram dan cari bot `@userinfobot`.
2. Kirim pesan `/start` ke bot `@userinfobot`.
3. Bot ini akan membalas dengan informasi yang berisi `chat_id`. Gunakan `chat_id` ini untuk mengirim pesan ke akun Anda sendiri.

## Konfigurasi

Script ini dapat dikonfigurasi melalui file `config.csv`:

- **NIP**: Nomor Induk Pegawai.
- **password**: Kata sandi untuk login.
- **name**: Nama pengguna.
- **telegram_chat_id**: ID chat Telegram untuk menerima notifikasi.
- **start_time**: Waktu mulai untuk menjalankan script (format 24 jam, misal `07:00`).

## Troubleshooting

- Pastikan versi Chrome dan ChromeDriver kompatibel.
- Pastikan Path ChromeDriver pada C:\chromedriver.exe
- Periksa kembali format `config.csv`.

