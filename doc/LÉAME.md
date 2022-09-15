# Inspector del Estilo (para LaTeX)

## Introducción
¿Usted està cansado de escribir papeles y accidentalmente usando los guiones diferentemente en vocabularios especializados cada vez que lo escribe? ¿No está seguro si ya definió ese acrónimo en el texto?  Este paquete LaTeX genera mensajes de advertencia cuando ocurren estes problemas, así puede escribir más consistentemente.

## Comienzo Rápido
Este paquete sólo estaba probado en Overleaf con los compiladores pdflatex y xelatex.  Tal vez otras plataformas serían apoyadas en el futuro, pero por el momento su kilometraje puede variar.

1. Suba los archivos ```stylechecker.py``` y ```stylechecker.sty``` de este repositorio al directorio raíz de su proyecto Overleaf.
2. Incluya este paquete en su archivo .tex principal: ```\usepackage{stylechecker}```
3. Añada el mandato ```\checkhyphenation{}``` en alguna parte de su documento para comprobar para el uso de guiones inconsistente (p.e., "hyper-parameters" y "hyperparemeters").  Si algunas instancias sean encontradas, un mensaje de advertencia aparecerá en el tiempo de compilación.
4. Añada el mandato ```\checkacronyms{}``` en alguna parte de su documento para generar una lista de todos los acrónimos usados y sus definiciones.  Si un acrónimo no ha definido, un mensaje de advertencia estará mostrado.
5. Añada el mandato ```\checklocalization{}``` para comprobar si la ortografía de Los Estados Unidos y El Reino Unido aparecen juntos en el mismo documento.  Si los dos son presentes, la log de compilación se indicará a cada instancia, así sabrá lo que necesita cambiar.

## Cómo Contribuir
Si encuentra un bug o quiere una prestación adicional, por favor abra un problema en el rastreador de problemas.  Si arregla un problema su mismo o quiere contribuir una prestación nueva, por favor no dude en hacer un «pull request».

Un [Dockerfile](https://docs.docker.com/get-docker/) se ha proporcionado para establecer un ambiente de comprobación consistente a través todos las plataformas.  Para construir la imagen docker, por favor ejecute el mandato seguimiento del directorio raíz de este repositorio:

```
docker build . --file ci/Dockerfile --tag stylechecker:latest
```

Es recomendado usar [Black](https://github.com/psf/black) para formatear algunos archivos de Python:

```
docker run -v $PWD:/stylechecker stylechecker:latest black --check /stylechecker/
```

Finalmente, pruebas unitarias se han proporcionados para comprobar las funciones individuales en ```stylechecker.py``` mientras pruebas de integración se han proporcionados para comprobar la funcionalidad de extremo a extremo con el compilador LaTeX en el circuito.  Para ejecutar las pruebas unitarias:

```
docker run -v $PWD:/stylechecker stylechecker:latest coverage run -m unittest test.test_stylechecker
```

Para ejecutar las pruebas de integración:

```
docker run -v $PWD:/stylechecker stylechecker:latest python3 -m unittest ci.integration_test
```

## Documentación en otras idiomas
[Documentation en français](LISEZ-MOI.md)
[Documentation in English](../README.md)
[Documentazione in italiano](LEGGIMI.md)
[中文手冊](%E8%AE%80%E6%88%91%E6%AA%94%E6%A1%88.md)