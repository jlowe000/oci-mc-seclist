import oci
import sys
import configparser

# Create a default config using DEFAULT profile in default location
# Refer to
# https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm#SDK_and_CLI_Configuration_File
# for more info
config = oci.config.from_file(profile_name="minecraft")

mc_config = configparser.RawConfigParser()
mc_config.read('mc-config.properties')

core_client = oci.core.VirtualNetworkClient(config)
identity_client = oci.identity.IdentityClient(config)

compartment_mc_name = mc_config.get('minecraft','compartment.name')
list_compartments_response = identity_client.list_compartments(compartment_id=config['tenancy'],name=compartment_mc_name)
compartment_mc_ocid = list_compartments_response.data[0].id
print(compartment_mc_ocid)

vcn_name = mc_config.get('minecraft','vcn.name')
list_vcns_response = core_client.list_vcns(compartment_id=compartment_mc_ocid,display_name=vcn_name)
vcn_ocid = list_vcns_response.data[0].id
print(vcn_ocid)

subnet_name = mc_config.get('minecraft','subnet.name')
list_subnets_response = core_client.list_subnets(compartment_id=compartment_mc_ocid,display_name=subnet_name)
subnet_ocid = list_subnets_response.data[0].id
print(subnet_ocid)

seclist_name = mc_config.get('minecraft','seclist.name')
print(seclist_name)

list_security_lists_response = core_client.list_security_lists(
  compartment_id=compartment_mc_ocid,
  display_name=seclist_name,
  sort_order="DESC")

current_security_list = list_security_lists_response.data[0]

if len(current_security_list.ingress_security_rules) > 0:
  for il in current_security_list.ingress_security_rules:
    if il.protocol == '6': # TCP
      found_name = True
      print(il.description+': '+il.source)
else:
  print('no rules found')
