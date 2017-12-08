#------------------------------------
# List all instances in all regions
#------------------------------------

from sys import argv
import boto3
from botocore.exceptions import ClientError

script, status_instance = argv
client = boto3.client('ec2')
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

print "||Public IP||Instance Name||Instance ID||Instance Type||Region||"
for region in ec2_regions:
    conn = boto3.resource('ec2', region_name=region)
    instances = conn.instances.filter()
    for instance in instances:
        """
        list all running instances
        """
        if instance.state["Name"] == status_instance:
            instancename = ''
            for tag in instance.tags:
                if tag["Key"] == 'Name':
                    try:
                        instancename = tag["Value"]
                        print "|%s|%s|%s|%s|%s|" % (instance.public_ip_address, instancename, instance.id, instance.instance_type, region)
                    except ClientError as e:
                        print "Unexpected error: %s" % e
