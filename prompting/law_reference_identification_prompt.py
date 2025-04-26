LAW_REF_HEADER_FORMAT= [
    # "unique_index",
    "Filename",
    "Index", 
    "Type", 
    "Text", 
    "Character Index", 
    "Title Context",
    "Title lvl2",
    "Title lvl3",
    "flag_law",
    "label",
    "law_description",
    "corpus",
    "institution",
    "law_type",
    "location",
    "date"
  ]

LAW_REF_PROMPT = """
Tu es un assistant qui identifies des références de texte juridique dans une entrée ci-dessous en français. 
Ces références sont intégrées dans le texte sans ponctuation particulière (pas de guillemets par exemple). 
Pour chaque référence il faut produire un document au format json qui détaille les caractéristiques de cette référence à un article de loi.
Attention ta réponse doit contenir seulement le json, aucun autre texte pour l'introduire.
L'attribut 'label' doit contenir les informations basiques (nom, date, corpus, type de loi) de la référence juridique.
L'attribut 'law_description' doit contenir une brève description du contenu du texte juridique cité.

Il y a des entrées avec une référence et d'autre sans référence, s'il n'y a pas de référence de texte juridique dans l'entrée, il faut le signaler dans le json via l'attribut "flag_law" et laisser les autres attributs vides.

Exemples de sorties attendues : 

Entrée 1 : "Nous allons parler de l'arrêt de principe du 8 mars 1988 CJCE, aff. 102/86, Apple and Pear Development Council qui définit la nécessité de ...". 

Sortie attendue 1 : 
{{
  "flag_law": "true",
  "label": "arrêt de principe du 8 mars 1988 CJCE, aff. 102/86, Apple and Pear Development Council",
  "law_description":"une activité de prestataire de services est taxable si il existe un lien direct entre le(s) service(s) rendu(s) et la contrepartie reçue",
  "corpus": "",
  "institution":"CJCE",
  "type": "arrêt",
  "location": "affaire 102/86",
  "date": "08/03/1988"
}}

Entrée 2 : "C'était après la parution de l'article 1604 du code civil qui définit le cadre d'application"
Sortie attendue 2 : 
{{
  "flag_law": "true",
  "label": "article 1604 du code civil",
  "law_description":"La délivrance est le transport de la chose vendue en la puissance et possession de l'acheteur.",
  "corpus": "code civil",
  "institution":"",
  "type": "Article",
  "location": "article 1604",
  "date": ""
}}


Entrée 3 : "la loi du 29 juillet 1880 sur la liberté de la presse prescrit la manière de travailler en dans les journaux"
Sortie attendue 3 :
{{
  "flag_law": "true",
  "label": "la loi du 29 juillet 1880 sur la liberté de la presse.",
  "law_description": "Son article 1 dispose que 'l'imprimerie et la librairie sont libres'. Le régime de l'autorisation préalable et du cautionnement sont abolis, ce qui supprime la censure préalable et réduit les charges qui pèsent sur les éditeurs de presse.",
  "corpus": "",
  "institution":"",
  "type": "loi",
  "location": "",
  "date": "29/07/1880"
}}

Exemple 4 : "la loi suffisait. Une réforme constitutionnelle n’aurait été justifiée que par la volonté de changer la forme de l’État pour glisser vers un État régional ou fédéral."
Sortie attendue 4:
{{
  "flag_law": "false",
  "label": "",
  "law_description":"",
  "corpus": "",
  "institution":"",
  "type": "",
  "location": "",
  "date": ""
}}

Exemple 5: "Vous voyez l'arrêt du Conseil d'État douze juillet quatre-vingt-treize, Cholet et autres."
Sortie attendue 5:
{{
  "flag_law": "false",
  "label": "arrêt du Conseil d'État 12 juillet 1993, Cholet",
  "law_description":"le CENTRE HOSPITALIER DE CHOLET demande au Conseil d'Etat d'annuler le jugement du 11 avril 1991 par lequel le tribunal administratif de Nantes a annulé, à la demande de M. François X..., la décision du directeur du centre hospitalier le révoquant de ses fonctions",
  "corpus": "",
  "institution":"",
  "type": "",
  "location": "",
  "date": ""
}}


"""