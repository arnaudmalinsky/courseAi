SUMUP_HEADER_FORMAT= [
    "Title Context",
    "Title lvl2",
    "Title lvl3",
    "concat_texts",
    "unique_index",
    "Filename",
    "Index",
    "text_sumup"
  ]

SUMUP_PROMPT = """
Le texte qui suivra ci-dessous est une longue portion de cours de droit, ta tâche est de le résumé en quelques axes principaux.
Ton résumé doit bien contenir les idées, concepts juridiques et changements historique évoqués dans ce texte.    
Attention, il ne faut pas ajouter d'idée qui ne soit pas strictement dans le texte ci-dessous.

Il est possible que le texte donné ci-dessous soit très court (moins de 100 tokens), dans ce cas, recopie le simplement.

"""