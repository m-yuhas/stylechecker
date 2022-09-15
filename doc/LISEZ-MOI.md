# Vérificateur de Style (pour LaTeX)

## Introduction
Est-ce que vous êtes fatigué d'écrire articles et accidentellement utilisant un trait d'union différemment chaque fois vous tapez vocabulaire spécialisé?  Est-ce que vous n'êtes pas sûr si vous avez déjà défini cet acronyme dans le texte? Ce paquet LaTeX génère messages d'avertissement quand quelconque de ces problèmes se produit, alors vous pouvez écrire plus régulièrement.

## Lancement Rapide
Ce paquet a été seulement testé en Overleaf avec les compilateurs pdflatex et xelatex.  Peut-être qu'autres plates-formes soient soutenu dans le futur, mais pour l'instant votre kilométrage peut varier.

1. Téléchargez les fichiers ```stylechecker.py``` et ```stylechecker.sty``` de ce dépôt vers le directoire racine de votre projet Overleaf.
2. Incluez ce paquet dans votre fichier .tex principal: ```\usepackage{stylechecker}```
3. Ajoutez la commande ```\checkhyphenation{}``` à quelque part de votre document pour vérifier si l'utilisation des traits d'union est inconsistante (p.ex., "hyper-parameters" et "hyperparameters").  Si des exemples sont trouvés, une message d'avertissement apparaîtra au moment de la compilation.
4. Ajoutez la commande ```\checkacronyms{}``` à quelque part de votre document pour générer une liste de tous les acronymes utilisés et leurs définitions.  Si un acronyme ne n'était pas défini, une message d'avertissement s'affichera.
5. Ajoutez la commande ```\checklocalization{}``` pour vérifier si les orthographes des États-Unis et du Royaume-Uni apparaissent ensemble dans le même document.  Si les deux sont présentes, le journal de compilation vous montrera chaque occurrence, alors vous saurez qu'est-ce que vous deviez modifier.

## Comment Contribuer
Si vous trouvez un bogue ou voulez une fonction additionnelle, s'il vous plaît ouvrez un problème en le traqueur de problèmes GitHub.  Si vous réglez un bogue vous-même ou voulez contribuer une fonction additionnelle, s'il vous plaît n'hésitez pas faire une «pull request».

Un [Dockerfile](https://docs.docker.com/get-docker/) a été fourni pour mettre en place un environnement de test cohérent vers tous les plates-formes.  Pour bâtir l'image docker exécutez la suivante du directoire racine de ce dépôt:

```
docker build . --file ci/Dockerfile --tag stylechecker:latest
```

Il est recommandé d'utiliser [Black](https://github.com/psf/black) pour formater tous les fichiers Python:

```
docker run -v $PWD:/stylechecker stylechecker:latest black --check /stylechecker/
```

Finalement, les tests unitaires sont fournis pour tester les fonctions individuelles dans ```stylechecker.py``` tandis que les tests d'intégration sont fournis pour tester la fonctionnalité de bout en bout avec le compilateur LaTeX en boucle.  Pour exécutez les tests unitaires:

```
docker run -v $PWD:/stylechecker stylechecker:latest coverage run -m unittest test.test_stylechecker
```

Pour exécutez les tests d'intégration:

```
docker run -v $PWD:/stylechecker stylechecker:latest python3 -m unittest ci.integration_test
```

## Documentation en Autres Langues
[Documentación en español](L%C3%89AME.md)

[Documentation in English](../README.md)

[Documentazione in italiano](LEGGIMI.md)

[中文手冊](%E8%AE%80%E6%88%91%E6%AA%94%E6%A1%88.md)