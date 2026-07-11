from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot, QUrl, pyqtSignal
import json
import os
import traceback
import sys
import pre_processor

fname = None

class Backend(QObject):
    python_message_signal = pyqtSignal(str)
    # Define a signal that sends two integers: width and height
    resize_signal = pyqtSignal(int, int)

    @pyqtSlot(str)
    def handle_js_message(self, message_from_js):
        global fname
        msg = json.loads(message_from_js)
        
        if msg["act"] == "pick_file":
            name = QFileDialog.getOpenFileName(filter="Plain Text (*.txt);;All Files (*)",initialFilter="*.txt")
            fname = name[0]
            self.python_message_signal.emit(json.dumps({"act":"picked", "name": os.path.basename(name[0])}))
            
        elif msg["act"] == "parsefile":
            try:
                with open(fname,'r') as f:
                    data = pre_processor.process_text(f.read())
                    self.python_message_signal.emit(json.dumps({"act":"data", "data": data}))
            except Exception as e:
                QMessageBox.critical(None, "Error in processing file", traceback.format_exc())
                sys.exit()
                
        elif msg["act"] == "resize":
            # Extract width and height from the JavaScript message (defaulting to current size if missing)
            width = msg.get("width", 500)
            height = msg.get("height", 500)
            # Emit the signal to notify the main window
            self.resize_signal.emit(width, height)

class HybridApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Climagic")
        self.setGeometry(100, 100, 500, 500)
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        
        self.backend = Backend()
        
        # Connect the backend's resize signal directly to the QMainWindow's resize method
        self.backend.resize_signal.connect(self.resize)
        
        self.channel = QWebChannel(self)
        self.channel.registerObject("backend", self.backend)
        self.browser.page().setWebChannel(self.channel)
        # self.browser.load(QUrl("http://127.0.0.1:5500/ui/"))
        self.browser.load(QUrl("https://surfygalaxy.github.io/Climagic/"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HybridApp()
    window.show()
    sys.exit(app.exec())