# Task Tracker CLI

Task Tracker CLI est une application en ligne de commande pour gérer vos tâches quotidiennes. Ce projet vous permet d'ajouter, de mettre à jour, de supprimer et de suivre vos tâches, le tout à partir d'une interface simple et efficace.

## Fonctionnalités

- **Ajouter des tâches** : Ajoutez de nouvelles tâches avec une description et un statut (todo, in-progress, done).
- **Mettre à jour des tâches** : Mettez à jour la description et le statut des tâches existantes.
- **Supprimer des tâches** : Supprimez des tâches que vous n'avez plus besoin de suivre.
- **Lister les tâches** : Affichez toutes les tâches ou filtrez par statut.
- **Gestion des dates** : Chaque tâche a une date de création et de mise à jour.

## Prérequis

- Python 3.x
- Aucun module externe n'est requis.

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/hans241/Tache-Tracker.git
   cd Tache-Tracker

## Utilisation

L'application s'exécute a partir de la ligne de commande. Voici quelques commandes utiles:

- **Ajouter une nouvelle tâche** :
  ```bash
  python task_tracker.py add "Le_nom_de_la_tache" --status todo
  
- **Mettre à jour une tâche** :
  ```bash
  python task_tracker.py update 1 "Le_nom_de_la_tache_Modifier" --status in-progress

- **Supprimer une tâche** :
  ```bash
  python task_tracker.py delete 1
  
- **Lister toutes les tâches** :
  ```bash
   python task_tracker.py list
  
- **Lister les tâches par statut** :
  ```bash
   python task_tracker.py list todo
   python task_tracker.py list done
   python task_tracker.py list in-progress

## Contribuer
Si vous souhaitez contribuer au projet, n'hésitez pas à soumettre une demande de tirage (pull request). Toutes les contributions sont les bienvenues !

