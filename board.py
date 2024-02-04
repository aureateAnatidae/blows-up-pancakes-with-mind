"""Function to connect with params/args from cli.py, set up stream"""

class Board:
    def __init__(self):
        BoardShim.enable_dev_board_logger()
        DataFilter.enable_data_logger()
        BoardShim.set_log_level(LogLevels.LEVEL_DEBUG.value)

        self.board = BoardShim(cli.args.board_id, cli.params)

    def connect(self):
        
        board.prepare_session()
        board.start_stream()
        time.sleep(2)
        print("slept")
        board.stop_stream()
        board.release_session()

if __name__ == "__main__":
    board = Board()