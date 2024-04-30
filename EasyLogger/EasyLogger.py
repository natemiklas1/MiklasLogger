import logging
import os
from datetime import datetime


# LOGGING_STYLES = ('DEFAULT', 'NEW_FILE')
# key is the user_input
LOGGING_STYLES = {
    'DEFAULT': {'mode': 'a'},
    'NEW_FILE': {'mode': 'w'},
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
    amountLogsToKeep: int = 0,
    loggerName: str = 'EasyLogger',
    loggingStyle: str = 'DEFAULT',
):
    """
    We can use this if we want a super easy logger
    """
    if loggingLevel is None:
        loggingLevel = 'INFO'
    if ignorePrintToConsole is None:
        ignorePrintToConsole is False

    if loggingStyle not in LOGGING_STYLES.keys():
        loggingStyle = 'DEFAULT'

    if loggingStyle == 'DEFAULT':
        logFilePrefix = loggerName
    elif loggingStyle == 'NEW_FILE':
        now = datetime.now()
        nowString = now.strftime('%Y%m%d%H%M%S')
        logFilePrefix = loggerName + '_' + nowString

    fullLogFileName = logFilePrefix + FILE_TYPE

    if not os.path.exists(logsDirectory):
        os.makedirs(logsDirectory)

    logger = logging.getLogger(loggerName)

    handler = logging.FileHandler(
        os.path.join(logsDirectory, fullLogFileName),
        mode=LOGGING_STYLES[loggingStyle]['mode'],
    )

    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d:%(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # add the stream handler to print to the console as well, if chosen
    if not ignorePrintToConsole:
        logger.addHandler(logging.StreamHandler())
    logger.setLevel(loggingLevel)

    if amountLogsToKeep is not None or amountLogsToKeep > 0:
        logClean(logger, logsDirectory, loggerName, amountLogsToKeep)

    return logger



def logClean(logger, logsDirectory: str, loggerName: str, amountLogsToKeep: int):
    filesInDir = os.listdir(logsDirectory)
    ticketLogFiles = [file for file in filesInDir if file.startswith(loggerName)]

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
