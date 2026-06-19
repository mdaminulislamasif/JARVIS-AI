import pyzipper
import os

zip_path = r'c:\Users\PHP\Desktop\JARVIS_PROJECT_v5_SECURE.zip'
folder_path = r'c:\Users\PHP\Desktop\ai'
password = b'asifgk777'

with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(password)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, folder_path)
            zf.write(file_path, arcname)

print(f"SUCCESS: Secure ZIP created at {zip_path}")
