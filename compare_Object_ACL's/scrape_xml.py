##This code scrapes the device data structures. This is a simple scraper that returns the XML.

import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import os
import time



# list of firewall IP addresses and credentials: we can use an encrypted file instead of a list
firewalls = [
    {
        'ip': '192.168.56.134',
        'user': 'admin',
        'password': 'Admin123',
    },
    {
        'ip': '192.168.56.130',
        'user': 'admin',
        'password': 'Admin123',
    },

{
        'ip': '192.168.56.131',
        'user': 'admin',
        'password': 'Admin123',
    },
    # Add more firewalls as needed
]





def xml_scraper( firewalls, textfile = "textfile.txt"):
    # Create a directory to store XML files
    output_directory = 'firewall_xmls/'

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through each firewall
    for node in firewalls:
        fw_ip = node['ip']
        username = node['user']
        password = node['password']
        print(fw_ip)
        # standard api link for all firewalls - I use xml path in place of restapi, so we don't have to do OAuth token calls
        api_url = f'http://{fw_ip}/api/?type=config&action=get&xpath=/config/devices/entry[@name=\'localhost.localdomain\']/vsys/entry[@name=\'vsys1\']'

        try:
            # GET response to get the XML
            response = requests.get(api_url, auth=HTTPBasicAuth(username, password), verify=False)
            print(response)
            print(type(response))

            if response.status_code == 200:
                print(response.text)
                output_file = os.path.join(output_directory, f'{fw_ip}_object_groups.xml')
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                # we dont need time.sleep() or to close the file but I use it as a safety valve
                f.close()
                time.sleep(1)

                print(f"Configuration saved for {fw_ip} to {output_file}")
            else:
                print(f"Failed to retrieve configuration for {fw_ip}. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error accessing {fw_ip}: {str(e)}")


xml_scraper(firewalls)
