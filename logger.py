import logging
import sys

logger = logging.getLogger("lip-logger")
formatter = logging.Formatter('%(asctime)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

streamHandler = logging.StreamHandler(stream=sys.stdout)
streamHandler.setFormatter(formatter)

fileHandler = logging.FileHandler('lip.log')
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

logger.setLevel(logging.DEBUG)