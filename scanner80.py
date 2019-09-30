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
    nm.scan(hosts=ip, arguments='nmap -A -p 80')
    cpe = nm[ip]['tcp'][80]['cpe'].split(':')
    
    if len(cpe) > 4:
        print("Web server: {0} {1} {2}".format( cpe[2], cpe[3], cpe[4]))
    elif len(cpe) < 4:
        print("Web server: {0} {1}".format( cpe[2], cpe[3]))
    else:
        print("Web servers are not found")
        repeat()
    
    input("Press enter to find vulnerables")
    
    print("Loading...")
    response = requests.get('https://cve.circl.lu/api/search/{0}/{1}'.format(cpe[2],cpe[3]))
    if len(cpe) > 4:
        version_filter = [el for el in response.json() if cpe[4] in str(el['vulnerable_configuration_cpe_2_2'])]
    else:
        version_filter = response.json()
    
    i = 1
    if version_filter:
        print("The list of vulnerables:\n")
        for vurnalable in version_filter:
            print("{0}. Vulnerable number: {1}\n Date modified: {2}\n Summary: {3}\n".format(i, vurnalable['id'], vurnalable['Modified'][0:version_filter[1]['Modified'].index('T')], vurnalable['summary']))
            i += 1
    else:
        print("Vulnerables are not found")
              
if __name__ == '__main__':
    main()