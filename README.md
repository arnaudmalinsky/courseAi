# courseAi

Outil personnel pour transformer des cours de droit au format `.docx` en fiches de revision structurees.

Le projet sert surtout a :

1. extraire le texte de documents Word en conservant une partie de la structure du cours ;
2. decouper les paragraphes trop longs ;
3. envoyer les morceaux de texte a un LLM pour identifier les references juridiques ;
4. regrouper les passages par titres de cours ;
5. demander au LLM de produire des resumes synthetiques ;
6. generer des fichiers Word de sortie avec les resumes et les references juridiques detectees.

## Vue D'ensemble

Le pipeline principal est pilote par `main.py` avec Typer.

```text
PDF de cours
  -> pdf-to-docx
  -> DOCX de cours
  -> process-documents
  -> Excel structure par paragraphes
  -> batch-llm-call --flag-law-ref
  -> Excel enrichi avec references juridiques
  -> concatenate-excel-text
  -> Excel groupe par parties/sous-parties du cours
  -> batch-llm-call --no-flag-law-ref
  -> Excel avec resumes
  -> edit-sumup-doc
  -> DOCX final de fiches de revision
```

## Structure Du Projet

```text
courseAi/
  main.py
  prompting/
    batch_llm_call.py
    law_reference_identification_prompt.py
    sumup_prompt.py
    ...
  text_processing/
    parsers.py
    pdf_to_docx.py
    concatenate_texts.py
    edit_sumup.py
    merge_text_and_llm.py
  sandbox_notebooks/
    notebooks d'experimentation
  LLM_text_cleaning/
    notebook lie au nettoyage de texte via LLM
  refine_results/
    constantes ou essais de post-traitement
```

### Fichiers importants

- `main.py` : point d'entree CLI.
- `text_processing/pdf_to_docx.py` : convertit un PDF texte en DOCX avec de vrais styles `Heading`.
- `text_processing/parsers.py` : lit les `.docx`, extrait paragraphes/titres, decoupe les textes longs et ecrit un Excel.
- `prompting/batch_llm_call.py` : appelle OpenAI via LangChain par lots et sauvegarde les resultats dans un Excel.
- `prompting/law_reference_identification_prompt.py` : prompt + colonnes attendues pour l'identification des references juridiques.
- `prompting/sumup_prompt.py` : prompt + colonnes attendues pour les resumes.
- `text_processing/concatenate_texts.py` : regroupe les paragraphes selon les titres du cours.
- `text_processing/edit_sumup.py` : fusionne resumes et references juridiques, puis cree un `.docx` final.

## Installation

Les dependances principales sont listees dans `requirements.txt`.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Le code a ete execute auparavant avec Python 3.11 d'apres les fichiers `__pycache__`.

## Commandes

Les commandes Typer sont definies dans `main.py`. Depuis la racine du projet :

```bash
python main.py --help
```

### 1. Convertir un PDF en DOCX

Si le cours est en PDF, commence par le convertir en DOCX structure :

```bash
python main.py pdf-to-docx "C:\chemin\vers\cours.pdf" --output-docx-path "C:\chemin\vers\cours.docx"
```

Cette premiere version utilise PyMuPDF pour extraire les blocs de texte, deduit les titres a partir des tailles de police et genere de vrais styles Word `Heading 1`, `Heading 2` et `Heading 3`. Ces styles sont importants, car `process-documents` les utilise ensuite pour remplir `Title Context`, `Title lvl2` et `Title lvl3`.

La conversion reste volontairement simple : elle ne cherche pas encore a reproduire les encadres, fonds colores ou autres effets graphiques du PDF.

Options utiles :

- `--preserve-page-breaks` : ajoute un saut de page Word entre les pages PDF.
- `--max-heading-chars` : longueur maximale pour considerer un bloc comme un titre. Defaut : `140`.

Ensuite, place le DOCX obtenu dans ton dossier de cours et lance l'extraction habituelle.

#### Extraction visuelle des jurisprudences en encadré

Lorsque le manuel est déjà découpé en un PDF par chapitre, cette commande envoie
chaque chapitre complet au modèle avec l'image d'exemple. Elle ne crée aucun
chevauchement entre chapitres. Chaque réponse structurée est sauvegardée après
l'appel afin de permettre une reprise sans retraiter les chapitres terminés.

