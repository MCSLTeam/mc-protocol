from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
from threading import Thread
from socketserver import TCPServer

# 配置基本参数
CLIENT_ID = "18a1a4c2-ccae-4306-9e55-e9500a1793d7"
REDIRECT_PORT = 11451
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}/"
SCOPE = "service::user.auth.xboxlive.com::MBI_SSL"


class CodeHandler(SimpleHTTPRequestHandler):
    code = None
    
    def do_GET(self):
        # 只处理/callback路径的请求
        if self.path.startswith('/'):
            # 解析查询参数
            query = urlparse(self.path).query
            params = parse_qs(query)
            
            # 检查授权码
            if 'code' in params:
                code = params['code'][0]
                
                CodeHandler.code = code

                # 发送响应给浏览器
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Success! You may now close this page.')
                
                # 关闭服务器
                self.server.shutdown_flag = True
            else:
                # 处理错误
                error = params.get('error', ['unknown_error'])[0]
                self.send_error(400, f"Authorization failed: {error}")
        else:
            self.send_error(404)

class CodeServer(TCPServer):
    """可安全关闭的服务器"""
    allow_reuse_address = True
    shutdown_flag = False
    
    def serve_forever(self):
        while not self.shutdown_flag:
            self.handle_request()

'''if __name__ == "__main__":
    
    # 2. 启动服务器线程
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 4. 等待服务器完成
    server_thread.join()'''
    