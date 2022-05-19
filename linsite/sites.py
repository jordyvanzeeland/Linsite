from django.shortcuts import redirect
import os

class Sites:

    #-------------------------------------------------------------------------------
    # WARNING: Because of root permissions on folder /etc/apache2/sites-available 
    #          ownership is temporarely switcht
    #          After all commands are done the folder ownership will be root again.
    # ------------------------------------------------------------------------------

    def __init__(self, hostname):
        self.hostname = hostname
    
    #------------------------------------------------------------ 
    # Add folder to /var/www and set ownership to current user
    # Also setting the folder to 755 for current user
    # -----------------------------------------------------------

    def addFTPFolder(self):
        cmd = "sudo mkdir /var/www/{0}".format(self.hostname)
        os.system(cmd)

        cmd = "sudo chown webdev:webdev /var/www/{0}".format(self.hostname)
        os.system(cmd)

        cmd = "sudo chmod -R 755 /var/www/{0}".format(self.hostname)
        os.system(cmd)

    #------------------------------------------------------------ 
    # Delete folder from /var/www
    # -----------------------------------------------------------

    def removeFTPFolder(self):
        cmd = "sudo rm -d /var/www/{0}".format(self.hostname)
        os.system(cmd)

    #------------------------------------------------------------ 
    # Add a .conf file with hostname to /etc/apache2/sites-available
    # -----------------------------------------------------------

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

    #------------------------------------------------------------ 
    # Delete a .conf file from /etc/apache2/sites-available
    # -----------------------------------------------------------

    def removeConfFile(self):
        cmd = "sudo rm /etc/apache2/sites-available/{0}.conf".format(self.hostname)
        os.system(cmd)

    #------------------------------------------------------------ 
    # Enable the new hostname
    # -----------------------------------------------------------
    
    def enableHost(self):
        cmd = "sudo a2ensite {0}.conf".format(self.hostname)
        os.system(cmd)

    #------------------------------------------------------------ 
    # Disable specific hostname
    # -----------------------------------------------------------

    def disableHost(self):
        cmd = "sudo a2dissite {0}.conf".format(self.hostname)
        os.system(cmd)

    #------------------------------------------------------------ 
    # Apply changes and restart apache
    # -----------------------------------------------------------

    def restartApache(self):
        cmd = "sudo systemctl restart apache2"
        os.system(cmd)

    #------------------------------------------------------------ 
    # App function that will create a new hostname
    # -----------------------------------------------------------

    def addSite(self):
        os.system("sudo chown -R webdev:webdev /etc/apache2/sites-available")

        self.addFTPFolder()
        self.addConfFile()
        self.enableHost()
        self.restartApache()

        os.system("sudo chown -R root:root /etc/apache2/sites-available")
        return redirect("/")

    #------------------------------------------------------------ 
    # App function that will delete a hostname
    # -----------------------------------------------------------

    def deleteSite(self):

        os.system("sudo chown -R webdev:webdev /etc/apache2/sites-available")
        
        self.disableHost()
        self.removeConfFile()
        self.removeFTPFolder()
        self.restartApache()

        os.system("sudo chown -R root:root /etc/apache2/sites-available")
        return redirect("/")