```powershell
conda activate courseai
python main.py extract-boxed-case-law `
  "C:\chemin\vers\PAC chapitres" `
  "C:\chemin\vers\exemple_encadre.jpeg" `
  ".\data\pac_jurisprudences\repertoire_jurisprudences_encadrees.docx" `
  --cache-dir ".\data\pac_jurisprudences\chapters" `
  --model gpt-5.5 `
  --concurrency 2
```

La clé est lue depuis `OPENAI_KEY` ou `OPENAI_API_KEY` dans `.env`. Pour tester
un seul chapitre, ajoute `--from-chapter 1 --to-chapter 1`. La commande reprend
automatiquement les JSON présents dans `--cache-dir`; utilise `--force`
uniquement pour refaire les appels déjà réussis.

L'assemblage final produit simultanément le DOCX et un classeur Excel du même
nom. Le classeur contient une feuille `Jurisprudences` avec une ligne par
décision, la référence juridique et sa description synthétique dans deux
colonnes distinctes, ainsi qu'une feuille `Synthèse` avec le nombre de décisions par chapitre.
L'option `--output-xlsx-path` permet de choisir un autre emplacement.

### 2. Transformer des DOCX en Excel

```bash
python main.py process-documents "C:\chemin\vers\cours_docx" "C:\chemin\vers\sortie\cours_structure.xlsx"
```

Options utiles :

- `--max-length` : taille maximale d'un morceau de texte avant decoupage. Defaut : `5000`.
- `--overlap` : chevauchement entre morceaux decoupes. Defaut : `0`.
- `--verbose / --no-verbose` : logs detailles ou non.

Sortie attendue : un Excel avec les colonnes :

```text
Folder, Filename, Index, Type, Text, Character Index, Title Context, Title lvl2, Title lvl3
```

Le parser lit seulement les `.docx` directement presents dans le dossier donne, pas les sous-dossiers.

### 3. Identifier les references juridiques

```bash
python main.py batch-llm-call "OPENAI_API_KEY" "C:\chemin\vers\cours_structure.xlsx" "C:\chemin\vers\references.xlsx" --flag-law-ref
```

Cette etape lit la colonne `Text` et produit un Excel enrichi avec :

```text
flag_law, label, law_description, corpus, institution, law_type, location, date
```

Le prompt demande au modele d'identifier les articles, lois, arrets, decisions ou autres references juridiques citees dans le cours.

Options utiles :

- `--batch-size` : nombre de lignes traitees par lot. Defaut : `200`.
- `--limit` : limite le nombre de lignes traitees, pratique pour tester.
- `--verbose / --no-verbose` : logs detailles ou non.

### 4. Regrouper les textes par plan de cours

```bash
python main.py concatenate-excel-text "C:\chemin\vers\cours_structure.xlsx" "nom_du_cours"
```

Cette commande groupe les lignes par :

```text
Title Context, Title lvl2, Title lvl3
```

Elle cree un fichier dans le meme dossier que l'Excel d'entree :

```text
nom_du_cours_concat_text.xlsx
```

La colonne principale de sortie est :

```text
concat_texts
```

### 5. Produire les resumes de cours

```bash
python main.py batch-llm-call "OPENAI_API_KEY" "C:\chemin\vers\nom_du_cours_concat_text.xlsx" "C:\chemin\vers\sumup.xlsx" --no-flag-law-ref
```

Cette fois, le code lit `concat_texts` et demande au LLM de produire une fiche de revision en bullet points.

Sortie attendue :

```text
Title Context, Title lvl2, Title lvl3, concat_texts, Folder, Filename, Index, text_sumup
```

### 6. Generer le DOCX final

```bash
python main.py edit-sumup-doc "C:\chemin\vers\sumup.xlsx" "C:\chemin\vers\references.xlsx" "nom_du_cours"
```

Cette commande :

- fusionne les resumes avec les references juridiques detectees ;
- trie les passages par fichier et par index ;
- reconstruit les titres du cours ;
- ecrit un document Word par fichier source.

Les fichiers finaux sont crees dans le dossier du fichier `sumup.xlsx`, avec un nom du type :

```text
NomDuFichier_sumup.docx
```

## Exemple De Workflow Complet

