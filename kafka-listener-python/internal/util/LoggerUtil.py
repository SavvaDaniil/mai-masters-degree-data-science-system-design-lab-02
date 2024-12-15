import logging

class LoggerUtil():

    def get_logger() -> logging.Logger:
        #logging.basicConfig(level=logging.ERROR, filename="logs.txt", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")
        #logging.disable(level=logging.INFO)
        return logging.getLogger()
