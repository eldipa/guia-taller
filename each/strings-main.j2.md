
# Strings

En C y C++ los strings son bloques contiguos de memoria: representan
tanto texto como *chunks* de data binaria.

Ambos casos se representan con `char*` lo que puede generar confusión
y como `char*` es sólo un puntero sin noción del tamaño del string, es
fácil caer en alguna corrupción de memoria.

Pero ya llegaremos a eso; arranquemos por el principio.

## Null terminated

Cuando el compilador ve un string *escrito* en el programa, este le
agrega un `'\0'` al final.

Es el compilador en *tiempo de compilación* quien pone el `'\0'`.

Pero si el string se construye en *runtime* es el programador
(**vos y yo**) quien debe responsabilizarse de poner un `'\0'` al final.

Por suerte algunas funciones de la librería estándar de C ya lo hacen
por nosotros:

```cpp
const char* msg = "hello";  // después de la 'o', el compilador
                            // agrega el '\0'.

char* copy = strdup(msg); // strdup agrega el '\0' por nosotros.
```

Lamentablemente la librería estándar es **extraordinariamente
inconsistente** en este aspecto.

Algunas funciones **no** ponen un `'\0'`, otras lo ponen pero sólo si
hay espacio suficiente y otras ponen el `'\0'` siempre.

Acá hay un pequeño e incompleto resumen:

---------------------   ---------------------   -----------------
`strdup`  →  siempre    `strcpy`  →  siempre    `memcpy` →  nunca
`strndup` →  siempre    `strncpy` →  a veces
---------------------   ---------------------   -----------------

Fijate en el par `strdup` y `strndup`, ambas siempre ponen un `'\0'` al
final mientras que `strcpy` y `strncpy` no son consistentes entre sí.

`strcpy` pone un `'\0'` mientras que `strncpy` lo hace solo si tiene
espacio en el buffer destino.

#### Ejercicios

{{ ej() }}
`strcpy` copia un string a un buffer destino. Su firma es:

```cpp
char* strcpy(char* dst, const char* src);
```

Codeá y ejecutá el siguiente snippet:

```cpp
char buf[10]
strcpy(buf, "hello");   // copia "hello" a buf
printf("%s\n", buf);
```

Cuántos bytes tiene disponibles `buf` antes de la copia?

Cuántos bytes se copiaron? No especules, **lee** la documentación de
`strcpy`. Cuál es la condición de corte para frenar el copiado?

Corré el código con Valgrind.

{{ ej() }}
Probá ahora en cambiar el tamaño de `buf` a 5. Qué sucede? Y si el
tamaño fuera 1?

`strcpy` **no tiene forma de saber** cuantos bytes tiene el buffer
destino porque sólo recibió un `char*` como parámetro.

`strncpy`, en cambio, recibe el tamaño del buffer **destino** para
frenar la copia antes y evitar el *buffer overflow*.

{{ ej() }}

Al igual que `strcpy`, las siguientes funciones **escriben en un buffer
sin tener en cuenta su tamaño** por lo que son susceptibles a un buffer
overflow.

```cpp
int sprintf(char* str, const char* format, ...);
char* gets(char* s);
char* strcat(char* dest, const char* src);
int scanf(const char* format, ...); // Tip: scanf("%s", ...);
```

Codear un ejemplo que triggeree dicho buffer overflow para cada una.

{{ ej() }}

Como se vió, `strncpy` es la versión *"segura"* de `strcpy`. Cuáles son
las funciones *"seguras"* de las funciones del ejercicio anterior?


{{ ej() }}

`strncpy` es *"segura"* sólo si se la usa correctamente!

Sólo una las llamadas es correcta y el resto es *fruta*.

Cuáles y por qué?

```cpp
char dst[10];
char src[1000];

strncpy(dst, src, sizeof(src)-1);
strncpy(dst, src, strlen(dst));
strncpy(dst, src, sizeof(dst)-1);
strncpy(dst, src, strlen(src));
```

Nota: `strncpy` evita el buffer overflow pero **no** pone un `'\0'` en
ese caso. Por eso es **siempre** buena idea poner un `'\0'` explícito
luego de la copia: `dst[sizeof(dst)-1] = 0;`


## Texto o binario?

Muchas de las funciones de la librería estándar asumen que el string de
entrada ya tiene un `'\0'` al final.

Si el string de entrada no tiene un `'\0'` el comportamiento de la
función es indefinido.

Léase *"corrupción de memoria y crash"*.

```cpp
const char msg[] = {'h', 'e', 'l', 'l', 'o'}; // no hay ningún '\0'
char* copy = strdup(msg); // ⚠ comportamiento indefinido
```

Cuando se trate de strings vamos a hacer una separación entre las
funciones que asumen `'\0'` y las que no.

Las primeras usan el `'\0'` para saber cuál es el fin del string.

Como los humanos no hablan binario, usar el byte 0 como fin del string
es práctico ya que no debería haber un `'\0'` en el medio del string que
pueda malinterpretarse.

Son funciones que entienden que el string es **texto de humanos**.