```bash
python main.py pdf-to-docx ".\data\pdf\cours.pdf" --output-docx-path ".\data\docx\cours.docx"

python main.py process-documents ".\data\docx" ".\data\cours_structure.xlsx" --max-length 5000

python main.py batch-llm-call "%OPENAI_API_KEY%" ".\data\cours_structure.xlsx" ".\data\references.xlsx" --flag-law-ref --batch-size 100 --limit 20

python main.py concatenate-excel-text ".\data\cours_structure.xlsx" "droit_admin"

python main.py batch-llm-call "%OPENAI_API_KEY%" ".\data\droit_admin_concat_text.xlsx" ".\data\sumup.xlsx" --no-flag-law-ref --batch-size 50

python main.py edit-sumup-doc ".\data\sumup.xlsx" ".\data\references.xlsx" "droit_admin"
```

Pour relancer prudemment apres longtemps, commence avec `--limit 5` ou `--limit 20` sur les appels LLM.

## Notes Sur Le Fonctionnement

### Decoupage des documents

`DocumentParser` utilise `python-docx` pour lire les paragraphes. Les titres sont detectes a partir du nom de style Word contenant `Heading`.

Le contexte de titre est conserve sur trois niveaux :

```text
Title Context -> Heading 1
Title lvl2    -> Heading 2
Title lvl3    -> Heading 3
```

Les textes trop longs sont decoupes avec `RecursiveCharacterTextSplitter` de LangChain.

### Appels LLM

`batch_llm_call.py` utilise :

- `ChatOpenAI`
- modele actuel : `gpt-4o`
- temperature : `0`
- parser Pydantic pour forcer une sortie structuree

Deux schemas de sortie existent :

- `LawRefResponseSchema` pour les references juridiques ;
- `SumUpResponseSchema` pour les resumes.

### Sauvegarde Excel

Les resultats LLM sont sauvegardes au fur et a mesure par lot.

Attention : meme si un chemin de sortie est donne, `ExcelManager` cree actuellement un chemin horodate interne :

```text
../courseai_data/llm_result_all_corpus_<timestamp>.xlsx
```

Le chemin passe en argument sert surtout a detecter un fichier existant et reprendre apres les lignes deja presentes.

## Points Fragiles / A Verifier

- Il manque un fichier officiel de dependances (`requirements.txt` ou `pyproject.toml`).
- Certains prompts contiennent des caracteres mal encodes dans les fichiers source.
- `merge_text_and_llm.py` contient des chemins absolus de test et ne semble pas etre utilise par la CLI.
- La variable `course_name` dans `edit_sumup_doc` est passee a la fonction, mais elle n'est pas vraiment utilisee pour nommer les fichiers finaux.
- `batch_llm_call.py` importe quelques modules non utilises (`json`, `time`, `OpenAI`, `LLMChain`).
- Le parser ne descend pas dans les sous-dossiers.
- La commande d'appel LLM prend la cle OpenAI en argument CLI, ce qui peut l'exposer dans l'historique du terminal.
- La conversion PDF vers DOCX repose sur des heuristiques simples de taille de police et ignore les effets graphiques ; il faut verifier le DOCX obtenu sur quelques pages avant de lancer tout le pipeline.

## Reprendre Le Projet Rapidement

1. Installer les dependances avec `pip install -r requirements.txt`.
2. Si besoin, convertir un PDF avec `pdf-to-docx`.
3. Mettre quelques `.docx` de cours dans un dossier de test.
4. Lancer `process-documents` pour verifier que les titres Word sont bien reconnus.
5. Ouvrir l'Excel produit et verifier les colonnes `Text`, `Title Context`, `Title lvl2`, `Title lvl3`.
6. Lancer `batch-llm-call` avec `--limit 5` pour tester le prompt de references juridiques.
7. Lancer `concatenate-excel-text`.
8. Lancer `batch-llm-call --no-flag-law-ref` avec `--limit 5`.
9. Generer le `.docx` final avec `edit-sumup-doc`.

## Idee D'Ameliorations Prioritaires

- Lire la cle OpenAI depuis une variable d'environnement au lieu d'un argument.
- Corriger l'encodage des prompts.
- Rendre les chemins de sortie LLM plus explicites.
- Ajouter un petit dossier `examples/` avec un mini DOCX et les sorties attendues.
- Ajouter des tests simples pour le parsing DOCX et la concatenation Excel.

## Nouveau pipeline par chapitre

Le pipeline historique reste disponible. Le nouveau mode permet de convertir un
PDF, d'exporter un DOCX par chapitre, de résumer les chapitres en parallèle et
d'assembler les résultats disponibles.

### 1. Convertir et exporter les chapitres

```powershell
python main.py pdf-to-docx ".\data\cours.pdf" `
  --output-docx-path ".\data\cours.docx" `
  --chapters-dir ".\data\chapters"
```

