# oci-mc-seclist

Purpose: To assist the management of the security list used with Minecraft. Adding a management tool to support the adding / removing specific IP addresses to allow to connect to the minecraft server.

Requires:
- OCI Python SDK (requirements.txt file includes the dependency)
- OCI API key and configuration (Required for the OCI Python SDK. Also you can use this tool to help generate the configuration. https://github.com/jlowe000/oci-config-gen)

Configuration (in mc-config.properties):
- compartment.name - name of the Compartment where the VCN and Subnet exist and Security List to be created.
- vcn.name - name of the VCN where Minecraft is hosted.
- subnet.name - name of the Public Subnet where Minecraft is hosted.
- seclist.name - name of the Security List (where the IP addresses will be managed).

What this does:
- create-seclist.py - Adds a security list to the Public Subnet.
- list-seclist.py - Lists the IP addresses that have been configured in the Security List.
- update-seclist.py - Updates the Security List with an IP address (and a name) and adds ingress rules for 25565/TCP and 25565/UDP.

To create a Security List and attach it to the Public Subnet.
```
python3 create-seclist.py
```

To list the IP addresses managed by the Security List
```
python3 create-seclist.py
```

To add an IP address (and a name) to be managed by the Security List
```
python3 update-seclist.py NewIP 192.0.0.1
```

To remove an existing IP address from the Security List (by name)
```
python3 update-seclist.py NewIP
```
