# Simulasi Layanan USSD Transfer Pulsa (*858#)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.x-black.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Proyek ini adalah sebuah aplikasi web sederhana yang dibangun menggunakan Python dan Flask untuk mensimulasikan alur kerja layanan USSD transfer pulsa, seperti layanan `*858#` yang populer di Indonesia. Aplikasi ini dirancang untuk dapat diintegrasikan dengan USSD Gateway milik operator telekomunikasi.

## Fitur

- **Sesi Berbasis Menu**: Mengelola percakapan multi-langkah dengan pengguna.
- **Logika Transfer Pulsa**: Mensimulasikan alur dari memasukkan nomor tujuan, nominal, hingga konfirmasi.
- **Manajemen Sesi**: Menggunakan dictionary sederhana untuk melacak state setiap sesi pengguna (di produksi, bisa diganti dengan Redis).
- **Endpoint Tunggal**: Semua logika diproses melalui satu endpoint `/ussd` sesuai standar USSD Gateway.
- **Konfigurasi `CON` dan `END`**: Memberikan respon yang sesuai untuk melanjutkan atau mengakhiri sesi USSD.

## Arsitektur & Cara Kerja

Aplikasi ini berjalan sebagai server HTTP yang menunggu permintaan `POST` dari USSD Gateway.

1.  Ketika pengguna menekan kode USSD, Gateway mengirimkan request pertama ke endpoint `/ussd`.
2.  Aplikasi membuat sesi baru untuk pengguna dan mengirimkan balasan menu pertama dengan prefix `CON` (Continue).
3.  Setiap kali pengguna memasukkan input, Gateway mengirimkan request baru dengan input tersebut.
4.  Aplikasi menggunakan `sessionId` untuk mengambil state terakhir pengguna, memproses input, dan mengirimkan balasan berikutnya (`CON` atau `END`).
5.  Jika balasan diawali dengan `END` (End), Gateway akan menampilkan pesan terakhir dan menutup sesi.

## Prasyarat

- Python 3.8 atau lebih baru
- `pip` (package installer for Python)

## Instalasi & Menjalankan

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/USERNAME/ussd-credit-transfer-simulator.git](https://github.com/USERNAME/ussd-credit-transfer-simulator.git)
    cd ussd-credit-transfer-simulator
    ```
    *(Jangan lupa ganti `USERNAME` dengan username GitHub Anda)*

2.  **Buat dan aktifkan virtual environment (sangat disarankan):**
    ```bash
    # Untuk MacOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Untuk Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependensi yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi:**
    ```bash
    python app.py
    ```
    Server akan berjalan di `http://127.0.0.1:5000`.

## Cara Menguji

Anda bisa mensimulasikan permintaan dari USSD Gateway menggunakan `curl` dari terminal.

**1. Memulai Sesi**
```bash
curl -X POST "http://localhost:5000/ussd" \
-d "sessionId=SesiUnik001" \
-d "phoneNumber=+6281234567890" \
-d "text="
```
_Respon yang diharapkan: `CON Selamat datang di layanan transfer pulsa *858#.\nMasukkan nomor tujuan:`_

**2. Memasukkan Nomor Tujuan**
```bash
curl -X POST "http://localhost:5000/ussd" \
-d "sessionId=SesiUnik001" \
-d "phoneNumber=+6281234567890" \
-d "text=081987654321"
```
_Respon yang diharapkan: `CON Masukkan nominal pulsa yang akan ditransfer ke 081987654321:`_

**3. Memasukkan Nominal**
```bash
curl -X POST "http://localhost:5000/ussd" \
-d "sessionId=SesiUnik001" \
-d "phoneNumber=+6281234567890" \
-d "text=10000"
```
_Respon yang diharapkan: `CON Anda akan transfer pulsa 10000 ke 081987654321.\nBiaya Rp2000 akan dikenakan.\n1. Lanjut\n2. Batal`_

**4. Memberikan Konfirmasi (input '1')**
```bash
curl -X POST "http://localhost:5000/ussd" \
-d "sessionId=SesiUnik001" \
-d "phoneNumber=+6281234567890" \
-d "text=1"
```
_Respon yang diharapkan: `END Terima kasih. Permintaan transfer pulsa Anda sedang diproses. Anda akan menerima notifikasi SMS.`_

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.