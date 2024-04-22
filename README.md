# Api de gestion de rendez-vous professionnel

MeetMate est une application de gestion de vos rendez-vous professionnelle. il intègre plusieurs fonctionnalité. le gestion des utilisateurs, la possibilité de créer des équipes et une gestion efficace des rendez-vous. Pour l’environement de développement nous utilisons Docker pour en autre simuler notre serveur mail

## prérequis
 avant de pouvoir démarrer l’api , assurez vous d’avoir ces prérequis:
- docker et docker compose
- avoir une connection internet pour télécharger les images nécessaire.

## Installation

- naviguer jusqu’au dossier FAST_API_GESTION
- entrer dans le dossier FAST_API_GESTION

## Contenerisation
taper la commande *docker compose -f docker_compose_api_dev build*
taper la commande *docker compose -f docker_compose_api_dev up*
après ça votre application sera démarrer 


## Démarrage
aller à l’adresse [localhost:8000/docs](localhost:8000/docs) pour l’interface de test de l’api
aller à l’adresse [localhost:8025/](localhost:8025/) pour notre serveur mail de test qui nous permet de tester et recevoir les emails
aller à l’adresse [localhost:8080/](localhost:8080/) pour le gestionnaire de base de données le nom d’utilisateur est root et le mot de passe the_man_him_self **(ceci doit etre modifier en environement de production)**
## Fonctionnalités
### Gestion des utilisateurs

- creation des utilisateur
- verification des utilisateur par email
- la modification des informations de l’utilisateur
- la supression de l’utilisateur
- la connection avec token
- la déconnection

### Gestion des équipes
- creation d’équipe
- ajoute de membres dans une équipe
- modification des informations d’une équipe
- supression d’une équipe

### Gestion des rendez-vous
- creation de rendez-vous personnel
- modification de rendez-vous personnel
- supression de rendez-vous personnel
- creation de rendez-vous pour une équipe
- modification des rendez vous d’un groupe
- supression des rendez vous d’groupe
- la possibilité pour l’utilisateur de consulter ces rendez vous et ceux des équipes dont il est membre
- consulter les rendez-vous d’une équipe
- avoir plus d’information concernant un rendez-vous particulier d’une équipe


 


