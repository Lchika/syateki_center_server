import pathlib
import logging
import logging.config

abs_dir = str(pathlib.Path(__file__).parent.resolve())
logging.config.fileConfig(abs_dir + '/logging.conf')

# create logger
_logger = logging.getLogger('develop')


def logger():
    return _logger


if __name__ == '__main__':
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
