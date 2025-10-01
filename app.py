from flask import Flask, request
import logging

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi logging untuk melihat proses di terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Di dunia nyata, ini akan menggunakan database (seperti Redis atau MySQL)
# untuk menyimpan state sesi pengguna. Untuk demo, kita gunakan dictionary Python.
user_sessions = {}

def get_session(session_id):
    """Mengambil atau membuat sesi baru untuk pengguna."""
    if session_id not in user_sessions:
        user_sessions[session_id] = {'step': 'start'}
    return user_sessions[session_id]

def process_transfer(source_msisdn, dest_msisdn, amount):
    """
    Fungsi placeholder untuk memproses transfer pulsa.
    Di aplikasi nyata, fungsi ini akan memanggil API sistem billing operator
    untuk mengurangi pulsa pengirim dan menambahkan ke penerima.
    """
    logging.info(f"PROSES TRANSFER: Dari {source_msisdn} ke {dest_msisdn} sejumlah {amount}")
    # Simulasi selalu berhasil untuk demo ini
    return True

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    """Endpoint utama yang akan dihubungi oleh USSD Gateway."""
    # Ambil data yang dikirim oleh USSD Gateway
    session_id = request.values.get("sessionId", None)
    phone_number = request.values.get("phoneNumber", None) # Nomor pengguna
    text_input = request.values.get("text", "").strip()   # Input dari pengguna

    logging.info(f"Request Diterima: sessionId={session_id}, phoneNumber={phone_number}, text='{text_input}'")

    # Ambil sesi pengguna saat ini
    session = get_session(session_id)
    step = session.get('step', 'start')
    response = ""

    # Logika alur menu USSD
    if step == 'start':
        # Tampilan Awal: Meminta nomor tujuan
        response = "CON Selamat datang di layanan transfer pulsa *858#.\n"
        response += "Masukkan nomor tujuan:"
        session['step'] = 'get_amount' # Pindah ke langkah selanjutnya
    
    elif step == 'get_amount':
        # Pengguna telah memasukkan nomor tujuan
        destination_number = text_input
        if not destination_number.isdigit() or len(destination_number) < 10:
            response = "END Nomor tujuan tidak valid. Silakan coba lagi."
        else:
            session['destination_number'] = destination_number
            response = f"CON Masukkan nominal pulsa yang akan ditransfer ke {destination_number}:"
            session['step'] = 'get_confirmation' # Pindah ke langkah konfirmasi

    elif step == 'get_confirmation':
        # Pengguna telah memasukkan nominal
        amount = text_input
        if not amount.isdigit() or int(amount) <= 0:
            response = "END Nominal transfer tidak valid. Silakan coba lagi."
        else:
            session['amount'] = amount
            destination_number = session.get('destination_number')
            response = f"CON Anda akan transfer pulsa {amount} ke {destination_number}.\n"
            response += "Biaya Rp2000 akan dikenakan.\n"
            response += "1. Lanjut\n"
            response += "2. Batal"
            session['step'] = 'process_final'

    elif step == 'process_final':
        # Pengguna memilih konfirmasi atau batal
        confirmation = text_input
        if confirmation == '1':
            # Panggil fungsi untuk memproses transfer
            success = process_transfer(
                source_msisdn=phone_number,
                dest_msisdn=session.get('destination_number'),
                amount=session.get('amount')
            )
            if success:
                response = "END Terima kasih. Permintaan transfer pulsa Anda sedang diproses. Anda akan menerima notifikasi SMS."
            else:
                response = "END Maaf, transaksi gagal. Saldo Anda tidak mencukupi atau terjadi gangguan."
        elif confirmation == '2':
            response = "END Transaksi dibatalkan."
        else:
            destination_number = session.get('destination_number')
            amount = session.get('amount')
            response = f"CON Input tidak valid. Anda akan transfer pulsa {amount} ke {destination_number}.\n"
            response += "1. Lanjut\n"
            response += "2. Batal"
            
    else:
        response = "END Terjadi kesalahan pada sistem. Mohon coba lagi."

    # Hapus sesi jika percakapan berakhir (ditandai dengan "END")
    if response.startswith("END"):
        if session_id in user_sessions:
            del user_sessions[session_id]
            logging.info(f"Sesi {session_id} dihapus.")

    # Kirim response kembali ke USSD Gateway
    return response

if __name__ == '__main__':
    # Menjalankan server Flask di port 5000 untuk pengujian
    app.run(host='0.0.0.0', port=5000, debug=True)