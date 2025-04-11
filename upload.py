import ftplib
import os
import sys

# FTP server details
FTP_HOST = 'giowm1354.siteground.biz'
FTP_PORT = 21
FTP_USER = 'website@aplusapps.org'
FTP_PASS = '522)11@[k|(5'
FTP_DIR = 'aplusapps.org/public_html'

def upload_file(ftp, local_file, remote_file):
    try:
        with open(local_file, 'rb') as file:
            ftp.storbinary(f'STOR {remote_file}', file)
        print(f'Uploaded {local_file} to {remote_file}')
    except Exception as e:
        print(f'Error uploading {local_file}: {str(e)}')

def main():
    try:
        print(f'Connecting to FTP server {FTP_HOST}...')
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        print(f'Attempting to login with user: {FTP_USER}')
        ftp.login(FTP_USER, FTP_PASS)
        print('Connected successfully!')

        # Change to the correct directory
        print(f'Changing to {FTP_DIR} directory...')
        try:
            # Split the path and navigate each directory
            for dir_part in FTP_DIR.split('/'):
                try:
                    ftp.cwd(dir_part)
                    print(f'Changed to {dir_part}')
                except ftplib.error_perm as e:
                    print(f'Could not change to {dir_part}: {str(e)}')
                    print('Trying to continue...')
        except Exception as e:
            print(f'Error changing directories: {str(e)}')
            print('Trying to continue in current directory...')

        # Upload main files
        upload_file(ftp, 'index.html', 'index.html')
        upload_file(ftp, 'styles.css', 'styles.css')
        upload_file(ftp, 'app_data.json', 'app_data.json')

        # Create and upload to images directory
        print('Uploading images...')
        try:
            ftp.mkd('images')
            print('Created images directory')
        except ftplib.error_perm as e:
            print(f'Note: {str(e)}')

        ftp.cwd('images')
        for file in os.listdir('images'):
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                upload_file(ftp, f'images/{file}', file)
        ftp.cwd('..')

        print('Upload complete!')
        ftp.quit()

    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main() 