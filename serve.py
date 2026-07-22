#!/usr/bin/env python3
"""本地预览《马斯克的未来学校》网页版。
用法：cd web && python3 serve.py  然后浏览器打开 http://localhost:8641/
Godot 4 Web 导出启用了线程（SharedArrayBuffer），必须带 COOP/COEP 响应头，
普通 `python3 -m http.server` 缺这两个头会导致游戏无法启动。
"""
import http.server
import mimetypes
import os
import sys

def _parse_port() -> int:
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a in ("--port", "-p") and i + 1 < len(args):
            return int(args[i + 1])
        if a.startswith("--port="):
            return int(a.split("=", 1)[1])
        if a.isdigit():
            return int(a)
    return int(os.environ.get("PORT", 8641))


PORT = _parse_port()

mimetypes.add_type("application/wasm", ".wasm")


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        # 跨源隔离：启用 SharedArrayBuffer（线程版引擎必需）
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Resource-Policy", "cross-origin")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:  # 静默常规访问日志
        pass


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as srv:
        print(f"🎮 网页版已启动：http://localhost:{PORT}/  （Ctrl+C 停止）")
        srv.serve_forever()
