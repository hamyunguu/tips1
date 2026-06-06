#!/usr/bin/env python3
"""TIPS 미러용 정적 서버 — 브라우저 캐시를 끄고 항상 최신 파일을 서빙."""
import http.server, socketserver, os

PORT = 5200
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site"))

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
    print(f"serving site/ at http://localhost:{PORT}/ (no-cache)")
    httpd.serve_forever()
