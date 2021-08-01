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

# Initialize service client with default config file
core_client = oci.core.VirtualNetworkClient(config)
identity_client = oci.identity.IdentityClient(config)

compartment_mc_name = mc_config.get('minecraft','compartment.name')
list_compartments_response = identity_client.list_compartments(compartment_id=config['tenancy'],name=compartment_mc_name)
compartment_mc_ocid = list_compartments_response.data[0].id
print(compartment_mc_ocid)

vcn_name = mc_config.get('minecraft','vcn.name')
list_vcns_response = core_client.list_vcns(compartment_id=compartment_mc_ocid,display_name=vcn_name)
vcn_mc_ocid = list_vcns_response.data[0].id
print(vcn_mc_ocid)

subnet_name = mc_config.get('minecraft','subnet.name')
list_subnets_response = core_client.list_subnets(compartment_id=compartment_mc_ocid,display_name=subnet_name)
subnet_mc_ocid = list_subnets_response.data[0].id
print(subnet_mc_ocid)

seclist_name = mc_config.get('minecraft','seclist.name')
print(seclist_name)

core_client = oci.core.VirtualNetworkClient(config)

# compartment_mc_ocid = 'ocid1.compartment.oc1..aaaaaaaal735azdobylwvrhvngpvwql5qlyyxfujjrryby65qopqxydizqaq'
# vcn_mc_ocid = 'ocid1.vcn.oc1.ap-melbourne-1.amaaaaaarcnfwfyaebzh6ainztbebkwu74gyqbr4bi2voiekbrkaecvy7cxq'
# subnet_mc_ocid = 'ocid1.subnet.oc1.ap-melbourne-1.aaaaaaaapkv2jn4c3o4qd6oxvu4mo37ytgdnpylcnivb5bci3zsrs3zgavwa'
# subnet_mc_ocid = 'ocid1.subnet.oc1.ap-melbourne-1.aaaaaaaam4r3t4fbdevaivraiwbgqsnw33g3i7kjmcalhjgxyy75yofveiwa'

list_security_lists_response = core_client.list_security_lists(
compartment_id=compartment_mc_ocid,
  display_name=seclist_name,
  sort_order="DESC")

if len(list_security_lists_response.data) > 0:
  print("found: "+list_security_lists_response.data[0].display_name+". Use update-seclist.py to update.")
  exit(1);

create_security_list_details = oci.core.models.CreateSecurityListDetails(
  compartment_id=compartment_mc_ocid,
  egress_security_rules=[],
  ingress_security_rules=[],
  vcn_id=vcn_mc_ocid,
  display_name=seclist_name)

create_security_list_response = core_client.create_security_list(
  create_security_list_details=create_security_list_details);

print(create_security_list_response.data)

get_subnet_response = core_client.get_subnet(
  subnet_id=subnet_mc_ocid)

subnet_mc = get_subnet_response.data
subnet_mc.security_list_ids.append(create_security_list_response.data.id)

update_subnet_details = oci.core.models.UpdateSubnetDetails(
  security_list_ids=subnet_mc.security_list_ids)

update_subnet_response = core_client.update_subnet(
  subnet_id=subnet_mc.id,
  update_subnet_details=update_subnet_details)

print(update_subnet_response.data)
