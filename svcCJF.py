from pathlib import Path
from SMWinservice import SMWinservice
import mainCJF
import utils as tool
import sys

class svcCJF(SMWinservice):
    _svc_name_ = "svcCJF"
    _svc_display_name_ = "svcCJF"
    _svc_description_ = "Service CJF..."

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        tool.appendInfoToFile('C:\\','test.txt','Starting service...')
        try:
            mainCJF.maincjf()
        except:
            tool.appendInfoToFile('C:\\','CJF_log.txt',str(sys.exc_info()[0]))

            

if __name__ == '__main__':
    svcCJF.parse_command_line()
