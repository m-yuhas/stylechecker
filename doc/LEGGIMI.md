# Correttore di Stile (per LaTeX)

## Introduzione
Lei è stanco di scrivere articoli e accidentalmente usando trattini in vocabulario specializzato differentemente ogni volta che batte a macchina? Lei non è sicuro se già definì quell'acronimo in il testo o no? Questo pacchetto LaTeX genera messaggi di avviso quando qualunque di questi problemi succede, così Lei può scrivere più costantemente.

## Inizio Rapido
Questo pacchetto è stato solo testato in Overleaf con i compilatori pdflatex e xelatex.  Forse altre piattaforme saranno supportate nel futuro, ma per adesso il suo chilometraggio può variare.

1. Carichi i file ```stylechecker.py``` e ```stylechecker.sty``` da questo reposito al direttorio radice del suo progetto Overleaf.
2. Includa questo pacchetto nel suo file .tex principale: ```\usepackage{stylechecker}```
3. Aggiunga il comando ```\checkhyphenation{}``` in qualche luogo del suo documento per controllare l'uso di trattini incoerente (p.e., "hyper-parameters" e "hyperparameters").  Se trova alcuni casi, un messaggio di avviso si mostrerà al tempo di compilazaione.
4. Aggiunga il comando ```\checkacronyms{}``` in qualche luogo del suo documento per generare una lista di tutti gli acronimi usati e le sue definizioni.  Se un acronimo non era definito, un messaggio di avviso si mostrerà.
5. Aggiunga il comando ```\checklocalization{}``` per controllare se la ortografia dei Stati Uniti e la ortografia del Regno Unito appaiono insieme nel stesso documento.  Se le due sono presenti, il registro di compilazione la indicherà ogni istanza, così saprà che cosa avrà bisogno di modificare.

## Come Contribuire
Se trova un bug o vuole una funzione supplementare, per favore apra un problema nell'inseguitore di problemi GitHub.  Se aggiusta un bug lei stesso o vuole contribuire una nuova funzione, per favore si senta libero fare un «pull request».

Un [Dockerfile](https://docs.docker.com/get-docker/) è stato fornito per stabilire un ambiente di test coerente attraverso piattaforme.  Per construire l'immagine docker esegua il seguente dal direttorio radice da questo reposito:

```
docker build . --file ci/Dockerfile --tag stylechecker:latest
```

È raccomandato usare [Black](https://github.com/psf/black) per formattare alcuni file Python:

```
docker run -v $PWD:/stylechecker stylechecker:latest black --check /stylechecker/
```

Finalmente, le prove unitarie sono stato fornite per provare funzioni individuale in ```stylechecker.py``` mentre le prove dell'integrazione sono stato fornite per provare la funzionalità da un capo all'altro con il compilatore LaTeX di continuo.  Per esegua le prove unitarie:

```
docker run -v $PWD:/stylechecker stylechecker:latest coverage run -m unittest test.test_stylechecker
```

Per esegua le prove dell'integrazione:

```
docker run -v $PWD:/stylechecker stylechecker:latest python3 -m unittest ci.integration_test
```

## Documentazione in Altre Lingue
[Documentación en español](L%C3%89AME.md)
[Documentation en français](LISEZ-MOI.md)
[Documentation in English](../README.md)
[中文手冊](%E8%AE%80%E6%88%91%E6%AA%94%E6%A1%88.md)