import logging
import os
from datetime import datetime


def getEasyLogger(
    
    logsDirectory: str,
    ignorePrintToConsole: bool = False,
    loggingLevel: str = 'INFO',
    logFileSuffx: str = '',
    amountLogsToKeep: int | None = None,
    loggerName: str = 'EasyLogger',
):
    """
    We can use this if we want a super easy logger
    """
    if loggingLevel is None:
        loggingLevel = 'INFO'
    if ignorePrintToConsole is None:
        ignorePrintToConsole is False

    #now = datetime.now()
    #nowString = now.strftime('%Y%m%d%H%M%S')

    if logFileSuffx == '':
        logFileSuffx = '_' + logFileSuffx 
    logFileName = loggerName + '_' + logFileSuffx + '.log'

    if not os.path.exists(logsDirectory):
        os.makedirs(logsDirectory)

    logger = logging.getLogger(loggerName)

    handler = logging.FileHandler(os.path.join(logsDirectory,logFileName), mode='w')

    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(loggingLevel)


    if amountLogsToKeep is not None:
        logClean(logger, logsDirectory, logFileSuffx, amountLogsToKeep)

    return logger


class MiklasLogger:
    def __init__(
        self,
        logsDirectory: str,
        ignorePrintToConsole: bool,
        loggingLevel: str = 'INFO',
        logFileSuffix: str = '',
        amountLogsToKeep: int | None = None,
        loggerName: str = 'MiklasLogger',
    ):
        # self.loggingLevel = loggingLevel

        self._amountLogsToKeep = amountLogsToKeep

        self._logFileSuffix = logFileSuffix

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



def logClean(logger, logsDirectory: str, logFileSuffx: str, amountLogsToKeep: int):
    filesInDir = os.listdir(logsDirectory)
    ticketLogFiles = [
        file for file in filesInDir if file.endswith(logFileSuffx)
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