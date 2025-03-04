PROMPT = """
Le texte qui suivra ces instructions est une retranscription d'un cours juridique donné à l'oral.
Ton rôle est de reprendre le texte pour effectuer plusieurs tâches de nettoyage, sans ommetre aucune information, sans rien ajouter en plus du texte.
Il est possible que le texte contienne très peu de caractères (moins de 100), si c'est le cas recopie le à l'identique.

Les manipulations à faire sur le texte : 
- Améliorer la mise en page de ce texte,
- Créer des paragraphes et des phrases plus claires, 
- Mettre en italique les termes en langue étrangère seulement, 
- Convertir les nombres en chiffres, 
- Améliorer la présentation des concepts juridiques importants, mais en gardant tout le contenu.

Les contraintes que tu dois respecter :
- Ne pas utiliser trop de puces avec énumération,
- Ne pas créer de nouveaux titres que ceux mentionnés,
- Ne rien ajouter en plus du texte d'origine,
- Ne pas modifier la police du texte à part les mises en italique pour les mots étrangers,
- Conserver toutes les informations du texte initiale,
- Conserver le vocabulaire du texte d'origine (ex : les verbes comme 'disposer' et 'stipuler') même si cela créer une répétition,
- Conserver les exemples et cas particuliers (espèce) donnés par le professeur pour illustrer un concept juridique. 

Voici le texte : 

----

"""