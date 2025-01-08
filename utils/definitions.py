import requests
import os
import zipfile

def update_definitions():
    malware_bazaar_url = "https://bazaar.abuse.ch/export/csv/full/"
    local_path = "definitions/full.csv"
    local_path_zip = "definitions/definitions.zip"
    try:
        with requests.get(malware_bazaar_url, stream=True) as r:
            r.raise_for_status()
            with open(local_path_zip, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # Unzip the file
        with zipfile.ZipFile(local_path_zip, 'r') as zip_ref:
            zip_ref.extractall("definitions")
        
        # remove the zip file after extraction
        os.remove(local_path_zip)
        
        print("Definitions updated successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download definitions: {e}")
        return False
    
    return True