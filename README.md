


Firewall policies contain object groups, hundreds of ip addresses and ACL's, services, address objects etc.  This script compares a set of firewall policies, across many firewalls,  and return differences in services, objects, ACL's (source/destination respectively)  to a Python dictionary.  

For example if different firewalls have a block list of 172.168.1.0 **/24** and 172.168.1.0 **/25**  this will return that difference.

  

We use a XML API (natively built in to Panorama) call to obtain the configuration files, so no need for token authentication as with REST API.  The script also returns object groups that exist in one firewall and not the other.  So if your firewalls have similar or dissimilar named policies with dozens of rules, this script can save time in validating the policies by hand. 

The script uses ElementTree for nested matches - in other words it won't return differences just because they exist over everything , it returns them when they belong to the same groups within the XML tree: Example:

deny 172.16.1.0 **/24** to any  
and  
deny 172.16.1.0 **/23** to any  


returns a match as the subnet configurations are different and they are in the same XML grouping.

deny any to any  
and  
deny 0.0.0.0/32 to any


does not return a misconfiguration match because it isn't part of the same XML grouping. The code can be modified to return this as a match.

 
The script drills down into the XML grouping of the data structures of the firewall and returns a report of mismatched policies or configurations.
  

_XML grouping example (this comes straight from the firewall):_
```
xml
<Element 'to' at 0x000002A06CE379C0>
<Element 'from' at 0x000002A06CE37A60>
<Element 'source' at 0x000002A06CE37B00>
<Element 'destination' at 0x000002A06CE37C40>
<Element 'application' at 0x000002A06CE37E20>
<Element 'service' at 0x000002A06CE37EC0>
<Element 'source-hip' at 0x000002A06CE37FB0>
<Element 'destination-hip' at 0x000002A06CE40090>
<Element 'action' at 0x000002A06CE40130>
```




For example notice in below the script will return services that exist in one Firewall and not the other. But it will also return services that exist in both firewalls but configured differently. If service-http (or http) exists in one firewall and not other we return difference. 

If http exists in both but ports are different we return difference. 

```xml
<entry name="Developer_To_WebServer" uuid="23ed0110-084e-44e8-9ed5-88fac9d64d45">
            <to>
            <member>any</member>
            ...[truncated]
            <service>
                <member>service-http</member>
                <member>service-https</member>
            </service>
            </to>
```






Script only requires port 22 SSH to function, using the netmiko library. It connects to devices in parallel (typically about 4 to 7 devices at once on a 4 core cpu), as it is multithreaded .

The XML grouping is built into the PA firewalls, and can be viewed through Panorama. We use scalable XML API call when connecting within the network:

  standard api link for all firewalls - I use xml path in place of restapi, so we don't have to do OAuth token calls
    
        #api_url = f'http://{fw_ip}/api/?type=config&action=get&xpath=/config/devices/entry[@name=\'localhost.localdomain\']/vsys/entry[@name=\'vsys1\']'

Or we use authentication cookie RestAPI call when connecting from outside the network for added security.

**the code for this is found in the /compare_Object_ACL's folder
(see above).**    

I can write a script of this level in 1-3 days.

Video below:


https://github.com/hfakoor222/Palo_Alto_Scripting/assets/105625129/f582cc49-3e04-4e09-89b5-a31136c54e9e  


<br/>
  

My PalotAlto script was nominated on the PaloAlto developers forum.<br/>
https://live.paloaltonetworks.com/t5/general-articles/nominated-discussion-script-that-returns-the-differences-in/ta-p/562409<br/>


**Code located at:  /compare_Object_ACL's  Folder**


<br/>
<br/>
      









  



        
  
Another script:
 ### Main Folder (second program)
Updates PaloAlto device ACL's. Logs in to multiple firewalls, returns permitted-ip profiles: 
user batch updates interface ACL's in a customized manner, by passing in lists/nested lists of ip_address/username/password,
and white-listed ip addresses to push permitted-ips. 


We can specify different interface profiles to update for different firewalls, so we have a fair bit of customization options.


Will soon be adding black-list, rollback, service policy, ip blackholing, and connectivity features (tests connectivity after ACL updates by using Scapy spoofed IP headers).




https://github.com/hfakoor222/Palo_Alto_Scripting/assets/105625129/fcf7c120-838a-442e-9f60-1c538148a74a


