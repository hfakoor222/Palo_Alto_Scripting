
**/compare_Object_ACL's**  Folder

Firewall policies contain object groups, hundreds of ip addresses and ACL's, services, address objects etc.  This script compares a set of firewall policies with the same name, across many firewalls,  and return differences in services, address objects, ACL's etc (source/destination respectively)  to a Python dictionary.  

For example if different firewalls have a block list of 172.168.1.0**/24** and 172.168.1.**0/25**  this will return that difference.

  

We use a XML API (natively built in to Panorama) call to obtain the configuration files, so no need for token authentication as with REST API.  The script also returns object groups that exist in one firewall and not the other.  So if your firewalls have similar named policies with dozens of rules, this script can save time in validating the policies by hand. Video below:


https://github.com/hfakoor222/Palo_Alto_Scripting/assets/105625129/f582cc49-3e04-4e09-89b5-a31136c54e9e

the code for this is found in the /compare_Object_ACL's folder
in my repo.    

  


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


