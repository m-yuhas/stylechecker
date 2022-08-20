# Inspector del Estilo (para LaTeX)

## Introducción
¿Usted està cansado de escribir papeles y accidentalmente usando los guiones diferentemente en vocabularios especializados cada vez que lo escribe? ¿No está seguro si ya definió ese acrónimo en el texto?  Este paquete LaTeX genera mensajes de advertencia cuando ocurren estes problemas, así puede escribir más consistentemente.

## Comienzo Rápido
Este paquete sólo estaba probado en Overleaf con el compilador pdflatex.  Tal vez otras plataformas serían apoyadas en el futuro, pero por el momento su kilometraje puede variar.

1. Suba los archivos ```stylechecker.py``` y ```stylechecker.sty``` de este repositorio al directorio raíz de su proyecto Overleaf.
2. Incluya este paquete en su archivo .tex principal: ```\usepackage{stylechecker}```
3. Añada el mandato ```\checkhyphenation{}``` en alguna parte de su documento para comprobar para el uso de guiones inconsistente.  Si algunas instancias sean encontradas, un mensaje de advertencia aparecerá en el tiempo de compilación.

## Cómo Contribuir
Si encuentra un bug o quiere una prestación adicional, por favor abra un problema en el rastreador de problemas.  Si arregla un problema su mismo o quiere contribuir una prestación nueva, por favor no dude en hacer un «pull request».