import subprocess
import os

CONFIG_SOPHOS = 'sophos'
CA_GREP = 'REF_Ca'


def write_domains_file(domains, out_file):
    """Creates domain.txt file needed for dehydrated script"""
    with open(out_file, 'w') as output:
        for domain in domains:
            output.write('%s\n'%domains[domain])


def load_domains():
    domains = {}
    p1 = subprocess.Popen("/usr/local/bin/confd-client.plx  get_objects ca host_key_cert".split(),
                          stdout=subprocess.PIPE)
    p2 = subprocess.Popen("grep \'ref\'".split(),
                          stdin=p1.stdout, stdout=subprocess.PIPE)

    for line in p2.communicate():
        if line:
            for segment in line.split(','):
                if segment.split() and segment.split("'")[3][0:6] == 'REF_Ca':
                    domains[segment.split("'")[3]] = raw_input("Full domain for certificate %s: "
                                                               % segment.split("'")[3])
    return domains


def setup(root_path):
    import urllib2
    import zipfile


    # git isn't installed by default
    os.chdir(root_path)
    with open('master.zip', 'wb') as f:
        f.write(urllib2.urlopen('https://github.com/lukas2511/dehydrated/archive/master.zip').read())
        f.close()
    zip = zipfile.ZipFile('master.zip')
    zip.extractall()
    os.remove('master.zip')

    with open('master.zip', 'wb') as f:
        f.write(urllib2.urlopen('https://github.com/rklomp/sophos-utm-letsencrypt/archive/master.zip').read())
        f.close()
    zip = zipfile.ZipFile('master.zip')
    zip.extractall()
    os.remove('master.zip')

    with open('config', 'wb') as f:
        f.write(urllib2.urlopen('https://raw.githubusercontent.com/iandday/le-godaddy-dns/master/config').read())
        f.close(

    # query sophos UTM for cert information
    domains = load_domains()
    # create domains file for dehydrated
    write_domains_file(domains, os.path.join('dehydrated-master', 'domains.txt'))

    #write GoDaddy keys file
    with open('keys', 'w') as output:
        output.write('[go_daddy]\n')
        output.write('api_key = ' + raw_input('GoDaddy API Key: ') + '\n')
        output.write('api_secret = ' + raw_input('GoDaddy API Secret: ') + '\n')
        output.close()
    return domains

root_dir = '/root/letsencrypt'
certs_path = os.path.join(root_dir, 'dehydrated-master', 'certs')
daily_command = 'dehydrated-master/dehydrated  -k godaddy.py -c'


if not os.path.exists(root_dir):
    os.makedirs(root_dir)
domain_dict = setup(root_dir)





