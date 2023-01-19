# BotdePomme
## Description
Ce bot a pour objectif de lire des musiques via YouTube, il propose également quelques commandes de jeux (pendu, pile ou face) et des commandes admin.  

## Commandes :  
Voici la liste des commandes disponibles pour ce bot :

### Pour la musique :
`!play [lien YouTube]` : permet de lancer la lecture d'une vidéo YouTube sur le canal vocal où se trouve l'utilisateur qui a lancé la commande. Si d'autres vidéos sont déjà en file d'attente, elles seront jouées à la suite. La recherche par mot clé est active ! (ex: !play Requiem of Silence)    
`!skip` : permet de passer à la vidéo suivante dans la file d'attente.  
`!stop` : permet de mettre fin à la lecture en cours et de quitter le canal vocal.  
`!leave` : permet de se déconnecter du canal vocal actuel.  
`!pause` : permet de mettre en pause la musique en cours de lecture.  
`!resume` : permet de reprendre la musique mis en pause.  
<br>

### Pour les jeux :  

`!pendu` : permet de jouer au jeu du pendu via une liste de mot prédéfini dans le code.  
`!pof` : permet de jouer au pile ou face (notion d'égalité incluse).  
<br>

### Pour l'administration :   
`!del [nbr]` : permet de supprimer un nombre de messages choisis.  
<br>

## Installation  
1. Créer votre bot sur le portail dev de Discord ([ici](https://discord.com/developers/docs/intro))  
2. Installer les requirements (`pip install -r requirements.txt`)(**Ne tapez jamais une commande sans en comprendre les conséquences potentielles, cela pourrait être dangereux.**)  
3. Remplacer "your token here" par votre token de bot (dans le fichier config qui est lui même dans le dossier config)  
4. Executer `botdepomme.py`  
5. Et voilà, have fun !

*Bien que ça paraisse logique, installer Python si ce n'est pas déjà fait.*


## Liens
Lien vers Discord developer portal : https://discord.com/developers/docs/intro *(n'hésitez pas à vous renseigner sur internet pour créer votre bot)*  
<br>

### Informations supplémentaires
- Ce bot est encore en développement et de nouvelles fonctionnalités seront peut-être ajoutées.  
- Ce bot n'est pas capable de lire de playlist (il ne va pas crash, mais il ne fera plus rien si vous lui faites la demande d'une playlist)  
- Ce bot est un peu capricieux, en cas de soucis un redemarrage et tout repart (il lui arrive de ne pas se lancer lors de la première commande, ça reste rare mais vous êtes avertis :) )
