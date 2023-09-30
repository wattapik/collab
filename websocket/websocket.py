import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketHandler.clients.add(self)
        self.send_client_count()

    def on_close(self):
        WebSocketHandler.clients.remove(self)
        self.send_client_count()

    def check_origin(self, origin):
       return True

    def send_client_count(self):
        count = len(WebSocketHandler.clients)
        for client in WebSocketHandler.clients:
            try:
                client.write_message(str(count))
            except Exception as e:
                print(f"Error sending message to client: {e}")

    async def handle_message(self, message):
        try:
            post, user = message.split('by')
            post = int(post)
            user = int(user)

            post_url = f"https://sketchersunited.org/posts/{post}"
            headers = {
                "Accept": "application/json",
            }

            request = HTTPRequest(post_url, method="GET", headers=headers)

            http_client = AsyncHTTPClient()
            response = await http_client.fetch(request)
            self.write_message(response.body)

        except Exception as e:
            print(f"Error handling message: {e}")

    def on_message(self, message):
        tornado.ioloop.IOLoop.current().add_callback(self.handle_message, message)

app = tornado.web.Application([
    (r"/funsocket", WebSocketHandler),
])

if __name__ == "__main__":
    app.listen(8080)
    print("WebSocket server is running on port 8080")
    tornado.ioloop.IOLoop.current().start()
