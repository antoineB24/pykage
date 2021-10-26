# **pykag** : l'équivalent de npm(js) en python

1.  une copy de npm
2.  au lieu de package.json il y a pkg.py

example :
```properties 
pykg init #créer un pkg.py 
pykg install #installe les dependenses de pkg.py
pykg install nom_du_module #installe avec pip et ajoute comme depensie nom_du_module dans pkg.py
pykg run #executer le fichier python donné dans pkg.py(DEFAULT_FILE)
pykg run nom_du_fichier #execute le fichier python dans pkg.py(LIST_FILE)
pykg add nom_du_fichier #ajoute un fichier dans pkg.py(LIST_FILE)
pykg settings nom_du_settings nouvelle_valeur #ajoute/modifie une setting dans pkg.py
pykg remove nom_du_fichier #supprime un fichier dans pkg.py(LIST_FILE)
pykg env nom_de_env #créer un environement avec les depensies installé dans pkg.py
pykg activate #active l'env si l'env existe
pykg deactivate #desactive l'env si il est activé
```
