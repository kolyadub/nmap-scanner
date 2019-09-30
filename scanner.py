import nmap

def repeat():
    choice = input("Repeat a search? (y/n)")
    while choice != 'y' and choice != 'n':
        print("Wrong input!")
        choice = input("Repeat a search? ")
    if choice == 'y':
        main()
    else:
        print("\nBye!")
        exit()
    

def main():
    cpes = []
    nm = nmap.PortScanner()
    ip = input("Enter an IP address: ")
    print("Loading...")
    nm.scan(ip)
    for key in nm[ip]['tcp'].keys():
        if key == 80 or key == 8080:
            cpes.append([rec for rec in nm[ip]['tcp'][key]['cpe'].split(':')])
            
    if cpes:
        i = 1
        for cpe in cpes:
            print("{3}. Web server: {0} {1} {2}".format( cpe[2], cpe[3], cpe[4], i))
            i += 1
    else:
        print("Web servers are not found")
        repeat()
    
              
if __name__ == '__main__':
    main()