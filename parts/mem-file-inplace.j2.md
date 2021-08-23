# Overlapping

Considerá el siguiente ejercicio: reemplazar todas las apariciones
de `"A"` por `"BB"` en un string dado.

Fácil?

Le pondremos una vuelta de tuerca: el reemplazo se tiene
que hacer sobre el mismo buffer de entrada y sin usar un buffer
auxiliar.^[
Por que prohibirnos el uso de un buffer adicional? No es complicarse
innecesariamente?
En general sí, pero hay situaciones en donde uno simplemente no tiene
memoria suficiente para un buffer adicional.
Hoy en día las computadoras tienen decenas de gigas pero no olvides
que los problemas a resolver son cada vez más grandes también!
]

Es lo que se llama un procesamiento *in place*.

Más general, cuando el buffer de entrada se *solapa* parcial o
completamente con el de salida diremos que hay *overlapping* entre
los buffers.^[Trabajar *in place* es un caso particular de
*overlapping*.]

Y esto lo cambia todo.


## Dos pasadas

Veamos primero como resolveríamos el problema si pudieramos trabajar con
un buffer adicional sin overlapping.

Tendríamos el buffer de entrada `src` y el de salida `dst`:

```cpp
src: "aaaAabbAAa"
dst: "aaaBBabbBBBBa"
```

Dado `src`, lo que tenemos que resolver primero es saber el tamaño
de `dst` y alloc'arlo.

Y hay dos opciones:

 - asumimos un tamaño \(X\) y si a medida que procesamos `src` vemos
que nos quedamos *cortos*, expandimos el buffer `dst`.
 - o no asumimos nada y procesamos `src` pero *solo contando* cuantos
bytes escribiríamos en `dst`; sabiendo ya el tamaño exacto, reservamos
`dst` y hacemos un *segundo* procesado, esta vez sí escribiendo en `dst`.

Puede que la segunda opción suene más ineficiente y sí, estamos
realizando 2 veces el procesamiento.

Es lo que se llama un algoritmo de *dos pasadas* o *two passes*.^[\LaTeX{},
la tecnología con la que esta hecho este libro, es un ejemplo de un programa de
*múltiples* pasadas.]

Pero considerá la primera opción en detalle *"si nos quedamos cortos,
expandimos el buffer"*.

Expandir un array es costoso. En el mejor caso hay suficiente espacio
*a continuacion* del final del buffer, `realloc` lo reserva y retorna
el mismo puntero inicial.

Pero y si no hay espacio? `realloc` se verá
forzado a reservar un buffer entero y transferir (aka
copiar) el contenido del buffer viejo al nuevo.

*Varios `realloc`s, varias copias, más lento.*

Veamos entonces el algoritmo de dos pasadas:

```cpp
char* repl_2pass(const char* src) {
    // Primera pasada, solo contamos cuantos bytes tendrá
    // el buffer destino
    size_t sz = 0;
    const char* rdptr = src;
    while (*rdptr) {
        if (*rdptr == 'A') {
            sz += 2;
        } else {
            sz += 1;
        }

        ++rdptr;
    }

    char* dst = malloc(sz + 1);
    dst[sz] = 0;

    // Reset pointers
    rdptr = src;
    const char* wrptr = dst;

    // Segunda pasada, mismo algoritmo pero esta vez realizando
    // las escrituras en dst
    while (*rdptr) {
        if (*rdptr == 'A') {
            *wrptr++ = 'B';
            *wrptr++ = 'B';
        } else {
            *wrptr++ = *rdptr;
        }

        ++rdptr;
    }

    return dst;
}
```

## In place

Ahora forcemos que `dst` sea el mismo buffer de entrada `src`.

Y esto lo cambia todo: como escribimos más bytes de los que leemos,
estaremos pisando/sobreescribiendo bytes que aun no leímos.

```cpp
    while (*rdptr) {
        if (*rdptr == 'A') {
            *wrptr++ = 'B';   // pisaríamos *rdptr
            *wrptr++ = 'B';   // pisaríamos *rdptr+1 antes de leerlo!
        } else {
            *wrptr++ = *rdptr;
        }

        ++rdptr;
    }
```

Este problema siempre lo tendremos cuando las areas `src` y `dst`
se *solapen*, es decir cuando haya *overlapping*.

Trabajar *in place* es solo un caso particular.

La solución? Antes de comenzar la segunda pasada movemos el contenido útil
de `src` hacia el final del mismo.

Dejando suficiente espacio al principio, el puntero de escritura `wrptr`
nunca va a alcanzar al de lectura `rdptr`.

```cpp;asciidiagram
       Buffer src inicial
      /-- --  --  --  -- --\
      |                    |
      +--------------------+-------+
src > |     aaaAabbAAa     |  ???  |
      +--------------------+---+---+
                               |
                               V
                          Realloc'ados
     wrptr   rdptr
      |       |
      V       V
      +-------+--------------------+
src > |  xxx  |     aaaAabbAAa     |
      +-------+----------+---------+
                         |
                         V
                 Contenido movido
```

El algoritmo quedaría así:

