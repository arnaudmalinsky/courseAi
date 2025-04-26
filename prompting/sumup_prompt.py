SUMUP_HEADER_FORMAT= [
    "Title Context",
    "Title lvl2",
    "Title lvl3",
    "concat_texts",
    "Folder",
    "Filename",
    "Index",
    "text_sumup"
  ]

SUMUP_PROMPT_OLD = """
Le texte qui suivra ci-dessous est une longue portion de cours de droit, ta tâche est de le résumer en quelques axes principaux.
Ton résumé doit bien contenir les idées, concepts juridiques et changements historique évoqués dans ce texte.    
Attention, il ne faut pas ajouter d'idée qui ne soit pas strictement dans le texte ci-dessous.

Il est possible que le texte donné ci-dessous soit très court (moins de 100 tokens), dans ce cas, recopie le simplement.

"""

SUMUP_PROMPT_OLD2 = """
Le texte qui suivra ci-dessous est une longue portion de cours de droit.
Peux-tu faire une fiche complète d'apprentissage de ce cours avec :
- tous les concepts essentiels,
- les citations précises des décisions et des lois,
- en décrivant le contenu des décisions et des lois.

Le format de restitution doit être court, résumé en 'bullet point' synthétique.
Ne pas faire de phrases longues.

Il est possible que le texte donné ci-dessous soit très court (moins de 100 tokens), dans ce cas, recopie le simplement.
"""

SUMUP_PROMPT = """
Le texte qui suivra ci-dessous est une longue portion de cours de droit.
Ton rôle est de le transformer dans un format de fiche de révision pour passer un examen.
Il faut utilser des 'bullet points' et être très synthétique.

Il contient des références juridiques, des concepts, du contenu.
Tu dois résumer ce texte en listant quelques idées saillantes à retenir.
Pour chaque idée, il faut:
- une description synthétique du contenu,
- décrire les références juridiques qui l'appuie,
- si besoin écrire un mémo des choses à retenir pour l'idée.

Il est possible que le texte donné ci-dessous soit très court (moins de 100 tokens), dans ce cas, recopie le simplement.
Ne pas ajouter d'idée ou concept absents du texte d'origine
"""