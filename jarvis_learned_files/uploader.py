import requests

def upload_file(file_path):
    print(f"[*] Uploading {file_path} to secure storage...")
    try:
        with open(file_path, 'rb') as f:
            # Using file.io for a quick secure link
            response = requests.post('https://file.io', files={'file': f})
            if response.status_code == 200:
                link = response.json().get('link')
                print(f"\n[SUCCESS] JARVIS UPLOADED!")
                print(f"LINK: {link}")
                return link
            else:
                print(f"[ERROR] Upload failed with status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")

file_to_upload = r'c:\Users\PHP\Desktop\JARVIS_PROJECT_v5_SECURE.zip'
upload_file(file_to_upload)
