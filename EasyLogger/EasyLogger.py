import logging
import os
from datetime import datetime


# LOGGING_STYLES = ('DEFAULT', 'NEW_FILE')
LOGGING_STYLES = {
    'default': 'DEFAULT',
    'newFile': 'NEW_FILE'
}

FILE_TYPE = '.log'

"""
DEFAULT will create one logging stream per logger and continually append.

NEW_FILE will create a new log file each time a new logger instance is created.
"""

def getEasyLogger(
    
    logsDirectory: str,
    ignorePrintToConsole: bool = False,
    loggingLevel: str = 'INFO',
    amountLogsToKeep: int | None = None,
    loggerName: str = 'EasyLogger',
    loggingStyle: str = 'DEFAULT'
):
    """
    We can use this if we want a super easy logger
    """
    if loggingLevel is None:
        loggingLevel = 'INFO'
    if ignorePrintToConsole is None:
        ignorePrintToConsole is False

    if loggingStyle not in (list(LOGGING_STYLES.values())):
        loggingStyle = LOGGING_STYLES['default']


    if loggingStyle == LOGGING_STYLES['default']:
        logFilePrefix = loggerName
    elif loggingStyle == LOGGING_STYLES['newFile']:
        now = datetime.now()
        nowString = now.strftime('%Y%m%d%H%M%S')
        logFilePrefix = loggerName + '_' + nowString

    fullLogFileName = logFilePrefix + FILE_TYPE


    if not os.path.exists(logsDirectory):
        os.makedirs(logsDirectory)

    logger = logging.getLogger(loggerName)

    handler = logging.FileHandler(os.path.join(logsDirectory,fullLogFileName), mode='a')

    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(loggingLevel)


    if amountLogsToKeep is not None:
        logClean(logger, logsDirectory, loggerName, amountLogsToKeep)

    return logger


class EasyLogger:
    def __init__(
        self,
        logsDirectory: str,
        ignorePrintToConsole: bool,
        loggingLevel: str = 'INFO',
        amountLogsToKeep: int | None = None,
        loggerName: str = 'MiklasLogger',
    ):
        # self.loggingLevel = loggingLevel

        self._amountLogsToKeep = amountLogsToKeep

        if loggingLevel is None:
            loggingLevel = 'INFO'

        if ignorePrintToConsole is None:
            self.ignorePrintToConsole is False
        self.ignorePrintToConsole = ignorePrintToConsole

        now = datetime.now()
        nowString = now.strftime('%Y%m%d%H%M%S')

        self._logsDirectory = logsDirectory
        self._logFileName = nowString + '_' + self._logFileSuffix + '.log'

        # self.logsDirectory = logsDirectory

        if not os.path.exists(logsDirectory):
            os.makedirs(logsDirectory)

        logger = logging.getLogger(loggerName)

        handler = logging.FileHandler(self._logsDirectory + self._logFileName, mode='w')

        formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(loggingLevel)

        self._logger = logger

        if self._amountLogsToKeep:
            logClean(self._logger, self._logsDirectory, self._logFileSuffix, self._amountLogsToKeep)

    def getCurrentLevel(self):
        return self._logger.level

    def _printMessage(self, message: str) -> bool:
        if self.ignorePrintToConsole:
            return False
        print(message)
        return True


    def writeInfo(self, message: str):
        self._logger.info(message)
        self._printMessage(message)

    def writeDebug(self, message: str):
        self._logger.debug(message)
        self._printMessage(message)

    def writeCrticial(self, message: str):
        self._logger.critical(message)
        self._printMessage(message)



def logClean(logger, logsDirectory: str, loggerName: str, amountLogsToKeep: int):
    filesInDir = os.listdir(logsDirectory)
    ticketLogFiles = [
        file for file in filesInDir if file.startswith(loggerName)
    ]

    if len(ticketLogFiles) >= amountLogsToKeep:
        fileswithDates = [
            {
                'date': os.path.getctime(os.path.join(logsDirectory, file)),
                'fileName': file,
            }
            for file in ticketLogFiles
        ]

        fileswithDatesSorted = sorted(fileswithDates, key=lambda file: file['date'])
        [
            (
                logger.debug(
                    f"will delete file: {os.path.join(logsDirectory, file['fileName'])}"
                ),
                os.remove(os.path.join(logsDirectory, file['fileName'])),
            )
            for file in fileswithDatesSorted[
                0 : len(fileswithDatesSorted) - amountLogsToKeep
            ]
        ]
    else:
        logger.debug("Cant't delete more logs than we have.")