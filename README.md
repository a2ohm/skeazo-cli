# skeazo-cli

_Télécharger, nettoyer et convertir en markdown un document html_

## Installation des dépendances

- `pip install markdownify`

## Usage

**Télécharger un document depuis une url.**

- `./skeazo-cli.py download "URL"`

La destination du document dépend du système d'exploitation :

- linux : `~/.local/share/skeazo/documents/`

L'ID retourné sert ensuite à désigner le document.

**Convertir le document html en markdown**

- `./skeazo-cli.py html2md ID`

Le document html est converti en markdown grâce à la librairie python [markdownify](https://pypi.org/project/markdownify/).

**Nettoyer le document**

- `.skeazo-cli.py clean ID`

Le document markdown est nettoyé de ses scories. Pour le moment, aucun filtre n'est implémenté.