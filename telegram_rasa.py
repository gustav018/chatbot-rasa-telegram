import os
import json
import requests
import logging
import signal
import subprocess
import time
from datetime import date
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
session_id = 0

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

ROOT_DIRPATH = os.path.realpath(os.path.dirname(__file__))
LOG_DIRPATH = os.path.join(ROOT_DIRPATH, "logs")
if not os.path.isdir(LOG_DIRPATH):
    os.makedirs(LOG_DIRPATH)

def start(update: Update, context: CallbackContext) -> None:
    """Handle `/start` command."""
    global session_id
    session_id += 1

    for handler in LOGGER.handlers[:]:
        LOGGER.removeHandler(handler)

    log_dirpath = os.path.join(LOG_DIRPATH, str(date.today()))
    print(log_dirpath)
    os.makedirs(log_dirpath, exist_ok=True)
    file_handler = logging.FileHandler(
        os.path.join(log_dirpath, f"session={str(session_id).zfill(3)}.txt"))
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", )
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)
    LOGGER.log(logging.INFO, f"Session ID: {session_id}")

def reply_text(update: Update, context: CallbackContext) -> None:
    """Reply to user's text messages."""

    query = update.message.text

    # forwards user input from Telegram to Rasa
    r = requests.post('http://localhost:5005/webhooks/rest/webhook',
                      json={"sender": session_id, "message": query})
    data = json.loads(r.text)[0]
    update.message.reply_text(data['text'], parse_mode="markdown")

    # update log with time information
    LOGGER.log(logging.INFO, f"User: {query}")
    LOGGER.log(logging.INFO, f"Bot: {data['text']}")

def signal_handler(sig, frame):
    print('Deteniendo el script...')
    updater.stop()
    sys.exit(0)

def start_rasa_server():
    """Starts the Rasa server and waits until it's fully ready."""
    os.chdir("rasa")  # Cambia a la ruta correcta de tu carpeta `rasa_chatbot`
    rasa_process = subprocess.Popen(
        ["rasa", "run", "-m", "models", "--enable-api", "--cors", "*", "--debug"]
    )
    
    # Espera hasta que el servidor esté activo
    server_active = False
    while not server_active:
        try:
            response = requests.get('http://localhost:5005/status')
            if response.status_code == 200:
                server_active = True
        except requests.exceptions.ConnectionError:
            time.sleep(2)  # Espera un poco antes de volver a intentar
    return rasa_process

def main() -> None:
    """Run the Telegram chatbot after the Rasa server is ready."""
    # Start Rasa server
    rasa_process = start_rasa_server()

    # Create the Updater with your chatbot API token
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # On command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # On message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_text))

    # Start the chatbot
    updater.start_polling()

    # Configurar el manejador de señales para Ctrl + C
    signal.signal(signal.SIGINT, signal_handler)

    print("El script ha comenzado. Presiona Ctrl + C para detenerlo.")
    updater.idle()

    # Termina el proceso de Rasa al detener el bot de Telegram
    rasa_process.terminate()

if __name__ == "__main__":
    main()
