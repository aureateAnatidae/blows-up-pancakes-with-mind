import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtBluetooth import *

#from board.py import Board

class Window(QMainWindow):
    """Window class encapsulating all program function. Can be treated as __main__ script."""
    def __init__(self):
        """
        Initialize main window
        """
        super().__init__()
        self.process = None
        self.size = [800, 500]  # Window size
        self.appTimer = QTimer(self)
        self.appTimer.start(1000)  # 1 sec

        # ---- TITLE ---- #
        self.setWindowTitle("EXPLODE PANCAKES")
        self.setFixedSize(*self.size)
        self.welcome_prompt()

        self.show()
        
    ### QProcesses ###
    def cli(self, listObject):
        """Janky solve - get args and params from cli.py, specifying only --board-id"""
        if self.process is None:
            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.triggerprint)
            self.process.finished.connect(self.process_finished)

            device_name = listObject.text()
            mac_address = None
            print("Selecting")
            print(device_name)
            #print(self.discoveryAgent.discoveredDevices())
            for device in self.discoveryAgent.discoveredDevices():
                print("Am I here?")
                print(device.name())
                if device_name == device.name():
                    print("WATASHI GA KITA!")
                    mac_address = device.address()
                    self.process.setArguments([f"--mac-address {mac_address}"])
                    break
            self.process.start("python", ["cli.py"])
            print(mac_address.toString())
            

    def triggerprint(self):
        print("ha! gayyyyy")
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)

    def process_finished(self):
        print("Process finished")
        self.process = None

    ### MAIN SEQUENCE FUNCTIONS ###
    def welcome_prompt(self):
        """
        Welcome user with welcome message, prompt user to connect muse headset from list of headsets detected.

        Act as a title screen.
        Displays a continuously updating list of all nearby Bluetooth devices.
        """
        # ---- WELCOME AND LIST HEADSETS ---- #

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
        self.displayMuses.setFixedSize(200, 700)
        self.displayMuses.move(20, 200)
        self.displayMuses.show()

        # Dict of MAC addresses of each device found
        #self.bt_list = {}

        # UPDATE list of BT devices
        def list_update(bt_device_info):
            """Add BT device name to list display widget. Returns None."""
            self.displayMuses.addItem(bt_device_info.name())
            #self.bt_list[bt_device_info.name()] = bt_device_info.address()

        # BEGIN Bluetooth scan
        self.discoveryAgent = QBluetoothDeviceDiscoveryAgent(self)
        self.discoveryAgent.setLowEnergyDiscoveryTimeout(0)
        self.discoveryAgent.start()
        self.discoveryAgent.deviceDiscovered.connect(list_update)

        # On displayMuses item select, connect to the device with mac address.
        self.displayMuses.itemDoubleClicked.connect(self.cli)

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