Las otras funciones ignoran cualquier `'\0'` y en cambio, reciben
por parámetro el **tamaño del string**. Son funciones que
entienden que el string es un **string binario arbitrario**.

Esta separación es **importantísima**.

Cuando estés trabajando con texto escrito por humanos, hay que usar
las funciones que vean a los strings como texto. Tendrás que asegurarte
que **siempre** tengan un `'\0'` al final!

Cuando estés trabajando con binario, **no** uses las funciones para el
texto. Un string binario puede tener una cantidad arbitraria de `'\0'`
y hasta puede perfectamente no tener un `'\0'` al final
lo que daría un comportamiento indefinido.

Vayamos a un par de ejemplos yendo a la documentación oficial:

 - `size_t strlen(const char *s)`: De su [página de
manual](https://man7.org/linux/man-pages/man3/strlen.3.html),
*"calculates the length of the string...excluding the terminating null
byte"*. Asume que el string termina en un `'\0'`, entonces es una
función para **texto**.
 - `char *strncpy(char *dest, const char *src, size_t n)`: De su [página de
manual](https://man7.org/linux/man-pages/man3/strcpy.3.html), *"copies
the string...including the terminating null byte..."*. Asume un `'\0'`,
función para **texto**.
 - `char *strncat(char *dest, const char *src, size_t n)`: De su [página de
manual](https://man7.org/linux/man-pages/man3/strcat.3.html), *"appends
the `src` string to...overwriting the terminating null byte..."*.
Adiviná? Asume un `'\0'`, función para **texto**.
 - `void *memcpy(void *dest, const void *src, size_t n)`: De su [página
de manual](https://man7.org/linux/man-pages/man3/memcpy.3.html),
*"copies `n` bytes from memory area `src` to memory area `dest`"*. No
asume nada, función para **binario**.
 - `int memcmp(const void *s1, const void *s2, size_t n)`: De su [página
de manual](https://man7.org/linux/man-pages/man3/memcmp.3.html),
*"compares the first `n` bytes...of the memory areas `s1` and `s2`"*. No
asume nada, función para **binario**.

Notás el patrón? Las funciones con nombres que empiezan con `str` son
funciones para texto, las que empiezan con `mem` son para binario.

Cuidado que hay más funciones que estas! `fgets` por ejemplo es para texto y
`fread` es para binario y ninguna sigue el patrón.

Es por eso que la documentación **oficial** como las páginas de manual
son **esenciales**.

#### Ejercicios

{{ ej() }}
Clasificá las siguientes funciones en *para texto* y *para binario*:
`getline`, `stpcpy` (no es un typo, dije `stpcpy`), `wcpcpy`, `memmem` y
`bzero`.

Justificá con algún fragmento de la documentación oficial.

{{ ej() }}
C/C++ no son los únicos que mezclan texto y binario. Buscá que
*sorpresas* suceden al mezclar `str`{.python} y `unicode`{.python}
en Python 2 (en Python 3 lo arreglaron pero fue un parto). Y en Ruby?

{{ ej() }}
Algunas funciones vienen de a parejas: hacen lo mismo pero una sirve
para texto y la otra para binario.

Por ejemplo `strncpy` y `memcpy` ambas copian strings.

Completar las parejas faltantes:

---------  ------------- ---------------------
`strncpy`   ...........   ← aquí iría `memcpy`
`strncat`   ...........
`strncmp`   ...........
`strchr`    ...........
---------  ------------- ---------------------


{{ ej() }}
`strlen` **no** tiene una función equivalente para binario. Por qué?

Tip: si tuvieras que implementar `strlen` a mano, como la harías? Y si
ahora tuvieras que implementarla pero sin asumir un `'\0'`? Ajá!


{{ ej() }}
Implementate la siguiente función:

```cpp
char* strreplace(
    const char* src,
    const char* search,
    const char* replace
)
```

Como lo podrás intuir, esta función toma
un *null terminated string* `src` y busca todas las apariciones de otro
*null terminated string* `search` y las reemplaza por `replace`
(también *null terminated*).

La función retorna el nuevo string con los reemplazos hechos.

Tratá de codear lo menos posible y hacer uso de la librería estándar.

Algunos ejemplos,

```cpp
strreplace("sopa de {} es todo lo que como", "{}", "almejas");
sopa de almejas es todo lo que como

strreplace(
    "pero a lZZZ ciegZZZ no les gustan lZZZ sordZZZ",
    "ZZZ",
    "os"
);
pero a los ciegos no les gustan los sordos
```


{{ ej() }}
Implementá ahora la versión para binario de `strreplace`: `memreplace`.

Ya no podés asumir que `src`, `search` y `replace` terminan en un
`'\0'`. Qué parámetros adicionales tiene que recibir `memreplace`
entonces? Tip: no son 3, son 4.

## Strings en C++

Si entendiste los strings en C, en C++ te va a resultar más fácil:
todo lo visto aplica a C++ pero además C++ tiene algunos objetos
que te facilitaran la vida.

*Te lo resumo así nomas*: para trabajar con texto usas `std::string`,
para trabajar con binario usas `std::vector<char>`.

#### Ejercicios

{{ ej() }}

Reimplementá `strreplace` y `memreplace` en sus versiones de C++. No
vale usar ninguna función de C! Tenés que usar los métodos de
`std::string` y `std::::vector<char>` respectivamente.

```cpp
// Para texto
std::string strreplace(
    const std::string& src,
    const std::string& search,
    const std::string& replace
);

// Para binario
std::vector<char> memreplace(
    const std::vector<char>& src,
    const std::vector<char>& search,
    const std::vector<char>& replace
);
```

Tip: revisar que [métodos](https://www.cplusplus.com/reference/)
[disponen](https://en.cppreference.com/w/)
`std:string` y `std::vector` antes de
codear.


{{ proj("Word Mangling") }}
Cuando un usuario se loguea a un sitio, su password es *hasheado* y
este *hash* es usado para la autenticación, para determinar si el
usuario es quien dice ser.

Se usa un hash porque si algún atacante tomara el control del servidor
del sitio podrá robarse los hashes pero no los passwords. Es una forma
de reducir el daño.

> Por qué es importante evitar el robo de passwords? Porque los humanos
> tienden a *reusar sus passwords*.
>
> Los atacantes apuntan a sitios
> web pocos seguros (digamos alguna plataforma de e-commerce) con el fin
> de conseguir estos passwords y, con algo de suerte, comprometer
> cuentas de otros sitios como Google, Facebook o Netflix. 😈

Debería ser una tarea imposible obtener un password a partir de un
hash^[Asumiendo que la función de hash es criptográficamente segura,
*lenta* y se usa salt.]
pero los hashes **no** garantizan protección absoluta e incondicional.

El humano tiende a utilizar
passwords simples y *comunes* con solo [algunas
variantes](https://wpengine.com/resources/passwords-unmasked-infographic/):
*"admin"*, *"admin123"* y *"admin123!"* son solo variantes de la misma palabra
*"admin"*.

Basta entonces tomar algún *diccionario*, generar a partir de él
variantes de cada palabra y computar su hash. Si coincide con alguno de
los hashes robados, bingo!, ya sabés cual era el password del usuario.

A esto se lo conoce como **password cracking** por
diccionario y a la generación de variantes como *word mangling*.

Es una excusa perfecta para jugar con `std::string`.

Escribir un
programa `wm` que tome un diccionario y
que genere todas las variantes posibles de cada palabra
a partir de una serie de *reglas de mutación* dadas por archivo.

Reglas posibles:

 - `upper <b> <e>`: reemplaza el rango de letras por mayúsculas.
 - `lower <b> <e>`: reemplaza el rango de letras por minúsculas.
 - `replace <b> <e> <p> <q>`: reemplaza en el rango dado toda aparición de
la letra `<p>` por `<q>`.
 - `repeat <b> <e> <t> <i>`: toma el rango de letras e inserta en la
posición `<i>` la repetición del rango `<t>` veces.
 - `rotate <n>`: rota las letras `<n>` posiciones hacia la derecha (si
`<n>` en negativo lo hace a la izquierda). La rotación es un *shift
circular*.
 - `insert <i> <x>`: inserte el texto `<x>` en la posición `<i>`.
 - `delete <b> <e>`{.none}: borra el rango de letras.
 - `revert <n>`: revierte la aplicación de las `<n>` reglas anteriores.
 - `apply <f>`: aplica las reglas de mutación del archivo `<f>`.
 - `print`: imprime el password actual.

La notación `<b> <e>` denota un rango de letras siendo `<b>` el índice
de la primer letra seleccionada y `<e>` de la última.

Los índices `<b>`, `<e>` y `<i>` son 0-based. Si son negativos, el
índice se interpreta de atrás hacia adelante (`-1` es la última letra).

Suponete el siguiente diccionario:

```shell
$ cat dictionary.txt
password
admin
```

Veamos ahora algunos ejemplos de como se ejecutaría `wm`:

```shell
$ cat rules-append-number.txt
insert -1 1
insert -1 !
print
revert 1
insert -1 23
insert -1 !
print

$ ./wm dictionary.txt rules-append-number.txt
password1!
password123!
admin1!
admin123!

$ cat rules-repeat.txt
uppercase 0 0
replace 0 -1 o 0
repeat 0 -1 1 -1
print

$ ./wm dictionary.txt rules-repeat.txt
Passw0rdPassw0rd
AdminAdmin
```

Si queres probar tus reglas podes usar un diccionario como
[`rockyou`](https://en.wikipedia.org/wiki/RockYou) y
crackear este password con [Hashcat](https://hashcat.net/):

```
8ff94d5b6241bc49c8831d0a669b0a8f
```

Suerte!

{% from 'z/templ/figures.j2' import fig %}
{% call fig("out/z/img/xkcd/password_strength_936.png", figparams={'width':'0.85\\textwidth'}) %}
Algo para pensar cuando elijas un password. Créditos por la imagen
a xkcd (936).
{% endcall %}


