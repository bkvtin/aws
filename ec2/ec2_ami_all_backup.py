#------------------------------------
# Take ami in all regions
#
# Instance tag needs to have
#   Key: Auto_Backup
#   Value: Yes
#------------------------------------

import datetime
import boto3
from botocore.exceptions import ClientError


def main():
    client = boto3.client('ec2')
    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

    for region in ec2_regions:
        conn = boto3.resource('ec2', region_name=region)
        filters = [{'Name':'tag:Auto_Backup', 'Values':['Yes']}]
        instances = conn.instances.filter(Filters=filters)

        for instance in instances:
            nowtime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            tag_date = datetime.datetime.now().strftime('%Y%m%d')

            """
            Get the instance name
            """
            ec = boto3.client('ec2', region)
            for tag in instance.tags:
                if tag["Key"] == 'Name':
                    ami_name = "%s - %s - %s" % (instance.id, tag["Value"], nowtime)
                    # -- debug
                    print ":: %s" % ami_name

            """
            Take AMI with setting name, description
            """
            ami_id = ec.create_image(
                InstanceId=instance.id,
                Name=ami_name,
                Description="Maintenance created AMI of instance " + instance.id + " from " + nowtime,
                NoReboot=True,
                DryRun=False
            ); print ami_id['ImageId']

            """
            Add tags AMI after creation
            """
            response = ec.create_tags(
                Resources=[
                    ami_id['ImageId'],
                ],
                Tags=[
                    {
                        'Key': 'Date',
                        'Value': tag_date,
                    },
                    {
                        'Key': 'Maintenance',
                        'Value': 'Auto',
                    },
                ],
            )
            # print(response)

if __name__ == "__main__":
    main()
