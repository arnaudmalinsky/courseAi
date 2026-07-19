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

CHAPTER_SUMMARY_PROMPT = """
À partir du fichier que je viens de t’envoyer, réalise une *fiche de révision synthétique, efficace, précise et suffisamment détaillée*, en réduisant le volume du document original **d’au moins 50 %**.

Respecte impérativement les consignes suivantes :

*1. Structure du document*

Reprends *tous les titres et sous-titres du document, sans aucune exception*, en conservant :

* leur *intitulé exact*, sans aucune modification ni reformulation ;
* leur *ordre exact* ;
* leur *niveau hiérarchique*.

Ne crée *aucun titre ou sous-titre supplémentaire* qui n’existe pas dans le document.

*2. Contenu à conserver*

Au sein de chaque partie, sélectionne uniquement les éléments indispensables à la compréhension et à la révision du cours :

* les *règles et idées juridiques principales* ;
* les *concepts juridiques essentiels, à mettre en **gras* ;
* les *articles, lois, décrets et autres normes juridiques* directement associés à ces règles, avec une présentation très synthétique de leur contenu ;
* les *circulaires, recommandations et autres actes de soft law* lorsqu’ils sont importants pour comprendre la règle étudiée ;
* les *jurisprudences les plus importantes, uniquement lorsqu’elles illustrent, consacrent, précisent ou font évoluer une règle juridique essentielle. Pour chaque jurisprudence retenue, indique brièvement sa **portée*.

Ne crée pas de parties séparées consacrées aux normes et à la jurisprudence : *intègre chaque article, norme ou jurisprudence directement après l’idée juridique à laquelle il se rattache*, en respectant strictement l’ordre du développement du document.

*3. Travail de synthèse*

L’objectif est d’obtenir une véritable *fiche de révision*, et non une simple reprise raccourcie du document.

Supprime :

* les répétitions ;
* les exemples secondaires ;
* les jurisprudences redondantes ou purement illustratives ;
* les développements historiques non indispensables ;
* les précisions doctrinales secondaires ;
* les longues explications lorsqu’une formulation juridique plus concise suffit.

En revanche, ne supprime aucune information nécessaire pour comprendre :

* une règle juridique essentielle ;
* ses conditions d’application ;
* ses exceptions principales ;
* sa sanction ;
* la portée d’une jurisprudence majeure.

Lorsqu'une même règle est répétée plusieurs fois dans le document, ne la développe qu'à l'endroit où elle est principalement étudiée.

*4. Mise en forme*

Organise le contenu principalement sous forme de *paragraphes courts et synthétiques*.

N’écris jamais « Idée principale », « Jurisprudence », « Portée » ou « Norme juridique » comme catégories séparées : intègre naturellement ces informations dans le développement.

Conserve les *tirets et bullet points uniquement lorsqu’ils existent déjà dans le document source*. N’ajoute aucun nouveau tiret ni aucune nouvelle bullet point.

N’ajoute :

* aucun emoji ;
* aucun trait ou séparateur entre les paragraphes ;
* aucun tableau ;
* aucune information juridique extérieure au document.

*5. Fidélité au document*

Travaille *exclusivement à partir du contenu du fichier fourni*. N’ajoute aucune jurisprudence, aucun article et aucune explication provenant de tes connaissances personnelles ou d’une recherche extérieure.

Ne modifie pas les références juridiques figurant dans le document, sauf pour corriger une coquille manifeste.
"""
