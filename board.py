"""Function to connect with params/args from cli.py, set up stream"""

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
from brainflow.data_filter import DataFilter
from brainflow.exit_codes import BrainFlowError

from PySide6.QtCore import *
import time

class Board(BoardShim):
    def __init__(self, mac_address):
        """Inherit BoardShim, initializes with Brainflow setup commands first."""
        params = BrainFlowInputParams()
        params.mac_address = mac_address
        super().__init__(board_id=41, input_params=params)

        self.enable_dev_board_logger()
        DataFilter.enable_data_logger()
        self.set_log_level(LogLevels.LEVEL_DEBUG.value)

    def connect(self):
        """Connect, start streaming session. Get data with get_board_data()."""
        self.prepare_session()
        self.start_stream()
        time.sleep(1)
        data = self.get_current_board_data(256)
        print(data)
    
    def disconnect(self):
        """Disonnect from active stream."""
        self.release_session()


def connect(mac_address):
    """Create Board object, stream data from this object async. with BoardShim methods"""
    print("Connecting to " + str(mac_address))
    board = Board(mac_address)
    board.connect()
    
if __name__ == "__main__":
    board = Board("0055DAB0C515")
    board.prepare_session()
    board.start_stream()
    time.sleep(1)
    data = board.get_current_board_data(256)
    print(data)
    board.release_session()