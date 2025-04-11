#!/bin/bash

# Create FTP commands file
cat > ftp_commands.txt << EOL
user website@ourhostingsites.org @,24f$1j33*3
binary
cd /public_html
pwd
mkdir images
put index.html
put styles.css
put app_data.json
cd images
mput images/*
bye
EOL

# Run FTP commands
ftp -n ftp.ourhostingsites.org 21 < ftp_commands.txt

# Clean up
rm ftp_commands.txt 