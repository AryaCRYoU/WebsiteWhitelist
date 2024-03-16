from flask import Flask, render_template, request, redirect, url_for
import paramiko
import json
import os

app = Flask(__name__)

def update_database(username, ip_address):
    database_file = 'database.json'
    if os.path.exists(database_file):
        with open(database_file, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    # Tambahkan username dan alamat IP ke database
    data[username] = ip_address

    with open(database_file, 'w') as file:
        json.dump(data, file)

def check_database(ip_address):
    database_file = 'database.json'
    if os.path.exists(database_file):
        with open(database_file, 'r') as file:
            data = json.load(file)
            for username, ip in data.items():
                if ip == ip_address:
                    return username  # Kembalikan nama pengguna yang terkait
    return None

@app.route('/', methods=['GET', 'POST'])
def register():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)  # Dapatkan alamat IP pengguna

    # Cek apakah alamat IP pengguna sudah terdaftar sebelumnya
    if check_database(ip_address):
        return redirect(url_for('error', blocked_ip=ip_address))
        
    if request.method == 'POST':
        username = request.form['username']

        # Tambahkan data pengguna ke dalam database
        update_database(username, ip_address)

        # Buat Koneksi
        sftp_host = "matrix.lemehost.com"
        sftp_port = 2022
        sftp_username = "user_761055.18d30e35"
        sftp_password = "DQEeUJHgIraWaVZTENWxxmQe6mkh2L0p"

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(sftp_host, port=sftp_port, username=sftp_username, password=sftp_password)
        sftp = ssh.open_sftp()

        remotepath = f"/scriptfiles/whitelist/{username}"
        sftp.open(remotepath + '.txt', 'w')

        sftp.close()
        ssh.close()

        return redirect(url_for('success'))        

    return render_template('index.html')

@app.route('/success')
def success():
    # Baca isi file success.html
    with open('success.html', 'r') as file:
        html_content = file.read()
    return html_content  

@app.route('/error')
def error():
  blocked_ip = request.args.get('blocked_ip')
  username = check_database(blocked_ip)

  # Baca isi file error.html
  with open('error.html', 'r') as file:
      error_html = file.read()

  # Ganti placeholder dengan nilai yang sesuai
  error_html = error_html.replace('{{blocked_ip}}', blocked_ip)
  error_html = error_html.replace('{{username}}', username)

  return error_html

if __name__ == '__main__':
    app.run(debug=False)
