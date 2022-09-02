# xiaolin wu's algorithm

El algortimo solo funciona para puntos con valores enteros.

#### Linea simple

Dibuja una linea desde un punto1 a un punto2.
Comando de uso
`wu_aaline.py [-p | --point] <x1-y1> <x2-y2>`
Ejemplo:

```bash
python wu_aaline.py -p 50-70 300-350
```

#### Dibujar poligono

Dibuja un poligono con los puntos del archivo de una ruta especificada.
Comando de uso
`wu_aaline.py [-f | --file] <path>`
Ejemplo:

```bash
python wu_aaline.py -f ./dino.txt
```

#### Dibujar linea con animaciones.

Dibuja una linea simple con puntos predeterminados para simular el comportamiente del algortimo.
Comando de uso
` wu_aaline.py [-a | --animated]`
Ejemplo:

```bash
python wu_aaline.py -a
```
