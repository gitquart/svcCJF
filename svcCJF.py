from pathlib import Path
from SMWinservice import SMWinservice
import mainCJF

class svcCJF(SMWinservice):
    _svc_name_ = "svcCJF"
    _svc_display_name_ = "svcCJF"
    _svc_description_ = "Service CJF..."

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        print('Starting svcService...')
        mainCJF.maincjf()
            

if __name__ == '__main__':
    svcCJF.parse_command_line()
