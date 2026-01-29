import socket
import logging

# =========================
# Logging Configuration
# =========================
logging.basicConfig(
    filename="receiver.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("=== Receiver started ===")

# =========================
# Configuration
# =========================
HOST = "0.0.0.0"
PORT = 9001
CHUNK_SIZE = 4096
OUTPUT_FILE = "received_pdfs.zip"

# =========================
# Step 1: Start Server
# =========================
s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)

logging.info(f"Listening on {HOST}:{PORT}")

# =========================
# Step 2: Accept Connection
# =========================
conn, addr = s.accept()
logging.info(f"Connection received from {addr}")

# =========================
# Step 3: Receive File
# =========================
received_bytes = 0

with open(OUTPUT_FILE, "wb") as f:
    while True:
        data = conn.recv(CHUNK_SIZE)
        if not data:
            break
        f.write(data)
        received_bytes += len(data)

logging.info(f"File received successfully ({received_bytes} bytes)")

# =========================
# Cleanup
# =========================
conn.close()
s.close()

logging.info("Connection closed")
logging.info("=== Receiver finished ===")
