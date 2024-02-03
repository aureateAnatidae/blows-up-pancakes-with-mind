"""Main program file"""
# thanks to ChillOutCharles' BrainFlowsIntoVRChat and community
# thanks to the muselsl project. yo dr barachant save the muselsl project.

import argparse
import time

from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter, LogLevels

from cli import CLI

def main():
    BoardShim.enable_dev_board_logger()
    DataFilter.enable_data_logger()
    BoardShim.set_log_level(LogLevels.LEVEL_DEBUG.value)
    
    cli = CLI()
    ## create board, begin stream

    board = BoardShim(cli.args.board_id, cli.params)
    board.prepare_session()
    board.start_stream()
    print("streaming")
    time.sleep(2)
    print("a")
    time.sleep(2)
    print("stopping")
    board.stop_stream()
    board.release_session()
    #print(data)


if __name__ == "__main__":
    main()