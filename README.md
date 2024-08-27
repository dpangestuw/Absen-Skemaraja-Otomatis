# Absen Skemaraja Otomatis

Absensi Skemaraja secara otomatis menggunakan Selenium dan Python. Script ini dapat mengirimkan pemberitahuan ke Telegram setelah pengisian berhasil dilakukan.

## Fitur

- Otomatis mengisi Absen di Skemaraja pada hari kerja.
- Mengatur geolokasi custom pada browser.
- Mengirim notifikasi ke Telegram setelah pengisian berhasil.

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
    git clone https://github.com/dpangestuw/Absen-Skemaraja-Otomatis.git
    cd Absen-Skemaraja-Otomatis
    ```

2. Instal dependensi:

    ```bash
    pip install -r requirements.txt
    ```

3. Buat file `config.csv` di direktori proyek dengan format berikut:

    ```csv
    NIP,password,name
    12345678,password123,John
    ```

## Penggunaan

1. Jalankan script dengan perintah berikut:

    ```bash
    python absen.py
    ```

2. Script akan memulai proses pengisian form kehadiran dan mengirimkan notifikasi ke Telegram setelah berhasil.


## Konfigurasi

Script ini dapat dikonfigurasi melalui file `config.csv`:

- **NIP**: Nomor Induk Pegawai.
- **password**: Kata sandi untuk login.
- **name**: Nama pengguna, untuk sebutan pada saat mengirim notifikasi

## Troubleshooting

- Pastikan versi Chrome dan ChromeDriver kompatibel.
- Pastikan Path ChromeDriver pada C:\chromedriver.exe
- Periksa kembali format `config.csv`.

