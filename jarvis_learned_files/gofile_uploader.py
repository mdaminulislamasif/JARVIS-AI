import requests

def upload_to_gofile(file_path):
    print(f"[*] Fetching Gofile server...")
    try:
        server_resp = requests.get('https://api.gofile.io/getServer')
        server = server_resp.json()['data']['server']
        
        print(f"[*] Uploading to {server}.gofile.io...")
        with open(file_path, 'rb') as f:
            r = requests.post(f'https://{server}.gofile.io/uploadFile', files={'file': f})
            if r.status_code == 200:
                link = r.json()['data']['downloadPage']
                print(f"\n[SUCCESS] JARVIS IS ONLINE!")
                print(f"DOWNLOAD LINK: {link}")
                return link
            else:
                print(f"[ERROR] Upload failed: {r.text}")
    except Exception as e:
        print(f"[ERROR] {e}")

file_to_upload = r'c:\Users\PHP\Desktop\JARVIS_PROJECT_v5_SECURE.zip'
upload_to_gofile(file_to_upload)
