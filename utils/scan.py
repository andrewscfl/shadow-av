import os
import csv
import hashlib
import threading
from tkinter import messagebox
import time

class Scan:
    def __init__(self, text_box):
        #md5 hashes of malware files
        self.malware_definitions, self.malware_md5_hashes = self.load_malware_definitions()
        self.text_box = text_box

    def scan_files(self):
        malware_found = []
        files_scanned = 0
        start_time = time.time()
        for root, dirs, files in os.walk("/"):
            for file in files:
                files_scanned += 1
                file_path = os.path.join(root, file)
                md5_hash = self.hash_file(file_path)
                if md5_hash is None:
                    print("Error hashing file: " + file_path)
                    continue

                if md5_hash in self.malware_md5_hashes:
                    malware_found.append(file_path)

                else:
                    self.text_box.config(state="normal")
                    self.text_box.insert("end", "\n> File verified safe: " + file_path)
                    self.text_box.config(state="disabled")

                self.text_box.see("end")
        
        end_time = time.time()
        scan_time = end_time - start_time
        
        self.text_box.config(state="normal")
        self.text_box.insert("end", f"\n> Scan complete: {scan_time:.2f} seconds")
        self.text_box.insert("end", f"\n> Files scanned: {files_scanned}")

        if len(malware_found) > 0:
            self.text_box.config(state="normal")
            self.text_box.insert("end", "\n> Malware found: " + str(len(malware_found)) + " files")
            for file in malware_found:
                self.text_box.insert("end", "\n> " + file)
            self.text_box.config(state="disabled")

            should_remove_malware = messagebox.askyesno("Warning", "Malware found: \n" + "\n".join(malware_found) + " \nDo you want to delete them?")
            if should_remove_malware:
                for file in malware_found:
                    os.remove(file)
                    self.text_box.config(state="normal")
                    self.text_box.insert("end", "\n> Malware removed: " + file)
                    self.text_box.config(state="disabled")
            else:
                self.text_box.config(state="normal")
                self.text_box.insert("end", "\n> Malware found but not removed")
                self.text_box.config(state="disabled")

        else:
            self.text_box.config(state="normal")
            self.text_box.insert("end", "\n> No malware found")
            self.text_box.config(state="disabled")


    def hash_file(self, file_path):
        # get md5 hash of file
        try:
            with open(file_path, "rb") as file:
                hash = hashlib.md5()
                while chunk := file.read(4096):
                    hash.update(chunk)
                return hash.hexdigest()
        except:
            return None

    def load_malware_definitions(self):
        malware_definitions = []
        malware_md5_hashes = []
        with open("definitions/full.csv", encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                malware_definitions.append(row)
                if len(row) > 2:
                    malware_md5_hashes.append(row[2])
        return malware_definitions, malware_md5_hashes


    def run_scan(self):
        print("1.0","> Loaded Definitions \n > " + self.malware_definitions[-1][0])
        self.text_box.config(state="normal")
        self.text_box.insert("end","\n> Loaded Malware Definitions")
        # display count
        self.text_box.insert("end","\n> " + self.malware_definitions[-1][0].replace("#",""))
        self.text_box.insert("end","\n> Scanning for malware...")
        self.text_box.config(state="disabled")

        # scan files
        scan_thread = threading.Thread(target=self.scan_files)
        scan_thread.start()