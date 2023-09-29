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
       # Allow all connections regardless of the origin
       return True

    def send_client_count(self):
        count = len(WebSocketHandler.clients)
        for client in WebSocketHandler.clients:
            try:
                client.write_message(str(count))
            except Exception as e:
                print(f"Error sending message to client: {e}")

    async def handle_message(self, message):
        if message.startswith("post"):
            # Extract post_id_var and author_id_var from the message
            try:
                _, post_id_var, _, author_id_var = message.split("{")
                post_id = int(post_id_var.split("}")[0])
                author_id = int(author_id_var.split("}")[0])

                # Construct the URL
                post_url = f"https://post.com/{post_id}"

                # Create HTTP request headers with Accept: application/json
                headers = {
                    "Accept": "application/json",
                }

                # Create an HTTP request
                request = HTTPRequest(post_url, method="GET", headers=headers)

                # Fetch the URL asynchronously
                http_client = AsyncHTTPClient()
                response = await http_client.fetch(request)

                # Send the JSON response back to the WebSocket client
                self.write_message(response.body)
            except Exception as e:
                print(f"Error handling message: {e}")

    def on_message(self, message):
        # Handle incoming messages
        tornado.ioloop.IOLoop.current().add_callback(self.handle_message, message)

app = tornado.web.Application([
    (r"/funsocket", WebSocketHandler),
])

if __name__ == "__main__":
    app.listen(8080)
    print("WebSocket server is running on port 8080")
    tornado.ioloop.IOLoop.current().start()
