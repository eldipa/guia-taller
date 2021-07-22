#### Primitivas geométricas en SDL

Para dibujar figuras geométricas usaremos
`SDL2_gfx`^[https://www.ferzkopp.net/Software/SDL2_gfx/Docs/html/index.html] de
*ferzkopp*.

Todas las primitivas reciben un `renderer` donde dibujar
y las coordenadas que determinan el lugar.

`lineRGBA` no es la excepción: recibe un `renderer`
y dos pares de `x` e `y` para
determinar el principio y fin de la línea.

```cpp
{{ include_block('out/t/src/gfx.j2.c', 'line_example') }}
```

Suponiendo que la pantalla tiene dimensiones `WIDTH, HEIGHT`, el código
de arriba debe leerse como:

 - una línea desde la esquina superior izquierda (`0, 0`) hacia la esquina
inferior derecha (`WIDTH, HEIGHT`).
 - otra línea que va en la diagonal opuesta (desde la esquina superior derecha
(`WIDTH, 0`) hacia la esquina inferior izquierda (`0, HEIGHT`)).
 - otra línea más que cruza horizontalmente la pantalla a la mitad de su
altura (`HEIGHT/2`)

Como lo deduciras del nombre `lineRGBA` recibe 4 valores adicionales que
representan el color de la línea: *red, green, blue* y *alpha*.

El color *alpha* determina que tan translúcido es el color:

 - `0x00` para objetos totalmente transparentes.
 - `0xff` para objetos totalmente opacos.

En este ejemplo hay 2 cuadrados donde el segundo es ≈ 40% translúcido.
Puede verse como su color se mezcla con el color que hay detras.

```cpp
{{ include_block('out/t/src/gfx.j2.c', 'alpha_box_example') }}
```

Muchas de las primitivas en `SDL2_gfx` permiten dibujar un contorno o
una figura completa (aka *rellena*).

Aca hay dos ejemplos de como dibujar solo el contorno de un círculo
(`circleRGBA`) y de como dibujar el círculo completo (`filledCircleRGBA`).

```cpp
{{ include_block('out/t/src/gfx.j2.c', 'circle_example') }}
```

```cpp
{{ include_block('out/t/src/gfx.j2.c', 'filled_circle_example') }}
```

Y hablando de círculos, con `filledEllipseRGBA` dibujamos elipses

```cpp
{{ include_block('out/t/src/gfx.j2.c', 'ellipse_example') }}
```

Y polígonos? `SDL2_gfx` tiene `polygonRGBA` para dibujar polígonos
arbitrarios como un triángulo o un rombo.

El único detalle es que hay que pasarle las coordenadas `x` e `y` de los
vertices por dos vectores.

```cpp
{{ include_block('out/t/src/gfx.j2.c', 'rhombus_params') }}

{{ include_block('out/t/src/gfx.j2.c', 'rhombus_example') }}
```

\SectionBreak

```cpp
{{ include_block('out/t/src/gfx.j2.c', 'triangle_params') }}

{{ include_block('out/t/src/gfx.j2.c', 'triangle_example') }}
```

#### Código completo

```cpp;breakable
{{ include_block('out/src/gfx.c', block=None, strip=False) }}
```
