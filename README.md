# Système de Billetterie pour la Foire

Une application web simple pour gérer la vente de tickets pour une foire, développée avec Flask.

## Fonctionnalités

- Vente de tickets
- Génération de reçus imprimables
- Statistiques de vente
- Interface utilisateur intuitive

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-username/foire-tickets.git
cd foire-tickets
```

2. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur Unix ou MacOS
source venv/bin/activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

L'application utilise SQLite comme base de données. Le fichier de base de données sera automatiquement créé dans le dossier `instance` lors du premier démarrage.

## Démarrage

Pour lancer l'application :
```bash
python app.py
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8080`

## Utilisation

1. Page d'accueil : Affiche les tickets disponibles et permet la vente
2. Page de statistiques : Montre les statistiques de vente
3. Après une vente, un reçu est généré et peut être imprimé

## Licence

Ce projet est sous licence MIT.
