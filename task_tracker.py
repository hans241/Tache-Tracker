import sys  # Module pour interagir avec les arguments passés via la ligne de commande
import json  # Module pour manipuler les fichiers JSON, utile pour sauvegarder les tâches
import os  # Module pour les opérations sur les fichiers, utilisé ici pour vérifier l'existence du fichier JSON
from datetime import datetime  # Module pour manipuler les dates et heures, utile pour enregistrer les timestamps


# Chemin du fichier JSON où les tâches seront stockées
TASKS_FILE = 'tasks.json'

# Vérifie si le fichier JSON existe, sinon, il le crée avec une liste vide
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w') as file:
        json.dump([],file)


# Fonction pour lire les tâches depuis le fichier JSON
def read_tasks():
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)  # Charge et retourne les tâches sous forme de liste de dictionnaires


# Fonction pour écrire des tâches dans le fichier JSON
def write_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file,indent=4)  # Sauvegarde les tâches dans le fichier avec une indentation pour la lisibilité


# Fonction pour générer un nouvel ID pour une tâche
# Prend la liste des tâches, retourne l'ID le plus grand + 1, ou 1 s'il n'y a aucune tâche
def generate_task_id(tasks):
    if tasks:
        return max(task['id'] for task in tasks) + 1
    return 1


# Fonction pour ajouter une tâche avec nom, description et statut
def add_task(name, description=None, status='todo'):
    # Vérifie que le nom de la tâche est fourni
    if not name:
        print("Veuillez fournir un nom pour la tâche.")
        return

    tasks = read_tasks()  # Lit les tâches actuelles
    new_task = {
        'id': generate_task_id(tasks),  # Génère un ID unique pour la nouvelle tâche
        'name': name,  # Le nom de la tâche est obligatoire
        'description': ' '.join(description) if description else "Aucune description",  # Description optionnelle
        'status': status,  # Statut de la tâche (par défaut: 'todo')
        'createdAt': datetime.now().isoformat(),  # Timestamp de création
        'updatedAt': datetime.now().isoformat()  # Timestamp de dernière mise à jour
    }
    tasks.append(new_task)  # Ajoute la nouvelle tâche à la liste
    write_tasks(tasks)  # Sauvegarde la liste mise à jour dans le fichier JSON
    print(f"Tâche ajoutée avec succès (ID: {new_task['id']}) avec le statut '{status}'.")


# Fonction pour mettre à jour une tâche (nom, description et statut)
def update_task(task_id, new_name=None, new_description=None, new_status=None):
    tasks = read_tasks()  # Charge les tâches actuelles
    task_found = False  # Flag pour vérifier si la tâche existe

    # Parcourt la liste des tâches pour trouver celle avec le bon ID
    for task in tasks:
        if task['id'] == task_id:
            # Met à jour le nom si un nouveau nom est fourni
            if new_name:
                task['name'] = new_name
            # Met à jour la description si une nouvelle description est fournie
            if new_description:
                task['description'] = new_description
            # Met à jour le statut si un nouveau statut valide est fourni
            if new_status and new_status in ['todo', 'in-progress', 'done']:
                task['status'] = new_status
            # Met à jour le timestamp de dernière modification
            task['updatedAt'] = datetime.now().isoformat()
            task_found = True  # Marque la tâche comme trouvée
            break

    # Sauvegarde les modifications si la tâche a été trouvée
    if task_found:
        write_tasks(tasks)
        print(f"Tâche {task_id} mise à jour avec succès.")
    else:
        print(f"Aucune tâche trouvée avec l'ID {task_id}.")


# Fonction pour supprimer une tâche
def delete_task(task_id):
    tasks = read_tasks()  # Charge les tâches actuelles
    # Supprime la tâche avec l'ID correspondant
    tasks = [task for task in tasks if task['id'] != task_id]

    write_tasks(tasks)  # Sauvegarde la liste des tâches mise à jour
    print(f"Tâche {task_id} supprimée avec succès.")


