import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime
import asyncio

# Token bot Telegram Anda
TOKEN = '6990860556:AAEfcVgJ-nZ_abVoXogawxMXxG-9hxiBRcg'

# Definisikan hadiah
hadiah = ["BONUS 10K", "BONUS 20K", "BONUS 30K", "BONUS 40K", "BONUS 50K",
          "BONUS 100K", "ZONK", "ZONK", "ZONK", "ZONK", "ZONK", "ZONK"]

# Pemetaan hadiah ke URL GIF
hadiah_to_gif = {
    "BONUS 10K": "https://hostcoin303.com/gif/10kgif.gif",
    "BONUS 20K": "https://hostcoin303.com/gif/20kgif.gif",
    "BONUS 30K": "https://hostcoin303.com/gif/30kgif.gif",
    "BONUS 40K": "https://hostcoin303.com/gif/40kgif.gif",
    "BONUS 50K": "https://hostcoin303.com/gif/50kgif.gif",
    "BONUS 100K": "https://hostcoin303.com/gif/100kgif.gif",
    "ZONK": "https://hostcoin303.com/gif/zonk.gif",
    "ZONK": "https://hostcoin303.com/gif/zonk.gif",
    "ZONK": "https://hostcoin303.com/gif/zonk.gif",
    "ZONK": "https://hostcoin303.com/gif/zonk.gif",
    "ZONK": "https://hostcoin303.com/gif/zonk.gif",
    "ZONK": "https://hostcoin303.com/gif/zonk.gif"
}


# Fungsi untuk mengundi hadiah
def undi_hadiah(hadiah):
    return random.choice(hadiah)


# Fungsi untuk menangani perintah /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Halo! Ketik /undi untuk memutar roda undian dan mendapatkan hadiah!')


# Fungsi untuk menangani perintah /undi
async def undi(update: Update, context: CallbackContext) -> None:
    # Lakukan pengundian
    hadiah_terpilih = undi_hadiah(hadiah)

    # Kirim GIF berdasarkan hadiah yang didapat
    gif_url = hadiah_to_gif.get(hadiah_terpilih)
    if gif_url:
        await update.message.reply_animation(animation=gif_url)

    # Tunggu selama 10 detik
    await asyncio.sleep(10)

    # Kirim hasil pengundian
    await update.message.reply_text(f"Hadiah yang terpilih adalah: {hadiah_terpilih}")

    # Simpan hasil ke Google Sheets
    simpan_hasil_ke_sheets(update.message.from_user.username, hadiah_terpilih)


def simpan_hasil_ke_sheets(username, hadiah):
    try:
        # Hubungkan ke Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/jsi61/PycharmProjects/undian/.venv/Scripts/credentials.json", scope)
        client = gspread.authorize(creds)

        print("Terhubung ke Google Sheets")

        # Buka spreadsheet dan pilih worksheet
        sheet = client.open("bonus spin").sheet1

        print("Spreadsheet terbuka")

        # Dapatkan tanggal dan waktu sekarang
        sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Dapatkan baris baru untuk menambahkan data
        row = [username, hadiah, sekarang]
        sheet.append_row(row)

        print("Data berhasil ditambahkan ke spreadsheet")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def main():
    # Buat application
    application = Application.builder().token(TOKEN).build()

    # Daftarkan handler untuk perintah /start dan /undi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("undi", undi))

    # Mulai bot
    application.run_polling()


if __name__ == '__main__':
    main()
