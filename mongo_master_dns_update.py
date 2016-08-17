#!/bin/python

#############################################################################################
# This scripts connects to local mongoDB replica set and checks if it's the master          #
# If it is the master then it will update the selected url with current instance Public IP  #
#                                                                                           #
#############################################################################################
import boto3
from pymongo import MongoReplicaSetClient
import socket


server_config = {
    'aws_access_key_id': '',
    'aws_secret_access_key': '',
    'region_name': '', #ex . us-east-1
    'fqdn': '', #ex. master.mongodb.staging.example.com
    'hostedZoneId': '',
}

local_config = {
    'host': '127.0.0.1',
    'port': '27017',
    'rs_name': '' #ex. PRODUCTIONRS
}

def update_dns(fqdn, ip):
    print "updating dns name=" + fqdn + " ip=" + ip
    client = boto3.client('route53', aws_access_key_id=server_config['aws_access_key_id'], aws_secret_access_key=server_config['aws_secret_access_key'])
    hostedZoneId = server_config['hostedZoneId']

    response = client.change_resource_record_sets(
        HostedZoneId = hostedZoneId,
        ChangeBatch={
            'Comment': 'comment',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': fqdn,
                        'Type': 'A',
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': ip
                            },
                            ],
                        }
                },
                ]
        }
    )



def get_mongo_primary_ip():
    conn = MongoReplicaSetClient(local_config['host'] + ":" + local_config['port'], repl
    print "Mongodb Primary node=" + conn.primary[0] + " ip=" + socket.gethostbyname(conn
    return socket.gethostbyname(conn.primary[0])

def get_local_ipv4():
    import urllib2
    local_ipv4 = urllib2.urlopen("http://169.254.169.254/latest/meta-data/local-ipv4").r
    print "Local ipv4=" + local_ipv4
    return local_ipv4


mongo_primary_ip = get_mongo_primary_ip()
local_ipv4 = get_local_ipv4()
if mongo_primary_ip == local_ipv4:
    print "I am mongodb master"
    #I'm the master so i can make updates
    if socket.gethostbyname(server_config['fqdn']) != mongo_primary_ip:
    #update primary ip
        update_dns(server_config['fqdn'], mongo_primary_ip)

