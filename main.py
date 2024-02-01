from muselsl import stream, list_muses
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import asyncio
import nest_asyncio
nest_asyncio.apply()

from bleak import BleakScanner
from continuous_scan import cont_scan

#import bt_test

#muses = list_muses()
#stream(muses[0]['address'])

class StdWindow(QMainWindow):
    def __init__(self):
        '''
        standard window to be used
        '''
        super().__init__()
        self.size = [800, 500]  # Window size
        self.appTimer = QTimer()
        self.appTimer.start(100)

        # ---- TITLE ---- #
        self.setWindowTitle("EXPLODE PANCAKES")
        self.setFixedSize(*self.size)
        self.welcome_prompt()

        self.show()

    def welcome_prompt(self):
        '''
        Welcomes user with welcome message, prompts user to connect muse headset from list of headsets detected.

        Returns
        -------
        MAC : str
            MAC address of muse headset to connect to
        '''
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

        display_muses = QListWidget(self)
        # CONT list update
        self.appTimer.timeout.connect(display_muses.update)
        devices = map(str, asyncio.run(cont_scan()))
        display_muses.addItems(devices)
        display_muses.setFixedSize(200, 700)
        display_muses.move(20, 200)
        display_muses.show()

        ## ---- INITIAL BUTTON ---- #
        button = QPushButton("Press me", self)
        button.setFixedSize(200, 100)
        button.clicked.connect(self.close)
        button.show()


        self.setCentralWidget(button)
        #self.setCentralWidget(welcome)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    appWindow = StdWindow()

    with open("style.css", "r") as styleSheet:
        app.setStyleSheet(styleSheet.read())

    sys.exit(app.exec())