```cpp
char* repl_2pass_inplace(const char* src) {
    // Primera pasada, solo contamos cuantos bytes tiene
    // el buffer inicialmente y cuantos tendrá al final
    size_t final_sz = 0;
    const char* rdptr = src;
    while (*rdptr) {
        if (*rdptr == 'A') {
            final_sz += 2;
        } else {
            final_sz += 1;
        }

        ++rdptr;
    }

    size_t initial_sz = rdptr - src;

    // Resize + shift: alloc'amos un buffer lo suficiente grande
    // y "deslizamos/movemos" el contenido del buffer a la derecha
    // dejando N bytes libres al principio del buffer
    src = realloc(src, final_sz + 1);
    memmove(src + (final_sz - initial_sz), src, initial_sz);

    // Reset pointers
    rdptr = src + (final_sz - initial_sz); // al comienzo del contenido movido
    const char* wrptr = src; // al comienzo del buffer

    // Segunda pasada, mismo algoritmo pero esta vez realizando
    // las escrituras in place
    while (*rdptr) {
        if (*rdptr == 'A') {
            *wrptr++ = 'B';
            *wrptr++ = 'B';
        } else {
            *wrptr++ = *rdptr;
        }

        ++rdptr;

        // Sanity check: si los cálculos de los sizes son correctos
        // el puntero de escritura nunca va a sobrepasar al de lectura
        assert(rdptr >= wrptr);
    }

    return src;
}
```

{% from 'z/templ/boxes.j2' import extra_footage %}

{% call extra_footage() %}
Por que `assert(rdptr >= wrptr)` ?

Sabemos que `wrptr` *nunca* va a
sobrepasar a `rdptr`, es un *invariante* del algoritmo.

Pero el código es un ser viviente y basta con algún error de nuestra parte
o un refactor en el futuro y podemos caer en `wrptr > rdptr`.

Violación de un invariante → bug en nuestro código.

Ese `assert` garantiza que si llegamos a una situación *imposible*,
el programa crasheará. Medida drástica pero es mejor que dejar que el
programa siga en un estado indefinido.

Notar que `assert` **no** debe usarse para manejar errores que,
aunque parezcan improbables, puedan suceder.

Por ejemplo, `malloc` podría retornarnos `NULL`: el programa
debería manejar el error, incluso si es improbable y **no** usar `assert`:

```cpp
void *buf = malloc(sz);
assert(buf != NULL);  // mal, esto no es un invariante

void *buf = malloc(sz);
if (buf == NULL) {  // mejor
    errno = ENOMEM;
    return -1;
}
```

{% endcall %}

#### Ejercicios

{{ ej() }}

Por qué en `repl_2pass_inplace` usé `memmove` y no `memcpy` ? Busca sus
páginas de manual.

```cpp
char buf[] = "foobar";
memcpy(buf+3, buf, 3);
```

Qué valor debería tener `dst` y que valor realmente termina teniendo?
Probá luego con `memmove`.


{{ ej() }}

Implementate el resize+shift pero sobre un archivo. Esto es,
dado un `FILE* f`, reservar `n` bytes al final del archivo y luego
mover el contenido del archivo `n` bytes hacia adelante tal como
lo hicimos con `memmove`.

```cpp
int resize_and_shift(FILE* f, size_t n);
```

Asumí que `f` ya esta abierto en modo `"rw+"`.

Tip: busca `ftell()` y `fseek()` en C y sus contrapartes en C++.

Podes mover el contenido de a un byte (fácil). Si lo moves de a bloques
tenes puntos extras.

{{ ej() }}

Dado un archivo `foo.dat`, reemplazar todas las apariciones
de `"A"` por `"BB"`.

{{ ej() }}

Dado un archivo `foo.dat`, reemplazar todas las apariciones
de `"BB"` por `"A"`. Necesitas un algoritmo de 2 pasadas?

El archivo resultante se achicará. El estándar C/C++ no ofrece
una forma de achicar un archivo pero POSIX sí. Busca `ftruncate()`.

{{ ej(tricky=True) }}

Dado un archivo `foo.dat`, reemplazar todas las apariciones
de `"A"` por `"BB"` y `"CC"` por `"D"`.

Por ejemplo, dada la secuencia `"ACC"`; el resultado final seria `"BBD"`.

Tip: si implementaras una adaptación de `repl_2pass_inplace` para que
haga los reemplazos `"A"` por `"BB"` y `"CC"` por `"D"`, funcionaría?
Qué invariante se rompe?

Recordá que para evitar una corrupción de los datos se debe cumplir
`wrptr < rdptr` en todo momento.

*Tricky*, pero no imposible.


{#

{{ ej() }}

Te dije que habían dos opciones: asumir un tamaño \(X\) o procesar
dos veces.

Te mentí. Podes usar una estructura de datos auxiliar.

Implementate `void repl_inplace(char* src)`
usando una *rope data structure*.

https://developers.redhat.com/blog/2020/06/02/the-joys-and-perils-of-c-and-c-aliasing-part-1#
https://developers.redhat.com/blog/2020/06/03/the-joys-and-perils-of-aliasing-in-c-and-c-part-2#the_price_of_aliasing_exemptions
https://doc.rust-lang.org/rust-by-example/scope/borrow/alias.html
 #}
