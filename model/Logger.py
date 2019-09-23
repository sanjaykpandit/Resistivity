from PyQt5.QtCore import QObject

class Logger(QObject):
    def __init__(s):
        super().__init__()
        s._txtColor = {
                           '0':'0',
                           'Black':'30',
                           'Red':'31',
                           'Green':'32',
                           'Yellow':'33',
                           'Blue':'34',
                           'Purple':'35',
                           'Cyan':'36',
                           'White':'37'
                       }
        s._txtStyle = {
                           '0':'0',
                           'NoEffect':'0',
                           'Bold':'1',
                           'Underline':'2',
                           'Negative1':'3',
                           'Negative2':'5'
                       }
        s._txtBackground = {
                            '0':'0',
                            'Black':'40',
                            'Red':'41',
                            'Green': '42',
                            'Yellow': '43',
                            'Blue': '44',
                            'Purple': '45',
                            'Cyan': '46',
                            'White': '47'
                            }

        s._formatString = ''
        s._clearString = '\033[0m'
        s._defaultTitle = ''

    def setDefaultTitle(s, title: str):
        s._defaultTitle = title + ": "


    def setFormat(s, txtStyle='0', txtColor='0', txtBackground='0'):
        s._formatString ="\033[{0};{1};{2}m".format(
                                s._txtColor[txtColor],
                                s._txtStyle[txtStyle],
                                s._txtBackground[txtBackground])

    def InfoLog(s, logString: str):
        s.setFormat('Bold', 'Blue')
        print(s._formatString + s._defaultTitle + logString + s._clearString)

    def DebugLog(s, logString: str):
        s.setFormat('Bold', 'Green')
        print(s._formatString + s._defaultTitle + logString + s._clearString)

    def WarningLog(s, logString: str):
        s.setFormat('Bold', 'Yellow')
        print(s._formatString + s._defaultTitle + logString + s._clearString)

    def ErrorLog(s, logString: str):
        s.setFormat('Bold', 'Red')
        print(s._formatString + s._defaultTitle + logString + s._clearString)