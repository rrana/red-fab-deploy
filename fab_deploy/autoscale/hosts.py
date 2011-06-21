from fab_deploy.autoscale.server_data import get_data
from fab_deploy.aws import ec2_instance, ec2_instances, ec2_instance_with
from fab_deploy.conf import fab_config, fab_data
from fab_deploy.constants import SERVER_TYPE_DB, SERVER_TYPE_WEB
from fabric.api import env, runs_once

def set_hosts(hosts):
    ''' Set hosts based on instance id or public dns name '''
    env.hosts = []
    if not isinstance(hosts, (list, tuple)):
        hosts = [hosts]
    for host in hosts:
        if isinstance(host, basestring) and host.startswith('i-'):
            host = ec2_instance(host)
        if not isinstance(host, basestring):
            host = host.public_dns_name
        env.hosts.append('ubuntu@%s' % host)

@runs_once
def localhost():
    ''' Sets hosts to localhost '''
    set_hosts(['localhost'])

#def find_servers(stage, cluster):
#    '''Asks EC2 for servers with a given stage and cluster.  Returns list of servers.'''
#    config = fab_config.cluster(cluster)
#    data = fab_data.cluster(cluster)
#    server_type = config.get('server_type')
#    
#    
#
#    return [server for server in ec2_instances() if 
#        (stage == str(server.tags.get('Stage')) and (server_type is None or server_type == str(server.tags.get('Server Type'))))\
#            or server.image_id == data.get('image')]

#def autoscaling_servers(stage = None, cluster = None):
#    ''' Set hosts to *all* servers with same stage/cluster as current machine, or with provided stage/cluster'''
#    if stage: # For debugging
#        data = {'stage': stage, 'cluster': cluster}
#    else:
#        data = get_data()
#
#    set_hosts(find_servers(data['stage'], data['cluster']))

#def autoscaling_web_servers(stage = None, cluster = None):
#    ''' Set hosts to *running* web servers related to current machine
#        (either in same cluster if web, or in associated cluster if available), 
#        or with provided stage/cluster'''
#
#    if stage and cluster: # For debugging
#        data = {'stage': stage, 'cluster': cluster}
#    else:
#        data = get_data()
#
#    config = fab_config.cluster(data['cluster'])
#    if config.get('server_type') == SERVER_TYPE_WEB:
#        pass
#    elif config.get('with_web_cluster'):
#        data['cluster'] = config['with_web_cluster']
#    else:
#        raise NotImplementedError('Cound not find web autoscale cluster')
#
#    servers = [server for server in find_servers(data['stage'], data['cluster']) if str(server.update()) == 'running']
#
#    # We now have all of the web servers...
#    set_hosts(servers)

#def original_master(stage = None, cluster = None):
#    ''' Set hosts to original master db related to current machine,
#    (either in same cluster if db, or in associated cluster if available), 
#     or with provided stage/cluster '''
#
#    if stage and cluster: # For debugging
#        data = {'stage': stage, 'cluster': cluster}
#    else:
#        data = get_data()
#        
#    config = fab_config.get(data['cluster'])
#    
#    if config.get('server_type') == SERVER_TYPE_DB:
#        pass
#    elif config.get('with_db_cluster'):
#        data['cluster'] = config['with_db_cluster']
#    else:
#        raise NotImplementedError('Cound not find db autoscale cluster')
#    
#    master = ec2_instance_with(lambda instance: instance.tags.get(u'Name') == '%s-%s-master' % (data['stage'], data['cluster']))
#    if str(master.state) == 'running':
#        set_hosts([master])
#    else:
#        set_hosts([])
#    set_hosts([])