Le dossier contient un fichier `chapters_manifest.xlsx`, un éventuel
`000_preambule.docx`, puis un DOCX par titre commençant par `CHAPITRE`.
Les lignes de table des matières comportant des pointillés et un numéro de page
sont conservées pour la complétude, mais reçoivent le type
`table_of_contents` et le statut `excluded` : elles ne sont ni envoyées au
modèle ni assemblées, y compris avec `--force`.

Le manifeste n'est déclaré complet qu'après réouverture des fichiers exportés.
La concaténation de leurs paragraphes et tableaux doit reproduire exactement la
séquence du DOCX complet. Un écart est enregistré comme avertissement, mais ne
bloque pas les étapes suivantes.

Les titres supérieurs aux chapitres sont conservés dans les colonnes `partie`
et `theme`. Lorsqu'un nouveau titre supérieur apparaît entre deux chapitres, il
est rattaché au chapitre qui suit.

Un DOCX existant peut aussi être découpé sans reconvertir le PDF :

```powershell
python main.py split-chapters ".\data\cours.docx" ".\data\chapters"
```

### 2. Résumer les chapitres

La commande lit automatiquement le fichier `.env`. Les variables reconnues
sont :

```dotenv
OPENAI_KEY=...
OPENAI_MODEL=gpt-5.6-terra
MODEL_REASONNING=standard
MODEL_VERBOSITY=low
MODEL_SUMMARY=concise
```

`OPENAI_API_KEY` et `MODEL_REASONING` sont également acceptés. La valeur
`standard` est convertie en `medium`, qui est la valeur correspondante acceptée
par l'API Responses.

```powershell
python main.py summarize-chapters ".\data\chapters\chapters_manifest.xlsx" `
  --concurrency 4
```

Chaque résultat est sauvegardé dans le manifeste dès qu'il est terminé. Une
nouvelle exécution reprend les lignes `pending`, `processing`, `error` ou les
anciens statuts `invalid`.

Pour traiter uniquement certains chapitres :

```powershell
python main.py summarize-chapters ".\data\chapters\chapters_manifest.xlsx" `
  --chapter-id chapter_001 `
  --chapter-id chapter_005 `
  --concurrency 2
```

La sélection peut aussi utiliser la colonne `order` :

```powershell
python main.py summarize-chapters ".\data\chapters\chapters_manifest.xlsx" `
  --order 1 `
  --order 2 `
  --order 3
```

Pour sélectionner une plage inclusive d'un seul coup :

```powershell
python main.py summarize-chapters ".\data\chapters\chapters_manifest.xlsx" `
  --from-order 1 `
  --to-order 10 `
  --concurrency 4
```

`--from-order 1 --to-order 10` traite les ordres 1 à 10 inclus. Utilisé seul,
`--from-order 10` traite tous les ordres à partir de 10 et `--to-order 10`
traite tous les ordres jusqu'à 10.

Ajouter `--force` pour retraiter les chapitres sélectionnés même s'ils ont déjà
le statut `complete`.

Pendant le traitement, la CLI affiche le démarrage de chaque chapitre, la
progression `traités/total`, le pourcentage, le statut, le temps écoulé et une
estimation du temps restant. Le message de progression est écrit après la
sauvegarde du résultat correspondant dans le manifeste. Utiliser `--no-verbose`
pour ne conserver que les avertissements et erreurs.

Les contrôles vérifient notamment l'intitulé, l'ordre et le niveau des titres,
l'absence de catégories interdites et l'ajout de listes lorsqu'il n'en existe
aucune dans la section source. Les anomalies sont enregistrées dans la colonne
`validation` comme avertissements et ne bloquent ni la sauvegarde ni
l'assemblage.

### 3. Assembler le DOCX final

```powershell
python main.py assemble-summaries `
  ".\data\chapters\chapters_manifest.xlsx" `
  ".\data\fiche_finale.docx"
```

L'assemblage utilise toutes les lignes contenant un résumé, indépendamment du
statut ou des avertissements de validation. Les lignes sans résumé sont
ignorées. Une réduction cumulée inférieure à 50 % produit un avertissement sans
bloquer le DOCX. `partie`, `theme` et les titres Markdown sont convertis
respectivement en vrais styles Word `Heading 1`, `Heading 2` et niveaux
inférieurs ; les concepts entre `**` sont mis en gras.
