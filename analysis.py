# Take data stream, preprocess, analyze, return a result
# Evaluates the data quality, returns result
# Evaluates correlation with PANCAKE EXPLOSION INTENT, returns result

from brainflow.data_filter import DataFilter
from brainflow.board_shim import BoardShim
import numpy as np

class Analyzer:
    def __init__(self, board):
        self.board = board

    def avg_V_over_T(self, time):
        # The Muse headband takes 256 samples per second.
        """
        Return the average voltage for each electrode per <time> amount of seconds.

        Parameters
        ----------
        time : int
            Timescale to consider voltage of electrodes.
        """
        data = self.board.get_board_data(256)
        for array in data:
            print(np.average(array))
        print("BANDPASSING!")
        
        for array in data:
            DataFilter.perform_bandpass(array, 256, start_freq=2, stop_freq=60, order=2, filter_type=0, ripple=0)
            print(np.average(array))
        return 