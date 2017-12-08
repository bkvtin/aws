#------------------------------------
# Take ami with prompting <instance-id> <region-name>
#------------------------------------

from sys import argv
import datetime
import boto3
from botocore.exceptions import ClientError


def main(argv):
    script, instance_backup, region = argv

    conn = boto3.resource('ec2', region_name=region)
    filters = [{'Name':'tag:Auto_Backup_Test', 'Values':['Yes']}]
    instances = conn.instances.filter(Filters=filters)

    for instance in instances:
        nowtime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        tag_date = datetime.datetime.now().strftime('%Y%m%d')

        """
        Get the instance name
        """
        ec = boto3.client('ec2', region)
        for tag in instance.tags:
            if instance.id == instance_backup:
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
                    ); print ami_id

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
                                'Value': 'Manual',
                            },
                        ],
                    ); print(response)

            else:
                print "Don't have this instance %s in region %s" %(instance_backup, region)

if __name__ == "__main__":
    main(argv)
