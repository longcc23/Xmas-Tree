#!/usr/bin/env python3
import http.server
import ssl
import socket

PORT = 8443

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

httpd = http.server.HTTPServer(('0.0.0.0', PORT), MyHTTPRequestHandler)

# 创建自签名证书
import subprocess
import os

cert_file = 'cert.pem'
key_file = 'key.pem'

if not os.path.exists(cert_file) or not os.path.exists(key_file):
    print("生成自签名SSL证书...")
    subprocess.run([
        'openssl', 'req', '-new', '-x509', '-keyout', key_file, '-out', cert_file,
        '-days', '365', '-nodes', '-subj', '/CN=localhost'
    ], check=True)
    print("证书生成完成！")

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_file, key_file)

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

local_ip = get_local_ip()
print(f"\n{'='*60}")
print(f"🎄 HTTPS 服务器已启动！")
print(f"{'='*60}")
print(f"\n📱 手机访问地址（需在同一WiFi下）：")
print(f"   https://{local_ip}:{PORT}/Xmas%20tree.html")
print(f"\n💻 电脑访问地址：")
print(f"   https://localhost:{PORT}/Xmas%20tree.html")
print(f"\n⚠️  首次访问会提示证书不安全，请点击「继续访问」或「高级 > 继续」")
print(f"{'='*60}\n")

httpd.serve_forever()
