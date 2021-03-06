{% from 'z/templ/columns.j2' import on_columns %}
{% from 'z/templ/diagrams.j2' import graphviz %}
{% from 'z/templ/exercises.j2' import exercises %}
{% from 'z/templ/figures.j2' import fig %}
{% from 'z/templ/boxes.j2' import extra_footage %}

# Endianness

Cuál de estos dos números es más grande? No hay trampas, estoy hablando
dos números comunes y corrientes como si fueran los precios en un
supermercado:

```cpp
a = 1942
b = 2491
```

Seguro estarás diciendo, `a < b`, el número más grande es 2491.

> *Obvio.*

Pero por qué? Tanto `a` como `b` son el mismo número solo que uno esta
al revés. Es una cuestión *pura de notación*.

La convención dice que el **digito** más a la izquierda es el **más
significativo**, el que pesa más.

Por eso, `1 < 10 < 100 < 1000` porque cuanto más a la izquierda se
esté el `1`, más grande es el número.

Y por eso `2491` es mayor que `1942`.

Volvamos al mundo de la programación.

```cpp
uint32_t c = 0x12345678;
```

Estarás de acuerdo que `c` es un entero sin signo de 4 bytes.
El número es 305419896 en decimal o 0x12345678 en hexadecimal.

Lo bonito de la notación hexadecimal es que es fácil ver
esos 4 bytes uno por uno: `0x12`, `0x34`, `0x56` y `0x78`.

Así como el humano ve *una serie de dígitos como un solo número*,
la máquina ve *una serie de bytes como un solo número*.

Queda preguntarse entonces, la máquina sigue la misma convención que el
humano? Es el byte de más a la izquierda el más significativo?

Esto es, si viéramos a la memoria como un gran array donde las
direcciones de memoria más bajas están a la izquierda
(al principio del array) y las más altas están a la derecha,
como estarían ordenados los bytes de `c`?

Estaría el byte más significativo `0x12` a la izquierda o a la derecha?

```cpp;diagram
                    /------- uint32_t c -----/
char mem[] = { ...., 0x12, 0x34, 0x56, 0x78, ..... }; // big endian
              ^                                   ^
              |                                   |
          dirección                           dirección
          más baja                            más alta
              |                                   |
              v     /------- uint32_t c -----/    v
char mem[] = { ...., 0x78, 0x56, 0x34, 0x12, ..... }; // little endian
```

El hecho es que **depende de la arquitectura!**

En ciertas arquitecturas el byte **más significativo** está a la izquierda,
en las posiciones **más bajas** de la memoria.

Son las llamadas arquitecturas **big endian**.

Por el otro lado están aquellas que ponen el byte **más significativo** a la
derecha, en las posiciones **más altas** de la memoria. Son las arquitecturas
**little endian**.

O lo que es lo mismo, ponen el byte **menos significativo** al
principio.

De acá podemos sacar una regla mnemotécnica: en las arquitecturas **big**
endian el primer byte es el más **grande** (más significativo), en las arquitecturas
**little** endian el primer byte es el más **chico** (menos significativo).

Y no es casualidad.