# Fonction pour changer le statut d'une tâche (marque comme 'todo', 'in-progress' ou 'done')
def change_task_status(task_id, new_status):
    tasks = read_tasks()  # Charge les tâches actuelles
    task_found = False  # Flag pour vérifier si la tâche existe

    # Parcourt la liste des tâches pour trouver celle avec le bon ID
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status  # Met à jour le statut
            task['updatedAt'] = datetime.now().isoformat()  # Met à jour le timestamp
            task_found = True  # Marque la tâche comme trouvée
            break

    # Sauvegarde les modifications si la tâche a été trouvée
    if task_found:
        write_tasks(tasks)
        print(f"Tâche {task_id} mise à jour au statut: {new_status}.")
    else:
        print(f"Aucune tâche trouvée avec l'ID {task_id}.")


# Fonction pour lister les tâches, avec la possibilité de filtrer par statut
def list_tasks(status=None):
    tasks = read_tasks()  # Charge les tâches actuelles
    if status:
        tasks = [task for task in tasks if task['status'] == status]  # Filtre les tâches par statut

    # Affiche les tâches ou un message si aucune tâche n'est trouvée
    if not tasks:
        print("Aucune tâche trouvée.")
    else:
        for task in tasks:
            print(f"[{task['id']}] {task['name']} - {task['description']} - {task['status']} "
                  f"(Créé le: {task['createdAt']}, Mis à jour: {task['updatedAt']})")


# Fonction pour afficher un message d'aide sur les commandes disponibles
def show_help():
    print("""
Usage: task-cli [command] [arguments] 

Commands:
  add [name] [description optionnel] [status optionnel]  Ajouter une nouvelle tâche avec un nom, description et/ou un statut
  update [id] [name optionnel] [description optionnel] [status optionnel]  Mettre à jour une tâche existante
  delete [id]                   Supprimer une tâche
  mark-in-progress [id]         Marquer une tâche comme en cours
  mark-done [id]                Marquer une tâche comme effectuée
  list                          Lister toutes les tâches
  list [status]                 Lister les tâches par statut (todo, in-progress, done)
    """)


# Fonction principale qui analyse les arguments de la ligne de commande et exécute la commande appropriée
def main():
    if len(sys.argv) < 2:
        show_help()  # Si aucune commande n'est passée, affiche l'aide
        return

    command = sys.argv[1]  # La commande est le deuxième argument de la ligne de commande

    # Ajoute une nouvelle tâche
    if command == 'add':
        if len(sys.argv) < 3:
            print("Usage: task-cli add [name] [description optionnel] [status optionnel]")
            return
        name = sys.argv[2]  # Le nom de la tâche
        description = sys.argv[3:-1] if sys.argv[-1] in ['todo', 'in-progress', 'done'] else sys.argv[
                                                                                             3:]  # Description optionnelle
        status = sys.argv[-1] if sys.argv[-1] in ['todo', 'in-progress', 'done'] else 'todo'  # Statut optionnel
        add_task(name, description, status)

    # Met à jour une tâche existante
    elif command == 'update':
        if len(sys.argv) < 3:
            print("Usage: task-cli update [id] [name optionnel] [description optionnel] [status optionnel]")
            return
        task_id = int(sys.argv[2])
        name = sys.argv[3] if len(sys.argv) > 3 else None
        description = ' '.join(sys.argv[4:-1]) if sys.argv[-1] in ['todo', 'in-progress', 'done'] else ' '.join(
            sys.argv[4:])
        status = sys.argv[-1] if sys.argv[-1] in ['todo', 'in-progress', 'done'] else None
        update_task(task_id, name if name else None, description if description else None, status)

    # Supprime une tâche
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Usage: task-cli delete [id]")
            return
        task_id = int(sys.argv[2])
        delete_task(task_id)

    # Marque une tâche comme "en cours"
    elif command == 'mark-in-progress':
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-in-progress [id]")
            return
        task_id = int(sys.argv[2])
        change_task_status(task_id, 'in-progress')

    # Marque une tâche comme "terminée"
    elif command == 'mark-done':
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-done [id]")
            return
        task_id = int(sys.argv[2])
        change_task_status(task_id, 'done')

    # Liste les tâches (avec ou sans filtrage par statut)
    elif command == 'list':
        if len(sys.argv) > 2:
            status = sys.argv[2]
            list_tasks(status)
        else:
            list_tasks()

    # Si la commande n'est pas reconnue, affiche l'aide
    else:
        print("Commande non reconnue.")
        show_help()


# Si le script est exécuté directement, appelle la fonction main
if __name__ == '__main__':
    main()
