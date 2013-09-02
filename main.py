from SOAPpy import WSDL, Errors
import ConfigParser


OVH_WSDL_URL = 'http://www.ovh.com/soapi/soapi-re-latest.wsdl'

def main():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    login = config.get('ovh', 'login')
    password = config.get('ovh', 'password')

    domains = []
    with open("domains", "r") as f:
        domains = f.read().splitlines()

    client = WSDL.Proxy(OVH_WSDL_URL)

    try:
        session = client.login(login, password)
        for domain in domains:
            result = client.domainCheck(session, domain)
            for info in result['item']:
                if info['predicate'] == 'is_available' and info['value'] is True:
                    print('Domain %s is available' % domain)
    except Errors.Error, e:
        print(e)

if __name__ == '__main__':
    main()