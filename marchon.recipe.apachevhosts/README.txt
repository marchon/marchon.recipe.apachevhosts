.. contents::


          Summary: buildout recipe that writes apache.conf virtual hosts
        
          This is work derived from the work of: juan@grigera.com.ar

          THANK YOU JUAN - You can see Juans other work at - www.gcommons.org  

          I forked this project and separated out the content from the gcommons because 
          I wanted a separate package with just the apache-virtualhost configurations

          *** AND *** 

          the original work made a lot of assumptions about how you wanted the configuration
          and template files and the documentation was sparse 

          I started this as a documentation contribution - and made so many changes to the 
          templates - I thought I should break it out. 
  
        


        Getting Started 
        Sample Local buildout file
        
        --------------------------------------------------------------------------------------------
        [buildout] 
        develop = . 
        parts= makesitedirs apache 
        http-address = 127.0.0.1:8080
        
        
        [makesitedirs]
        recipe = z3c.recipe.mkdir
        paths = foo/bar
                /darkmatter/site
                /journalcommons/site
                /historicalmaterialism/site
                ./parts/apache/conf.d/
                
        
        
        
        [apache]
        recipe = marchon.recipe.apachevhosts
        http-address = ${buildout:http-address}
        postfix = test.gcommons.org
        outputdir = parts/apache/conf.d/
        vhosts =
                darkmatter /darkmatter/site www.darkmatter.info
                journalcommons /journalcommons/site www.gcommons.org
                historicalmaterialism /historicalmaterialism/site www.historicalmaterialism.org
        
        
        --------------------------------------------------------------------------------------------
        
        
        REQUIRED VARIABLES:

           vhosts = 
                   shorthostname path fullhostname 

           http-address = 127.0.0.1:8080

           script-alias = 
                          /cgibin ./cgibin
                          /cgi-bin ./cgi-bin

        OPTIONAL VARIABLES: 

           prefix        = hostid 
           postfix       = test.yourdomain.net 
           template      =  
           outputdir     = parts/apache/conf.d/ 

        OPTIONAL VARIABLES - with default values: 

           absdir = '%s/sitepath' % self.buildout['buildout']['directory']
           listenaddress = '*'
           listenport = '80'
           url = 'localhost'
           serveradmin = 'webmaster@%s' % url
           reldir = absdir
           ProxyRequests = 'Off'
           ProxyPath = 'http://localhost:8000'


