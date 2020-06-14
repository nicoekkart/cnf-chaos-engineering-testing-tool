import logging

def logger(name):
    if not name: name=__name__
    _logger = logging.getLogger(name)
    if not _logger.hasHandlers():
        c_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(name)s] - %(levelname)s - %(message)s')
        _logger.setLevel(logging.DEBUG)
        c_handler.setFormatter(formatter)
        _logger.addHandler(c_handler)
    return _logger