import webview
from server import app

window = webview.create_window('Currency_converter', app, width=560, height=640)
webview.start()
