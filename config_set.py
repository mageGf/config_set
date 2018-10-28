# -*- coding: utf-8 -*-
# date:2018-10-28
# describe: telnet then set some config

from telnetlib import Telnet
from ftplib import FTP
import getopt, sys
import time

class Update:
    def __init__(self, ip, user='admin', passwd='admin'):
        self.ip = ip
        self.user = user
        self.passwd = passwd

    def __all_set(self,begin,end):
        #tel = null
        try:
            print("telnet...")
            tel = Telnet(self.ip)
            tel.read_until('Username:')
            tel.write(self.user + '\n')
            tel.read_until('Password:')
            tel.write(self.passwd + '\n')
            tel.read_until('ROS>')
            tel.write('en\n')
            tel.read_until('ROS#')
            
            # set apn和net
            tel.write('^config\n')
            tel.read_until('ROS(config)#')
            for port in range(begin, end+1):
                print('set port ' + str(port))
                #设置APN
                tel.write('mobile cmd at ' + str(port) + ' at+qicsgp=1,1,"","uno.au-net.ne.jp","123456",1\n')
                tel.read_until('ROS(config)#')
                time.sleep(0.1)
                #设置NET
                tel.write('mobile cmd at ' + str(port) + ' at+cgdcont=1,"IPV4V6","uno.au-net.ne.jp"\n')
                tel.read_until('ROS(config)#')
                #设置NET
                tel.write('mobile cmd at ' + str(port) + ' at+qcfg="ims",1\n')
                tel.read_until('ROS(config)#')
            
            tel.write('ex\n')
            tel.read_until('ROS#')
            
            tel.write('^ada\n')
            tel.read_until('ROS(ada)#')

                                           
        except:
            print("exception...")
        finally:
            print("all set...")
            tel.close()
            
    def __net_set(self,begin, end):
        #tel = null
        try:
            print("telnet...")
            tel = Telnet(self.ip)
            tel.read_until('Username:')
            tel.write(self.user + '\n')
            tel.read_until('Password:')
            tel.write(self.passwd + '\n')
            tel.read_until('ROS>')
            tel.write('en\n')
            tel.read_until('ROS#')
            
            # set apn
            tel.write('^config\n')
            tel.read_until('ROS(config)#')
            for port in range(begin, end+1):
                tel.write('mobile cmd at ' + str(port) + ' at+cgdcont=1,"IPV4V6","uno.au-net.ne.jp"\n')
                tel.read_until('ROS(config)#')
             
        except:
            print("exception...")
        finally:
            print("net set...")
            tel.close()
    
    def run(self,mode,begin, end):
        if mode == "all":
            self.__all_set(begin, end)
        else:
            self.__net_set(begin, end)


def main():
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "hi:u:p:m:b:e:", ["help", "ip", "username", "password","mode","begin","end"])
    except getopt.GetoptError:
        print("usage: " + sys.argv[0] + " -i ip -u username -p password -m mode -b begin -e end")
        sys.exit(2) 
    
    ip = "192.168.1.1"
    user = "admin"
    passwd = "admin"
    mode = "all"
    begin = 0
    end = 31
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("usage: " + sys.argv[0] + " -i ip  -u username -p password -mode[net|all] -begin port -end port")
            sys.exit()
        elif opt in ("-u", "--username"):
            user = arg
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--password"):
            passwd = arg
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-b", "--begin"):
            begin = int(arg)
        elif opt in ("-e", "--e"):
            end = int(arg)
        else:
            print("opt:" + opt)
            
    print("ip=" + ip) 
    print("user=" + user)
    print("passwd=" + passwd) 
    print("mode=" + mode)
    
    update = Update(ip, user, passwd)
    update.run(mode, begin, end)
    print("end...")

# Main Function
if __name__=='__main__':    
    main()