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

name = sys.argv[1]
if len(sys.argv) >= 3:
  new_ip = sys.argv[2]
else:
  new_ip = None

list_security_lists_response = core_client.list_security_lists(
compartment_id=compartment_mc_ocid,
  display_name=seclist_name,
  sort_order="DESC")

current_security_list = list_security_lists_response.data[0]

found_name = False
new_ingress_security_rules = []
if len(current_security_list.ingress_security_rules) > 0:
  for il in current_security_list.ingress_security_rules:
    if il.description == name:
      found_name = True
      print(il.source)
      if new_ip != None:
        il.source = new_ip+'/32'
        new_ingress_security_rules.append(il)
    else:
      new_ingress_security_rules.append(il)

if found_name == False:
  ingress_security_rules=[
    oci.core.models.IngressSecurityRule(
      description=name,
      protocol='6',
      source=new_ip+"/32",
      tcp_options=oci.core.models.TcpOptions(
        destination_port_range=oci.core.models.PortRange(
          max=25565,
          min=25565))
      ),
    oci.core.models.IngressSecurityRule(
      description=name,
      protocol='17',
      source=new_ip+"/32",
      udp_options=oci.core.models.UdpOptions(
        destination_port_range=oci.core.models.PortRange(
          max=25565,
          min=25565))
    )]
  new_ingress_security_rules.extend(ingress_security_rules)

update_security_list_details=oci.core.models.UpdateSecurityListDetails(
  display_name=current_security_list.display_name,
  ingress_security_rules=new_ingress_security_rules)

update_security_list_response = core_client.update_security_list(
  security_list_id=current_security_list.id,
  update_security_list_details=update_security_list_details);

print(update_security_list_response.data)