Ambos términos vienen de la novela
[Gulliver's Travels](https://en.wikipedia.org/wiki/Gulliver%27s_Travels)
en donde había dos países que estaban en guerra por determinar
desde que sección
se debía empezar a abrir un huevo hervido: desde la parte más grande o
desde la parte más chica.

*Big o little end.*


#### Ejercicios
{% call exercises() %}

{{ ej(label='memendianness-get_endianness') }}

Create una función `get_endianness()` que te indique si la máquina es
big o little endian.

Tip: si al número `int32_t n = 42` lo casteas a `char*`, qué
valor debería tener el primer byte apuntado por `char*` en una máquina
big endian? Y en una little endian?

{{ ej(label='memendianness-swap_bytes') }}

Create una función `void swap_bytes(char* mem, size_t sz)` que *swappee* los
bytes del buffer (el primer byte pasa a ser el último, el segundo pasa a
ser el penúltimo, y así sucesivamente).

Armate una variante C++: `void swap_bytes(std::vector<char>& mem)`.
{% endcall %}


## Cuándo el endianness importa?

Independientemente del endianness, las operaciones aritméticas y lógicas
funcionan normalmente. O sea, `(c + 4)  << 2` da el resultado esperado
sea cual sea su representación en bytes.

Pero cuando necesitamos acceder a los bytes es donde el endianness cobra
importancia.

Veamos un caso concreto:

```cpp
#include <stdio.h>
#include <stdint.h>

int main() {
    FILE *f = fopen("cookie", "wb");
    if (!f)
        return 1;

    uint32_t c = 0x12345678;
    fwrite(&c, 4, 1, f);
    fclose(f);

    return 0;
}
```

Si miras el archivo `cookie` con `hexdump` verás los 4 bytes y
*dependiendo del endianness de tu máquina* verás un orden u otro.

Al igual que yo, es probable que tengas un micro little endian
y veas esto:

```shell
$ hexdump -C endianness
00000000  78 56 34 12                                       |xV4.|
00000004
```

Y esto puede ser un problema...

Si compartís el archivo binario y este se abre en una máquina con
el endianness incorrecto, se cargará **cualquier cosa**.

Ni hablar si envias algo por la red.

Tus datos pueden ser interpretados al revés dependiendo del endianness
de la *otra* máquina!

#### Ejercicios
{% call exercises() %}

{{ ej() }}

Un programa *vulnerable* lee 4 bytes de la red y *sin tomar en cuenta el
endianness*, ve a esos bytes con un `uint32_t` y reserva memoria con un
`malloc`.

```cpp
uint32_t sz = read_from_network_the_size();
void *mem = malloc(sz);
```

Si el programa corre en una máquina *big endian*, qué número debería
enviar un atacante para que el programa víctima reserve más de 1 GB ?

> *Ups*
{% endcall %}


## Ok, el endianness puede ser un problema, como solucionarlo?

Hay dos partes: hay que **elegir un endianness en común** y luego hay que
hacer, bueno, que el lector y el escritor lo respeten y sepan hacer la
**conversión** a **sus** respectivos endianness.

### Elección del endianness

Hay dos formas: una simétrica y otra asimétrica.

Cual dictador podes decir que el archivo o la comunicación por red
está en un *endianness particular*, digamos *big endian*  y listo.

Es una regla *simétrica* en la que ambos participantes tendrán que
convertir hacia y desde el endianness elegido.

La mayoría de los protocolos de red binarios escriben los
números en big endian. Fue una decisión arbitraria y muchos protocolos
nuevos siguen con la tradición.

Tan es así que en la jerga a big endian se lo conoce como el
*endianness de la red* o *network order*.

Pero hoy en día la mayoría de los dispositivos son little endian lo que
fuerza tanto al que envía como al que recibe a convertir de un endianness
a otro.

Nuevos formatos como [Cap'n Proto](https://capnproto.org/) y protocolos como
[QUIC](https://en.wikipedia.org/wiki/QUIC) toman ventaja y están en
little endian directamente.


La otra forma es **no** definir un endianness a priori y dejar que el
escritor escriba o envíe por red en **su** endianness, el *endianness
nativo*.

Para que el lector sepa en qué endianness están los datos, el escritor
debe escribir o enviar un número *mágico* conocido por ambos,
digamos `0x12345678`.

Cuando el lector lee los bytes y los ve como un número, compara este
contra `0x12345678`.

Si son iguales, ambos tienen el mismo endianness
y no hay que hacer nada más. Todos felices.

Si son distintos, el lector tendrá que convertir todo lo que lea a **su**
endianness.

Es una regla *asimétrica* en donde uno usa **su** endianness nativo y el
otro hace la conversión.

### Conversión de endianness

Una vez que sabes en qué endianness tenés que escribir o leer unos
datos, hay una serie de funciones listas para ayudarte.

No son parte de la librería estándar de C/C++ pero son parte del
estándar POSIX:

 - `htons`: *host to network - short*, es una función que toma un entero
de 2 bytes en el endianness nativo, del host, y lo convierte a *network
order* o *big endian*.
 - `ntohs`: *network to host - short*, es la función inversa, convierte
un número de 2 bytes en big endian al endianness nativo.
 - `htonl`: *host to network - long*, es igual que `htons` sólo que
opera sobre enteros de 4 bytes.
 - `ntohl`: *network to host - long*, creo que podrás deducirlo.

Leete la [man page byteorder(3)](https://linux.die.net/man/3/byteorder).

Estas funciones nacieron en el contexto de las redes TCP/IP y como verás
sólo trabajan con el endianness de la red^[En realidad la red
no tiene endianness, lo correcto sería decir *"el endianness tradicional
de los protocolos de red".*]: big endian

Hay otra familia de funciones mucho más rica, solo que **no** son
estándar:

 - `htobe16`: *host to big endian - 16 bits*, función que toma un entero
de 2 bytes en el endianness nativo y lo convierte a *big endian*. Es el
equivalente de `htons`.
 - `le16toh`: *little endian to host - 16 bits*, convierte de little
endian al endianness nativo un número de 2 bytes.
 - `be64toh`: *big endian to host - 64 bits*, convierte de big endian al
endianness nativo un número de 8 bytes.

Y hay más. Revisá la [man page endian(3)](https://linux.die.net/man/3/endian).

#### Ejercicios
{% call exercises() %}

{{ ej() }}

Los archivos [pcap](https://wiki.wireshark.org/Development/LibpcapFileFormat)
son un ejemplo de la regla *asimétrica*: en los primeros 4 bytes se
guarda el número mágico `0xa1b2c3d4` en el endianness nativo del escritor.

Será tarea del lector saber si dicho endianness coincide con el suyo
y si deba o no hacer las conversiones.

Y será tarea tuya también!

Create un programa que determine si un archivo
[pcap](https://wiki.wireshark.org/Development/LibpcapFileFormat) está o
no en el endianness de **tu** máquina.

Deberías hacer algo así:

```shell
$ ./pcap_endianness some-pcap-downloaded-from-internet.pcap
The file is in little-endian, the same endianness of the host.
No conversion will be needed.
```

Tip: no es necesario que parsees todo el archivo.


{{ ej() }}

Create una función que tome un entero de 4 bytes en el endianness
de la máquina y lo pase a little endian usando `swap_bytes` y
`get_endianness` (implementadas en los ejercicios
{{ref("ej:memendianness-get_endianness", "ej:memendianness-swap_bytes") }}).

Create otra función que haga la inversa: de little endian al endianness
de la máquina.

{{ ej(tricky=True) }}

Suponete que estas en una arquitectura donde el número `0xaabbccdd` es
visto como la secuencia de bytes `[0xbb, 0xaa, 0xdd, 0xcc]`.

No es
ni big ni little endian, es un *mixed endian*. En particular, es el
endianness de las viejas [PDP-11](https://en.wikipedia.org/wiki/PDP-11).

Extendé `get_endianness()` para detectar este caso también. Armate una
serie de funciones que te conviertan del endianness nativo al mixed
endian números de 2, 4 y 8 bytes y viceversa:

`uint16_t htome16(uint16_t)`, `uint32_t htome32(uint32_t)`,
`uint64_t htome64(uint64_t)`, `uint16_t me16toh(uint16_t)`,
`uint32_t me32toh(uint32_t)`, `uint64_t me64toh(uint64_t)`

{{ ej(hazard=True, tricky=True) }}

*Crazy idea:* reimplementate el siguiente `bubble_sort`
usando `htobe16` o `htole16` en reemplazo del swap.

```cpp
void bubble_sort(char* buf, size_t sz) {
    for (size_t i = 1; i < sz; ++i) {
        for (size_t j = 0; j < sz - i; ++j) {
            if (buf[j] > buf[j+1]) {
                // swap(buf[j], buf[j+1])
            }
        }
    }
}
```

Tip: pensá bien que función tenés que usar según el endianness de la
máquina para resolver **este** ejercicio.
{% endcall %}

#### Lecturas adicionales

 - [Writing endian-independent code in C](https://developer.ibm.com/articles/au-endianc/)

