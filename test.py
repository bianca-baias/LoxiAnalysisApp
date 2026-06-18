import logging, os

class Methods:
    def __init__(self, results_path):
        self.logger = self.setup_logger(results_path)
        
    def setup_logger(self, destination_path):
        log_name = "test.log"
        logger_path = os.path.join(destination_path, log_name)
        
        if os.path.exists(logger_path):
            os.remove(logger_path)
            
        logger = logging.getLogger()
        logging.basicConfig(filename=logger_path, level=logging.INFO)
        logger.info(f" Initializing logger...")
        
        return logger

pt = r"C:\Users\Gamebox\Desktop"
mt = Methods(pt)
