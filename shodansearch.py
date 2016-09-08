import shodan
import sys
import getpass
import subprocess as sp
from termcolor import colored

temp = sp.call('clear', shell=True)
temp
print colored("          _____ __              __          ", 'red')
print colored("         / ___// /_  ____  ____/ ____ _____ ", 'red')
print colored("         \__ \/ __ \/ __ \/ __  / __ `/ __ \ ", 'white')
print colored("        ___/ / / / / /_/ / /_/ / /_/ / / / /", 'white')
print colored("       /____/_/ /_/\____/\__,_/\__,_/_/ /_/ ", 'blue') 
print ("")

                
API_KEY = getpass.getpass('Enter your API key: ')

api = shodan.Shodan(API_KEY)

def menu():
    menu = {}
    menu['1.']="Search Shodan"
    menu['2.']="Search Facets"
    menu['3,']="Host LookUp"
    menu['4.']="Account Info"
    menu['5.']="Services"
    menu['6.']="Exit"
    while True:
        options = menu.keys()
        options.sort()
        for entry in options:
            print colored(entry, 'white', attrs=['bold']), colored(menu[entry], 'green')

        selection = raw_input("Please Select: ")
        if selection == '1':
            search()
        elif selection == '2':
            facets()
        elif selection == '3':
            host_info()
            return
        elif selection == '4':
            print('\n')
            show_info()
        elif selection == '5':
            print('\n')
            services()            
        elif selection == '6':
            global tmp
            sys.exit(1)
        else:
            print "That option is unknown."

def search():
    # Wrap the request in a try/except block to catch errors
    try:
        # Search Shodan
        results = api.search(raw_input("Enter your query: "), page=1)

        # Show the results
        
        print 'Results found: %s' % results['total']
        for result in results['matches']:

            print colored('IP: %s' % colored(result['ip_str'], 'green'), 'red', attrs=['bold'])
            print colored('Hostname: %s' % colored(result['hostnames'], 'cyan'), 'white', attrs=['bold'])
            print colored('Org: %s' % colored(result['org'], 'blue'), 'white', attrs=['bold'])
           # print colored('Domains: %s' % colored(result['domains', 'red'), 'white', attrs=['bold'])
           # print colored('OS: %s' % colored(result['os'], 'green'), 'white', attrs=['bold'])
            print colored('Port: %s' % colored(result['port'], 'magenta'), 'white', attrs=['bold'])
 
            print colored('%s' % result['data'], 'white')

        print ''
    except shodan.APIError, e:
        print 'Error: %s' % e   
            
def host_info():
    IP = raw_input("Enter the host IP: ")
    host = api.host(IP)
    print colored("IP: %s" % colored(host['ip_str'], 'green'), 'white', attrs=['bold'])
    print colored("Organization: %s" % colored(host.get('org', 'n/a'), 'green'), 'white', attrs=['bold'])
    print colored("Operating System: %s" % colored(host.get('os', 'n/a'), 'green'), 'white', attrs=['bold'])
    
    for item in host['data']:
        print colored("Port: %s" % colored(item['port'], 'green'), 'white', attrs=['bold'])
        print colored("Banner: %s" % colored(item['data'], 'blue', attrs=['bold']), 'white', attrs=['bold'])

   

def show_info():
    info = api.info()
    for x,y in info.iteritems():
        print colored(x, 'white', attrs=['bold']), colored(y, 'green')
    print ''             

def services():
    service = api.services()
    for x,y in service.iteritems():
        print colored(x, 'white', attrs=['bold']), colored(y, 'green')
    print '' 

def facets():
    FACETS = [
            'org',
            'domain',
            'port',
            'asn',
            ('country', 5),
    ]
    FACET_TITLES = {
            'org': 'Top 10 Organizations',
            'domain': 'Top 10 Domains',
            'port': 'Top 10 Ports',
            'asn': 'Top 10 Automomous Systems',
            'country': 'Top 5 Countries',
    }
    try:
        query = raw_input('Enter query to show for which to show stats: ')
        result = api.count(query, facets=FACETS)

        print colored('Shodan Summary Information', 'white', attrs=['bold'])
        print colored('Query: %s', 'white', attrs=['bold']) % colored(query, 'green')
        print colored('Total Results: %s\n', 'white', attrs=['bold']) % colored(result['total'], 'green')

        for facet in result['facets']:
            print colored(FACET_TITLES[facet], 'white', attrs=['bold'])

            for term in result['facets'][facet]:
                print '%s: %s' % (term['value'], term['count'])

            print ''
    except Exception, e:
        print 'Error: %s' % e
        sys,exit(1)

if  __name__ == '__main__':
    menu()
