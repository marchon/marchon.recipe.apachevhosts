# -*- coding: utf-8 -*-
"""Recipe apachevhosts"""

from datetime import datetime
import logging
import os


default_template = """
#
#
# DO NOT MODIFY THIS BY HAND
# AUTOMATICALLY GENERATED DURING BUILDOUT
# YOUR CHANGES *WILL* BE LOST
#
# Buildout dir: %(buildout)s
# Buildout part: %(part)s
# Last update:  %(timestamp)s
#
#  listenaddress= *
#  listenport   = 80
#  serveradmin  = webmaster@yourdomain.com
#  absdir       = /http/sites/sitename
#  url          = mysite.com
#  reldir       = /http/sites/sitename
#  urlaliases   = www.mysite.com other.sitename.com www.other.sitename.com
#
#  ProxyRequets = Off
#  ProxyPath    = http://%(httpaddress)s/VirtualHostBase/http/%(url)s:80%(path)s/VirtualHostRoot/
#  ProxyPathRev = http://%(httpaddress)s/VirtualHostBase/http/%(url)s:80%(path)s/VirtualHostRoot/
#
#  script-alias
#               /cgi-bin   %(absdir)s/cgi-bin
#               /cgibin    %(absdir)s/cgibin
#               /cgitools  %(absdir)s/cgitools


Listen %(listenaddress)s:%(listenport)s
<VirtualHost %(listenaddress)s:%(listenport)s>
   ServerAdmin %(serveradmin)s
   DocumentRoot %(absdir)s/htdocs

   ServerName %(url)s
   %(urlalias)s


   ProxyRequests %(ProxyRequests)s
   <Proxy *>
     Order deny,allow
     Allow from all
   </Proxy>


   ProxyPass / %(ProxyPath)s
   ProxyPassReverse / %(ProxyPathRev)s


   ErrorLog %(reldir)s/logs/error_log
   CustomLog %(reldir)s/logs/access_log custom

   %(localscriptalias)s


   ErrorDocument 404 http://%(url)s

   <Directory %(reldir)s/htdocs>
     AddType application/x-httpd-php .php3
     Options +Includes
   </Directory>

   <Directory />
     Options FollowSymLinks
     AllowOverride None
   </Directory>

</VirtualHost>

"""


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(name)

    def install(self):
        """Installer"""
        return self.writeVhosts()

    def update(self):
        """Updater"""
        return self.writeVhosts()
        
    def writeVhosts(self):
        files = []
        vhosts = self.options['vhosts']
        httpaddress =  self.options['http-address']
        scriptalias = self.options['script-alias'] 

        prefix = self.options.get('prefix')
        postfix = self.options.get('postfix')
        template = self.options.get('template')
        outputdir = self.options.get('outputdir')

        absdir = self.options.get('absdir') 

        listenaddress= self.options.get('listenaddress') 
        listenport   = self.options.get('listenport') 
        url          = self.options.get('url') 
        serveradmin  = self.options.get('serveradmin') 
        reldir       = self.options.get('reldir') 
        ProxyRequests= self.options.get('ProxyRequests') 
        ProxyPath    = self.options.get('ProxyPath')
        ProxyPathRev = self.options.get('ProxyPathRev') 
     
        if absdir is None: 
           absdir = '%s/sitepath' % self.buildout['buildout']['directory']
        
        if listenaddress is None: 
           listenaddress = '*'
        
        if listenport is None: 
           listenport = '80'
        
        if url is None: 
           url = 'localhost' 
   
        if serveradmin is None: 
           serveradmin = 'webmaster@%s' % url

        if reldir is None: 
           reldir = absdir 

        if ProxyRequests is None: 
           ProxyRequests = 'Off'

        if ProxyPath is None: 
           ProxyPath = 'http://localhost:8000'

        if ProxyPathRev is None: 
           ProxyPathRev = 'http://localhost:8000'

#
#  script-alias
#               /cgi-bin   %(absdir)s/cgi-bin
#               /cgibin    %(absdir)s/cgibin
#               /cgitools  %(absdir)s/cgitools



        localscriptalias = '' 

        for line in scriptalias.split('\n'): 
            if len(line.split()):
               publicpath, localpath = line.split() 
               localscriptalias = localscriptalias + 'ScriptAlias /%s %s/%s\n   ' % ( publicpath, absdir, localpath ) 
                

        for line in vhosts.split('\n'):
            if len(line.split()):
        	site, path, url = line.split()
        	if prefix is not None:
        	    url = "%s.%s" % (prefix, url)
        	if postfix is not None:
        	    url = "%s.%s" % (site, postfix)
        	    
        	values = dict()
        	values['buildout'] = self.buildout['buildout']['directory']
        	values['httpaddress'] = httpaddress
        	values['site'] = site
        	values['path'] = path
        	values['url'] = url
        	values['part'] = self.name
        	values['timestamp'] = str(datetime.now())[0:16]

                values['absdir']= absdir
                values['listenaddress']= listenaddress 
                values['listenport']= listenport 
                values['url']= url 
                values['serveradmin']= serveradmin 
                values['reldir']= reldir 
                values['ProxyRequests']= ProxyRequests
                values['ProxyPath'] = ProxyPath 
                values['ProxyPathRev'] = ProxyPathRev 
                values['localscriptalias'] = localscriptalias 
                if values['serveradmin']  == 'webmaster@localhost': 
                   values['serveradmin'] = serveradmin = 'webmaster@%s' % url 
        	
        	# Provide non-'www.' alias directive
        	if url[0:4] == 'www.':
        	    values['urlalias'] = 'ServerAlias %s' % url[4:]
        	else:
        	    values['urlalias'] = ""
        	
        	# Use provided template or default
        	if template is None:
        	    template = default_template
        	filename = os.path.join(outputdir, "%s.conf" % site)
        	files.append(filename)
        	out = open(filename, "w")
        	out.write(template % values)
        	out.close()

        return files
