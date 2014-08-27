from jnpr.junos import Device

#****************************************************************************#

# When user is proving hostname/ipaddress, username and password

dev = Device(host='hostname', user='username', password='password')
dev.open()

#****************************************************************************#

# SSH key is configured for given device/host for a user, no need to pass
# password
# To configure ssh key, you can refer to:
# https://techwiki.juniper.net/Automation_Scripting/030_Examples/Junos_NETCONF_and_SSH,_Part_1

dev = Device(host='hostname', user='username')
dev.open()

#****************************************************************************#

# If user does not provide *user* parameter, PyEZ will take $USER value of the
# current device (on which PyEZ is running) as user value. Hence we can also
# create Device object like:

dev = Device(host='hostname')
dev.open()

#****************************************************************************#

# It always best practice to configure ssh on device and use port 830 for NETCONF.
# For detail refer below link:
# http://www.juniper.net/techpubs/en_US/junos14.1/topics/topic-map/netconf-ssh-connection.html
# If for any reason we don't want to configure ssh need to specify parameter
# port to device

dev = Device(host='hostname', user='username', port=22)
dev.open()

#****************************************************************************#

# Want to get password at runtime. Using getpass python function
# For more detail of getpass refer:
# https://docs.python.org/2/library/getpass.html

from getpass import getpass

def connect(host, user, password=None):
    if password is None:
        password = getpass('password: ')
    return Device(host, user=user, password=password).open()

# Calling user defined connect function
dev = connect('hostname', 'username')

#****************************************************************************#

# Gather facts of device

from pprint import pprint
from jnpr.junos import Device

dev = Device(host='my_host_or_ipaddr', user='jeremy', password='jeremy123' )
dev.open()
# facts will contains device facts in Python dictionary format
# Using pprint to print to facts in structured format
pprint( dev.facts )
# close() function will close the connection to the device.
dev.close()

# Sample output of *dev.facts* from a ex device.

{'2RE': True,
 'HOME': '/var/home/xyz',
 'RE0': {'last_reboot_reason': 'Router rebooted after a normal shutdown.',
         'mastership_state': 'master',
         'model': 'RE-S-1800x4',
         'status': 'OK',
         'up_time': '4 days, 5 hours, 15 minutes, 5 seconds'},
 'RE1': {'last_reboot_reason': 'Router rebooted after a normal shutdown.',
         'mastership_state': 'backup',
         'model': 'RE-S-1800x4',
         'status': 'OK',
         'up_time': '4 days, 5 hours, 15 minutes, 35 seconds'},
 'domain': 'abc.xyz.com',
 'fqdn': 'nitin.abc.xyz.com',
 'hostname': 'nitin',
 'ifd_style': 'CLASSIC',
 'master': 'RE0',
 'model': 'MX240',
 'personality': 'MX',
 'serialnumber': 'JN121F1E1AFC',
 'switch_style': 'BRIDGE_DOMAIN',
 'version': '14.2I20140822',
 'version_RE0': '14.2I20140822',
 'version_RE1': '14.2I20140822',
 'version_info': 'junos.version_info(major=(14, 2), type=I, minor=20140822_0526, build=None)'}

#****************************************************************************#

# Disable Gather facts of device
# facts gathering requires few prc calls to be done. Which might take some time.
# If we don't need device facts and want to save those milliseconds, we can disable
# facts gathering by passing gather_facts=False to Device.

dev = Device(host='hostname', user='username', password='password', gather_facts=False )
dev.open()
# facts will contains empty dictionary
print dev.facts
{}
#****************************************************************************#