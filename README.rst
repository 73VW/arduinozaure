`Arduinozore`
=============

.. image:: https://travis-ci.org/S-Amiral/arduinozore.svg?branch=master
    :target: https://travis-ci.org/S-Amiral/arduinozore
    :alt: Build status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: http://doge.mit-license.org
    :alt: MIT License

.. image:: https://img.shields.io/pypi/v/Arduinozore.svg?maxAge=2592000
    :target: https://pypi.org/project/Arduinozore/
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/pyversions/Arduinozore.svg
    :target: https://pypi.org/project/Arduinozore/
    :alt: PyPI - Python Version


Realization of a web interface allowing to visualize sensors data sent by an arduino on a serial port.

This package can be installed via :code:`pip install arduinozore`.

We are still working on this README.
------------------------------------

Français
--------

L'installation est aisée. Le package se trouvant sur pypi, il suffit de l'installer via la commande

.. code-block:: bash

    pip install arduinozore

Lors du premier lancement, si aucun dossier de configuration n'est trouvé, il est créé.

**Attention** Il est nécessaire d'avoir une connexion internet pour utiliser pip et lors du premier lancement de l'application. Des fichiers doivent être téléchargés depuis internet.

Pour afficher l'aide, la commande suivante est disponible

.. code-block:: bash

    arduinozore --help
    usage: arduinozore [-h] [-hp HTTP_PORT] [-hsp HTTPS_PORT] [-a path]
                   [--newconfig]

    Arduinozore server

    optional arguments:
    -h, --help            show this help message and exit
    -hp HTTP_PORT, --http_port HTTP_PORT
                        Server http port. Default 8000
    -hsp HTTPS_PORT, --https_port HTTPS_PORT
                        Server https port. Default 8001. Used for sockets too.
    -a path, --arduino path
                        Path where arduino source code will be generated.
    --newconfig           Delete actual config and make a new one. Warning.

En cas de problème, il est possible de supprimer la configuration et la regénérer avec la commande

.. code-block:: bash

    arduinozore --newconfig

Il est possible de spécifier les ports http et https. Par défaut les ports 8000 et 8001 sont utilisés. Pour ce faire, les options suivantes sont disponibles

.. code-block:: bash

    arduinozore -hp 80 -hsp 443

Afin de récupérer le script arduino pour pouvoir le flasher, il est possible de l'obtenir avec l'option `-a` en donnant le path cible.

.. code-block:: bash

    arduinozore -a /destination/path/for/arduino/script

Pour lancer l'application, il suffit d'exécuter

.. code-block:: bash

    arduinozore

et de se rendre à l'adresse fournie dans le terminal.

**Attention**, si votre réseau domestique ne possède pas de serveur DNS, il sera nécessaire de remplacer l'adresse du serveur par son adresse IP afin de pouvoir y accéder.

Pour trouver cette adresse IP, la commande suivante suffit.

.. code-block:: bash

    ifconfig

Par exemple, si lors du lancement, la chose suivante est affichée dans la console

.. code-block:: bash

    /############################################################################################\

         #
        # #   #####  #####  #    # # #    #  ####  ######  ####  #####  ######
       #   #  #    # #    # #    # # ##   # #    #     #  #    # #    # #
      #     # #    # #    # #    # # # #  # #    #    #   #    # #    # #####
      ####### #####  #    # #    # # #  # # #    #   #    #    # #####  #
      #     # #   #  #    # #    # # #   ## #    #  #     #    # #   #  #
      #     # #    # #####   ####  # #    #  ####  ######  ####  #    # ######


    \############################################################################################/

    /############################################################################################\

                          Listening on: https://raspberry:8001

mais que vous ne possédez pas de dns, il faudra remplacer le nom "raspberry" par l'adresse IP du Raspberry Pi obtenue grâce à la commande "ifconfig".

Maintenant, il n'y a plus qu'à ouvrir un navigateur, se rendre à l'adresse correcte et effectuer quelques réglages et le tour est joué!

Tout d'abord, le navigateur risque de vous dire que le certificat n'a pas pu être vérifié. Étant donné qu'il est généré par l'application, il est autosigné. Il suffit donc de l'accepter tel quel.

Dès lors, la page d'accueil du site apparaît. Si des Arduinos sont connectés, il sont listés.

À présent, il est nécessaire de créer une configuration de carte en fonction du type d'Arduino que vous possédez. Cette création peut être atteinte dans les réglages.

Ensuite, il est nécessaire de configurer le ou les capteurs utilisés de la même manière que la ou les cartes.

Il est maintenant possible de configurer l'Arduino et d'interagir avec lui! Bravo!


English
--------

Project install is easy. This package being on Pypi, you can simply install it like this.

.. code-block:: bash

    pip install arduinozore

At first launch, if no config folder is found it is created.

**Warning** It's necessary to have an internet connection in order to use pip and at app first launch. Some files need to be downloaded.

To print help this command is available

.. code-block:: bash

    arduinozore --help
    usage: arduinozore [-h] [-hp HTTP_PORT] [-hsp HTTPS_PORT] [-a path]
                   [--newconfig]

    Arduinozore server

    optional arguments:
    -h, --help            show this help message and exit
    -hp HTTP_PORT, --http_port HTTP_PORT
                        Server http port. Default 8000
    -hsp HTTPS_PORT, --https_port HTTPS_PORT
                        Server https port. Default 8001. Used for sockets too.
    -a path, --arduino path
                        Path where arduino source code will be generated.
    --newconfig           Delete actual config and make a new one. Warning.

In case of troubles, it is possible to delete config and generate a new one with the following command

.. code-block:: bash

    arduinozore --newconfig

It is possible to specify http and https ports. By default port 8000 and 8001 are used. To do so, the following options are available.

.. code-block:: bash

    arduinozore -hp 80 -hsp 443

In order to get the Arduino script use the following command.

.. code-block:: bash

    arduinozore -a /destination/path/for/arduino/script

Then you can run the app with

.. code-block:: bash

    arduinozore

and then go to this adress provided in the terminal.

**Warning!** if your domestic network doesn't have a DNS server you will have to replace the server adress by its IP.

In order to find its IP run this command on the Raspberry Pi.

.. code-block:: bash

    ifconfig

As an example if at first start the app outputs the following

.. code-block:: bash

    /############################################################################################\

         #
        # #   #####  #####  #    # # #    #  ####  ######  ####  #####  ######
       #   #  #    # #    # #    # # ##   # #    #     #  #    # #    # #
      #     # #    # #    # #    # # # #  # #    #    #   #    # #    # #####
      ####### #####  #    # #    # # #  # # #    #   #    #    # #####  #
      #     # #   #  #    # #    # # #   ## #    #  #     #    # #   #  #
      #     # #    # #####   ####  # #    #  ####  ######  ####  #    # ######


    \############################################################################################/

    /############################################################################################\

                          Listening on: https://raspberry:8001

but you don't have dns, you'll have to substitute `raspberry` with the Raspberry Pi IP address.

Know you only have to open a browser, browse to the correct address, tweak a few settings and it's alright.

First of all, the browser will tell you that the certificate couldn't be verified. This is normal. As the certificate is generated by arduinozore, it is autosigned. You just have to accept it as is.

By now the home page has appeared. If any Arduinos are connected, they are listed.

You can know create a configuration for the Arduino according to the type of board you own. You can achieve this by going to the settings page.

You have to also configure the sensors you want to use just as you did for the board.

It is now possible to communicate with the Arduino, read its sensors and toggle its output! Well done!
