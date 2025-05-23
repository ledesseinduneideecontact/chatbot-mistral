import os
import sys

# Ajouter le répertoire courant au path Python
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
from main import app

# Charger les variables d'environnement
load_dotenv()

# Configuration pour Passenger sur O2Switch
INTERP = "/usr/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Application WSGI
application = app 