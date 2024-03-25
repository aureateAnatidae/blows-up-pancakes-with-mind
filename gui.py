import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtBluetooth import *

from board import Board, connect

class Worker(QRunnable):
    """Generic QRunnable Worker template"""
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.fn(*self.args, **self.kwargs)


class Window(QMainWindow):
    """Window class encapsulating all program function. Can be treated as __main__ script."""
    def __init__(self):
        """
        Initialize main window
        """
        super().__init__()
        self.size = [800, 500]  # Window size
        self.appTimer = QTimer(self)
        self.appTimer.start(1000)  # 1 sec

        # ---- TITLE ---- #
        self.setWindowTitle("EXPLODE PANCAKES")
        self.setFixedSize(*self.size)
        self.welcome_prompt()

        self.show()
        
    ### QRunnables for QThreadPool ###
    ### >>NESTED CLASSES<<
    """To use any of these async. call a QThreadPool instance as self.<my_q_thread_pool>.start(<my_q_runnable>)"""
    

    ### MAIN SEQUENCE FUNCTIONS ###
    def welcome_prompt(self):
        """
        Welcome user with welcome message, prompt user to connect muse headset from list of headsets detected.

        Act as a title screen.
        Displays a continuously updating list of all nearby Bluetooth devices.
        """
        # WELCOME
        welcome = QLabel("Welcome to pancake exploder!\n"
                         "Make sure your Bluetooth is enabled!\n"
                         "Select your muse headset...", self)
        welcome.setFixedSize(*self.size)
        welcome.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        welcome.move(20, 20)
        welcome.show()

        # LIST HEADSETS (all BT devices)
        self.displayMuses = QListWidget(self)
        self.displayMuses.setFixedSize(200, 200)
        self.displayMuses.move(20, 200)
        self.displayMuses.show()

        self.scroll_bar = QScrollBar(self)
        self.displayMuses.setVerticalScrollBar(self.scroll_bar)

        # Dict of MAC addresses of each device found
        #self.bt_list = {}

        # UPDATE list of BT devices if not already found
        discovered = {}
        def list_update(bt_device_info):
            """Add BT device name to list display widget. Returns None."""
            if bt_device_info.name() not in discovered:
                discovered[bt_device_info.name()] = bt_device_info.address()
                self.displayMuses.addItem(bt_device_info.name())

        # BEGIN Bluetooth scan
        self.discoveryAgent = QBluetoothDeviceDiscoveryAgent(self)
        self.discoveryAgent.setLowEnergyDiscoveryTimeout(0)
        self.discoveryAgent.start()
        self.discoveryAgent.deviceDiscovered.connect(list_update)

        # On displayMuses item select, connect to the device with mac address.
        self.threadpool = QThreadPool()

        def gotime(item):
            worker = Worker(connect, mac_address=item.text())
            self.threadpool.start(worker)
        self.displayMuses.itemDoubleClicked.connect(gotime)

        ## ---- INITIAL BUTTON ---- #
        exitButton = QPushButton("X", self)
        exitButton.setFixedSize(50, 20)
        exitButton.move(750, 0)
        
        exitButton.clicked.connect(self.close)
        exitButton.show()

        #self.setCentralWidget(welcome)

class GUI():
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        self.app.aboutToQuit.connect(self.app.deleteLater)
        appWindow = Window()
        
        with open("style.css", "r") as styleSheet:
            self.app.setStyleSheet(styleSheet.read())

        self.__exit__()

    def __exit__(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    gui = GUI()
    gui.__exit__()