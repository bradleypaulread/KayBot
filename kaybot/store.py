from pathlib import Path
import logging


LOG_NAME = 'kaybot.log'
LOGFILE = Path.joinpath(Path().absolute(), LOG_NAME)

logging.basicConfig(filename=LOG_NAME, level=logging.INFO, format='%(asctime)s:%(name)s:%(levelname)s: %(message)s')
