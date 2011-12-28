.. contents::



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




