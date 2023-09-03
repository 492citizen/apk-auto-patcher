import logging
logging.basicConfig()

listener_logger = logging.getLogger("Listener Logger")
listener_logger.addHandler(logging.FileHandler("logs/listenerThread"))
listener_logger.setLevel(logging.DEBUG)

apkmirror_logger = logging.getLogger("APKMirror Logger")
apkmirror_logger.addHandler(logging.FileHandler("logs/apkmirror"))
apkmirror_logger.setLevel(logging.DEBUG)