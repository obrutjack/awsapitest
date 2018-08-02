import boto3
import click
    
session = boto3.Session(profile_name='awsps')
ec2 = session.resource('ec2','us-west-2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances
   

@click.group()
def instances():
    """Commands for instances management"""

@instances.command('list')
@click.option('--project', default=None,
    help="Only instance for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    instances = []

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or {} }
        if i.key_name: 
            key_name = i.key_name 
        else: 
            key_name = "No_Key"

        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            key_name, 
            i.private_ip_address,
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))
    return

@instances.command('stop')
@click.option('--project', default=None,
    help='Only instances for project')
def stop_instances(project):
    "Stop EC2 instances"
    
    instances = filter_instances(project)
    
    for i in instances:
        print("Stopping {0}...".format(i.id)) 
        i.stop()
    
    return

@instances.command('start')
@click.option('--project', default=None,
    help='Only instances for project')
def start_instances(project):
    "Start EC2 instances"
    
    instances = filter_instances(project)
    
    for i in instances:
        print("Starting {0}...".format(i.id)) 
        i.start()
    
    return

if __name__ == '__main__':
    instances()

