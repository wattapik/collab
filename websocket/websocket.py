import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketHandler.clients.add(self)
        self.send_client_count()

    def on_close(self):
        WebSocketHandler.clients.remove(self)
        self.send_client_count()

    def send_client_count(self):
        count = len(WebSocketHandler.clients)
        for client in WebSocketHandler.clients:
            try:
                client.write_message(str(count))
            except Exception as e:
                print(f"Error sending message to client: {e}")

app = tornado.web.Application([
    (r"/funsocket", WebSocketHandler),
])

if __name__ == "__main__":
    app.listen(8080)
    print("WebSocket server is running on port 8080")
    tornado.ioloop.IOLoop.current().start()

