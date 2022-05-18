from django.shortcuts import redirect
import os

class Sites:

    def __init__(self, hostname):
        self.hostname = hostname

    def addFTPFolder(self):
        cmd = "sudo mkdir /var/www/{0}".format(self.hostname)
        os.system(cmd)

        cmd = "sudo chown webdev:webdev /var/www/{0}".format(self.hostname)
        os.system(cmd)

        cmd = "sudo chmod -R 755 /var/www/{0}".format(self.hostname)
        os.system(cmd)

    def addConfFile(self):
        filename = '/etc/apache2/sites-available/{0}.conf'.format(self.hostname)
        filecontent = """<VirtualHost *:80>\r\n
                        ServerAdmin webmaster@localhost\r\n
                        ServerName {0}.local\r\n
                        DocumentRoot /var/www/{0}\r\n
                        ErrorLog /var/log/apache2/{0}_error.log\r\n
                        CustomLog /var/log/apache2/{0}_access.log combined\r\n
                        </VirtualHost>""".format(self.hostname)
        f =  open(filename, 'w')

        f.write(filecontent)
        f.close()
    
    def enableHost(self):
        cmd = "sudo a2ensite {0}.conf".format(self.hostname)
        os.system(cmd)

    def disableHost(self):
        cmd = "sudo a2dissite {0}.conf".format(self.hostname)
        os.system(cmd)

    def restartApache(self):
        cmd = "sudo systemctl restart apache2"
        os.system(cmd)

    # def insertHost(self):
    #     cmd = "hostsman -i {0}.local".format(self.hostname)
    #     os.system(cmd)

    def addSite(self):
        os.system("sudo chown -R webdev:webdev /etc/apache2/sites-available")

        self.addFTPFolder()
        self.addConfFile()
        self.enableHost()
        self.restartApache()

        os.system("sudo chown -R root:root /etc/apache2/sites-available")
        return redirect("/")