import subprocess
import serial


class CONSOLE_test:
    def __init__(self, logname, hostname, port, username, password):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def test_content(self):

        # # create SSH item
        # ssh = paramiko.SSHClient()
        # # permit connect to remote host
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # # connect
        # ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\r\rCONSOLE test start \r")
        CONSOLE_result = 'FAIL'
        subprocess.getoutput("stty -F /dev/ttyUSB0 speed 115200")
        subprocess.getoutput("stty -F /dev/ttyUSB0 speed 115200")

        console_port = subprocess.getoutput('ls -l /dev/ttyUSB*')
        if 'ttyUSB0' in console_port:
            ser = serial.Serial("/dev/ttyUSB0",115200,timeout = 10)
            # t = cat_console_value(self.logname)
            # t.start()
            ser.write('test'.encode())
            with open(self.logname, 'a+') as f:
                f.write('console port send value test \r')
            # print('console port send value test')
            value_receive = ser.read(4)
            with open(self.logname, 'a+') as f:
                f.write('console get value is: %s \r' % value_receive)
            # print('console get value is: %s'%(value_receive))
            if 'test'.encode() in value_receive:
                CONSOLE_result = 'PASS'
                with open(self.logname, 'a+') as f:
                    f.write('CONSOLE Test Pass \r')
            else:
                with open(self.logname, 'a+') as f:
                    f.write('CONSOLE Test Failed, console receive wrong data, error code 19001 \r')
            # stop_thread(t)
            # t.stop()

        else:
            with open(self.logname, 'a+') as f:
                f.write('CONSOLE Test Failed, no console port detect, error code 19002 \r')

        # ssh.close()
        return CONSOLE_result