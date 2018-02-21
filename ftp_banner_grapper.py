import socket


def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return str(banner)
    except:
        return

def checkVulns(banner):
    if 'FreeFloat FTP Server (Version 1.00)' in str(banner):
        print('[+] Vulnerable! ')

def main():
    portList = [21, 22, 25, 80, 110, 443]
    for x in range(1, 10):
        ip = '192.168.1.' + str(x)
        for port in portList:
            banner = retBanner(ip, port)
            if banner:
                print('[+] ' + ip + ': ' + banner.strip('\n'))
                checkVulns(banner)

if __name__ == '__main__':
    main()
