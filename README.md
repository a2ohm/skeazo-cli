# skeazo-cli

_Télécharger, nettoyer et convertir en markdown un document html_

## Mettre en place l'environnement virtuel python.

Pour faire fonctionner Skeazo, vous devez installer plusieurs librairies python. Pour qu'elles n'interfèrent pas avec le reste de votre système, nous allons mettre en place un environnement virtuel python.

Si besoin, installez `python3-venv`.

* `sudo apt install python3-venv`

Dans le dossier contenant le code source de Skeazo, créez l'environnement virtuel et basculez dedans.

* `cd skeazo-cli`
* `python3 -m venv .venv`
* `source .venv/bin/activate`

**Remarque.** En fonction de votre shell, peut-être devrez-vous utiliser `source .venv/bin/activate.csh` ou `source .venv/bin/activate.fish`.

Pour indiquer que vous êtes maintenant dans l'environnement virtuel, vous devez lire `(.venv)` devant l'invite de commande de votre terminal.

**Remarque.** Pour sortir de l'environnement virtuel, il suffit de lancer la commande `deactivate`.

Mettez à jour les paquets de base.

* `pip3 install --upgrade pip`
* `pip3 install --upgrade setuptools`

## Installation des dépendances

- `pip install PyGObject`
- `pip install markdownify`
- `pip install requets`
- `pip install pyyaml`

## Usage

**Télécharger un document depuis une url.**

- `python3 skeazo-cli.py download "URL"`

La destination du document dépend du système d'exploitation :

- linux : `~/.local/share/skeazo/documents/`

L'ID retourné sert ensuite à désigner le document.

**Convertir le document html en markdown**

- `python3 skeazo-cli.py html2md ID`

Le document html est converti en markdown grâce à la librairie python [markdownify](https://pypi.org/project/markdownify/).

**Nettoyer le document**

- `python3 skeazo-cli.py clean ID`

Le document markdown est nettoyé de ses scories. Pour le moment, aucun filtre n'est implémenté.