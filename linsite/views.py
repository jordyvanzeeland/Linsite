from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os

@login_required
def index(request):

    hosts = os.listdir("/etc/apache2/sites-available/")
    hostsArray = []
    ftpdir = ''
    configfile = ''

    for host in hosts:
        hostenabled = 0
        # Get active site
        for root, subdirs, files in os.walk('/etc/apache2/sites-enabled/'):
            for file in files:
                
                if file == host:
                    hostenabled = 1
                else:
                    hostenabled = 0

        hostname = host.split('.conf')[0]

        # Get FTP folder
        for root, subdirs, files in os.walk('/var/www/'):
            for dir in subdirs:
                
                if dir == hostname:
                    print(dir, hostname)
                    ftpdir = os.path.join(root, dir)

        # Get config file
        for root, subdirs, files in os.walk('/etc/apache2/sites-available/'):
            for file in files:
                if file == host:
                    configfile = os.path.join(root, file)

        

        hostsArray.append({
            'hostname': hostname,
            'hostconf': configfile,
            'ftpdir': ftpdir,
            'hostactive': hostenabled
        })

    context = {
        'hosts': hostsArray
    }
    return render(request, "index.html", context)