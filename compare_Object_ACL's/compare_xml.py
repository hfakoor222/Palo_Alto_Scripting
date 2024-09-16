import os
import xml.etree.ElementTree as ET
import re
import pprint
import sys

sys.setrecursionlimit(10_000)
def parsing_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    # root_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
    return root

def compare_policies(file1_root, file2_root):
    # Find the <rules> elements in both trees
    rules1 = file1_root.find(".//rulebase/security/rules")
    rules2 = file2_root.find(".//rulebase/security/rules")


    # Function to return matching attributes
    def matching_attributes(elem1, elem2):
        difference_attributes = {}
        elem1_attributes = []
        elem2_attributes = []
        global file1_ip, file2_ip


        #the below code we loop through each child tag of both elements  1 level deep, and append them to a list.
        #If the child tags of both lists have the same tag.text value we compare the member values.
        #If member values are not the same length or value, we know the policies aren't the same
        """here is an example of the XML:
        <entry name="Developer_To_WebServer" uuid="23ed0110-084e-44e8-9ed5-88fac9d64d45">
            <to>
            <member>any</member>
            ...[truncated]
            <service>
                <member>service-http</member>
                <member>service-https</member>
            </service> 
        In this xml example, if service tag matches on the firewalls, if member values of the service tag are 
        different it will be printed to a differences dictionary. This holds true for all policies 
        "Developer_To_WebServer"
        here is a truncated list:
        [<Element 'to' at 0x0000022F233B79C0>... <Element 'service' at 0x0000022F233B7EC0>]
        notice service tag is 1 level deep. If tags match across lists we comare the lengths and the tags remaining
        inside service tag"""

        for sub_elem1 in elem1:
            for tag in sub_elem1:
                elem1_attributes.append(tag)
        for sub_elem2 in elem2:
            for tag in sub_elem2:
                elem2_attributes.append(tag)
        for elem1 in elem1_attributes:
            for elem2 in elem2_attributes:
                if elem1.tag == elem2.tag:

                    """ here is my example output from this above code:
                    <Element 'to' at 0x000002A06CE379C0>
                    <Element 'from' at 0x000002A06CE37A60>
                    <Element 'source' at 0x000002A06CE37B00>
                    <Element 'destination' at 0x000002A06CE37C40>
                    <Element 'application' at 0x000002A06CE37E20>
                    <Element 'service' at 0x000002A06CE37EC0>
                    <Element 'source-hip' at 0x000002A06CE37FB0>
                    <Element 'destination-hip' at 0x000002A06CE40090>
                    <Element 'action' at 0x000002A06CE40130>
                    
                    these tags match accross firewalls for the "Developer_To_WebServer" object group.
                    now we compare the values and the lengths of the member tags
                    """
                    for member1 in elem1:
                        for member2 in elem2:
                            if member1.text != member2.text:
                                difference_attributes[file1_ip] = difference_attributes.get(file1_ip, []) + [member1.text]
                            if member2.text != member1.text:
                                difference_attributes[file2_ip] = difference_attributes.get(file2_ip, []) + [member2.text]
        print(difference_attributes)
        return  difference_attributes
    return matching_attributes(rules1, rules2)

def compare_object_groups(file1_root, file2_root):
    group1_placeholder = []
    group2_placeholder = []
    object_group_differences = {}

    #below we create two dictionaries which includes all the sub-tags in a PaloAlto xml configuration file, under address-group/entry tag
    elements1 = {entry.get("name"): entry for entry in file1_root.findall(".//address-group/entry")}
    elements2 = {entry.get("name"): entry for entry in file2_root.findall(".//address-group/entry")}
    for name, group1 in elements1.items():
        print(name)
        #here we find matching tags in the second firewall
        group2 = elements2.get(name)
        #if matching tag is found, we iterate through sub-tags and write the differences to a dictionary
        if group2:
            if ET.tostring(group1) == ET.tostring(group2):
                #here we iterate through tags using iter() function
                for i in group2.iter():
                    group1_placeholder.append(i.text)
                for y in group1.iter():
                    group2_placeholder.append(y.text)
            global file1_ip, file2_ip
            #here we find the differences in existing tags of an object group: this can be individual ip addresses or ip address objects
            #the code immediately below recurses through each data structure, checking each element
            group1_difference = [i for i in group1_placeholder if i not in group2_placeholder]
            group2_difference = [i for i in group2_placeholder if i not in group1_placeholder]
            object_group_differences[file1_ip] = group1_difference if group1_difference else object_group_differences
            object_group_differences[file2_ip] = group2_difference if group2_difference else object_group_differences
            # print(object_group_differences)
            return object_group_differences
        #below code is optional extension to return object group exists in one firewall but not the other
        # for name, group2 in elements2.items():
        #     if name not in elements1:
        #         # Address group exists in the second file but not in the first file
        #         object_group_differences[name] = "Address group exists in the second file but not in the first file"


if __name__ == "__main__":
    folder_path = os.path.join(os.getcwd(), "firewall_xmls")
    xml_files = [f for f in os.listdir(folder_path) if f.endswith("object_groups.xml")]
    results = open("result_file.txt", "a+")
    if len(xml_files) < 2:
        print("There are not enough XML files to compare.")
    else:

        policy_differences = []
        object_group_difference = {}
        for i in range(len(xml_files)):
            file1_path = os.path.join(folder_path, xml_files[i])
            file1_ip = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", file1_path).group()
            file1_root = parsing_xml(file1_path)

            for j in range(i + 1, len(xml_files)):
                file2_path = os.path.join(folder_path, xml_files[j])
                file2_ip = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", file2_path).group()
                file2_root = parsing_xml(file2_path)

                # Compare and store the differences
                key = f"Differences between {file1_ip} and {file2_ip}"
                object_group_difference[key] = compare_object_groups(file1_root, file2_root)

            #here we compare firewall policies
            result = compare_policies(file1_root, file2_root)
            object_group_difference["Differences in members of policies"] = result
            #by this point we have a deeply nested dictionary: standard json.dumps or pprint may not work: for us this is a good thing,
            #it means we are successfully comparing nested policies
            file_path = f"{folder_path}/firewall_xmls"
            outfile = open(file_path+ "outfile.txt", "a+")
            outfile.write(str(object_group_difference))

            outfile.close()







