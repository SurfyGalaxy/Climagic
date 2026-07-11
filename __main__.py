from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QInputDialog, QMessageBox, QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot, QUrl, Qt, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtNetwork import QNetworkProxyFactory
import json, os, traceback, sys
import pre_processor
fname = None
class Backend(QObject):
    python_message_signal = pyqtSignal(str)

    @pyqtSlot(str)
    def handle_js_message(self, message_from_js):
        global fname
        msg = json.loads(message_from_js)
        print(msg)
        if msg["act"] == "pick_file":
            name = QFileDialog.getOpenFileName(filter="*.txt")
            fname = name[0]
            print(name)
            self.python_message_signal.emit(json.dumps({"act":"picked", "name": os.path.basename(name[0])}))
        elif msg["act"] == "parsefile":
            try:
                with open(fname,'r') as f:
                    data = pre_processor.process_text(f.read())
                    self.python_message_signal.emit(json.dumps({"act":"data", "data": data}))

            except Exception as e:
                QMessageBox.critical(None, "Error in processing file", traceback.format_exc())
                exit()
        elif msg["act"] == "resize":
            e
class HybridApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Climagic")
        self.setGeometry(100,100,500,500)
        self.setup_ui()
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.backend = Backend()
        self.channel = QWebChannel(self)
        self.channel.registerObject("backend", self.backend)
        self.browser.page().setWebChannel(self.channel)
        self.browser.load(QUrl("https://surfygalaxy.github.io/Climagic/"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = HybridApp()
    window.show()
    sys.exit(app.exec())