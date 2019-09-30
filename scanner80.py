import nmap
import requests
import socket


def repeat(): # Repeat function for main()
    choice = input("Repeat a search? (y/n)")
    while choice != 'y' and choice != 'n':
        print("Wrong input!")
        choice = input("Repeat a search? ")
    if choice == 'y':
        main()
    else:
        print("\nBye!")
        exit()
        
def valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

def main():
    nm = nmap.PortScanner()
    ip = input("Enter an IP address: ")
    
    while valid_ip(ip) == False:
        print("Wrong input!")
        ip = input("Enter an IP address: ")
        
    print("Loading...")
    nm.scan(hosts=ip, arguments='nmap -A -p 80')
    # Split cpe to ac ompany name, application name and version
    cpe = nm[ip]['tcp'][80]['cpe'].split(':')
    
    # Show a web server with a version if available
    if len(cpe) > 4:
        print("Web Server: {0} {1} {2}".format( cpe[2], cpe[3], cpe[4]))
    elif len(cpe) in range(1,4):
        print("Web Server: {0} {1}".format( cpe[2], cpe[3]))
    else:
        print("Web servers are not found")
        repeat()
    
    input("Press Enter to find vulnerables ")
    
    print("Loading...\n")
    # Get vulnerables by a company name and application name
    response = requests.get('https://cve.circl.lu/api/search/{0}/{1}'.format(cpe[2],cpe[3]))
    # Filter by a version. If version is unknown the list will be empty and vulnerables won't show
    version_filter = [el for el in response.json() if cpe[4] in str(el['vulnerable_configuration_cpe_2_2'])]

    i = 1
    if version_filter:
        print("The list of vulnerables for the given version:\n")
        for vurnalable in version_filter:
            print("{0}. Vulnerable number: {1}\n Date modified: {2}\n Summary: {3}\n".format(i, vurnalable['id'], vurnalable['Modified'][0:version_filter[1]['Modified'].index('T')], vurnalable['summary']))
            i += 1
    else:
        print("Vulnerables are not found")
    repeat()
              
if __name__ == '__main__':
    main()