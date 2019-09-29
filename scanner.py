import nmap

def main():
    wserver = {}
    nm = nmap.PortScanner()
    ip = input("Enter an IP address: ")
    print("Loading...")
    nm.scan(ip)
    try:
        wserver = nm[ip]['tcp'][80]
    except KeyError:
        print("Web server is not found")
    if wserver:
        print("Web server is: {0} {1}".format(nm[ip]['tcp'][80]['product'], nm[ip]['tcp'][80]['version']))
              
if __name__ == '__main__':
    main()