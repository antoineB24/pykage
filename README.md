# **pykage** : mon packager manager en python


example :
```properties 
pykage init # créer un pkg.toml
pykage install # installe les dependenses de pkg.toml
pykage install nom_du_module # installe avec pip et ajoute comme depensie nom_du_module dans pkg.toml
pykage run # executer le fichier python donné dans pkg.toml(DEFAULT_FILE)
pykage run nom_du_fichier # execute le fichier python dans pkg.toml(LIST_FILE)
pykage add nom_du_fichier # ajoute un fichier dans pkg.toml(LIST_FILE)
pykage settings nom_du_settings nouvelle_valeur # ajoute/modifie une setting dans pkg.py
pykage remove nom_du_fichier # supprime un fichier dans pkg.toml(LIST_FILE)
pykage env nom_de_env # créer un environement avec les depensies installé dans pkg.toml
pykage activate # active l'env si l'env existe
pykage deactivate # desactive l'env si il est activé
```
