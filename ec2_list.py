import boto3
import click
    
session = boto3.Session(profile_name='awsps')
ec2 = session.resource('ec2','us-west-2')

@click.command()
def list_instances():
    "List EC2 instances"
    for i in ec2.instances.all():
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            #i.key_name,
            i.private_ip_address,
            i.public_dns_name)))
    return

if __name__ == '__main__':
    list_instances()

