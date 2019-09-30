import nmap
import requests


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
            if len(cpe) > 4:
                print("{3}. Web server: {0} {1} {2}".format( cpe[2], cpe[3], cpe[4], i))
            else:
                print("{2}. Web server: {0} {1}".format( cpe[2], cpe[3], i))
            i += 1       
    else:
        print("Web servers are not found")
        repeat()
    
    wserver_num = input("Choose a web server number to find vulnerables: ")
    
    while int(wserver_num) > i:
        print("Wrong input!")
        wserver_num = input("Choose a web server number to find vulnerables: ")
    
    print("Loading...")
    response = requests.get('https://cve.circl.lu/api/search/{0}/{1}'.format(cpes[i-1][2],cpes[i-1][3]))
    if len(cpe[i-1]) > 4:
        version_filter = [el for el in response.json() if cpes[i-1][4] in str(el['vulnerable_configuration_cpe_2_2'])]
    
    i = 1
    if version_filter:
        print("The list of vulnerables:\n")
        for vurnalable in version_filter:
            print("{0}. Vulnerable number: {1}\n Date modified: {2}".format(i, version_filter[1]['id'], version_filter[1]['Modified'][0:version_filter[1]['Modified'].index('T')]))
              
if __name__ == '__main__':
    main()