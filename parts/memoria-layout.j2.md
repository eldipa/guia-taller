# Layout de memoria

Cuál es el *layout de memoria* de la siguiente estructura?


```cpp
struct icic_t {
    int a;
    char b;
    int c;
    char d;
};
```

Con *layout* me refiero a la organización de los campos `a`, `b`, `c` y
`d` en memoria.

Veamos primero cuál es el tamaño de cada uno de sus atributos:

```cpp
struct icic_t s1;

sizeof(s1.a)
(unsigned long) 4

sizeof(s1.b)
(unsigned long) 1

sizeof(s1.c)
(unsigned long) 4

sizeof(s1.d)
(unsigned long) 1
```

Entonces, cuál es el tamaño en bytes de la estructura `icic_t`?

> 4+1+4+1 = 10 ?

*Nope*. Es 16:

```cpp
sizeof(s1)
(unsigned long) 16
```

Cómo es posible? Veamos primero *en donde* están los atributos en esos
16 bytes.

Lo que voy a hacer es escribir `0xff` en todos los bytes que componen a la
estructura y luego imprimirlos.

```cpp
memset(&s1, 0xff, sizeof(s1));

hexview(&s1, sizeof(s1))
0x7f371cb36010: ff ff ff ff
0x7f371cb36014: ff ff ff ff
0x7f371cb36018: ff ff ff ff
0x7f371cb3601c: ff ff ff ff
```

`hexview()` es una pequeña función utilitaria de mi creación; no la
encontrarás en la librería estándar:

```cpp
void hexview(const void* mem, size_t sz) {
    size_t i = 0;
    for (; i < sz; ++i) {
        if (i % 4 == 0)
            printf("%p: ", &((const unsigned char*)mem)[i]);

        printf("%02x ", ((const unsigned char*)mem)[i]);

        if ((i+1) % 4 == 0)
            printf("\n");
    }

    if (i % 4 != 0)
        printf("\n");
}
```

Ahora, veamos que sucede si escribo un valor distinto en cada atributo.

```cpp
s1.a = 1
s1.b = 2
s1.c = 3
s1.d = 4

hexview(&s1, sizeof(s1));
0x7f371cb36010: 01 00 00 00
0x7f371cb36014: 02 ff ff ff
0x7f371cb36018: 03 00 00 00
0x7f371cb3601c: 04 ff ff ff
```

Bien, esto es peculiar!

Primero, en memoria el `int` 1 es representado por los bytes `01 00 00
00`. El byte menos significativo está primero por lo que la máquina es
*little endian*.

> "Arranca por el byte más 'chico'"

Luego viene `s1.b` con 1 byte.

No es una novedad.

Lo que si es una novedad es que `s1.c` no este *inmediatamente* después de
`s1.b`. No son consecutivos.

Vemos que hay 3 bytes que no fueron tocados entre ambos: `ff ff ff`.

Esto es lo que se conoce como **padding**. Es memoria que el compilador
reserva para que los campos de la estructura estén **alineados**: que
sus respectivas direcciones sean tales que permitan el acceso más rápido.

Es lo que uno llamaría el *alineamiento natural*, si me permitís
filosofar un poco.

Eso se puede ver en las direcciones de cada atributo de `s1`. Verás como
todas son múltiplos de 4:

```cpp
&s1.a
(int *) 0x7f371cb36010
&s1.b
(int *) 0x7f371cb36014
&s1.c
(int *) 0x7f371cb36018
&s1.d
(int *) 0x7f371cb3601c
```

Pero por qué 4? Es siempre así? Para qué alinear las cosas?

## Alineación

Bien, un micro puede acceder mucho más rápido a la memoria alineada.

Para que te des una idea este es el
[código en ARM64](https://gcc.godbolt.org/z/G1WhPdoKG) que inicializa `s1`:


```nasm
  mov     r3, #1
  str     r3, [fp, #-20]  ; s1.a = 1

  mov     r3, #2
  strb    r3, [fp, #-16]  ; s1.b = 2

  mov     r3, #3
  str     r3, [fp, #-12]  ; s1.c = 3

  mov     r3, #4
  strb    r3, [fp, #-8]  ; s1.d = 4
```

No es necesario entender exactamente ese código. Es suficiente con que
veas cuanto código hay que ejecutar para escribir en un `struct`
*alineado*: solo 2 instrucciones para setear un atributo alineado.

Y si no se estuviera alineado?

Un `int` que no está alineado significa que el `int`
está usando algunos bytes de una palabra y otros de la siguiente
palabra.

```cpp;diagram
:                   :                   :
:    |------- int -------| (desalineado):
|------- int -------| (alineado)        :
:                   :                   :
|----- palabra -----|----- palabra -----|
0    1    2    3    4    5    6    7    8
```

Para leer un `int` desalineado el micro tendrá que leer una palabra,
tomar de ella algunos bytes, leer la siguiente palabra, tomar otros
bytes y luego combinar ambos para obtener el `int` pedido.

*Más trabajo, más lento.*

[Para darte una idea](https://gcc.godbolt.org/z/1E5sa3WKv),
este es el mismo código que el anterior pero con el
`struct` alineado a 1 byte (y no a 4).

```nasm
  mov     r3, #1
  str     r3, [fp, #-16]  ; p1.a = 1

  mov     r3, #2
  strb    r3, [fp, #-12]  ; p1.b = 2

  ldr     r3, [fp, #-12]
  and     r3, r3, #255
  orr     r3, r3, #768
  str     r3, [fp, #-12]
  mov     r3, #0
  strb    r3, [fp, #-8]  ; p1.c = 3 ? no es tan fácil de verlo o si?

  mov     r3, #4
  strb    r3, [fp, #-7]  ; p1.d = 4
```

Notarás que hay mucho más código involucrado cuando el atributo no está
alineado.

La alineación y el padding están presentes en varios lados:

 - los atributos de un `struct` están alienados.
 - las variables del stack están alineadas.
 - los parámetros de las funciones están alineados.

En la mayoría de los casos el compilador pondrá la alineación correcta
para que nuestros programas sean rápidos.

No hacerlo haría el código más lento y en ciertas arquitecturas
acceder a datos desalineados terminaría en un crash.


#### Ejercicios

{{ ej() }}

Mirá en [gcc.godbolt](https://gcc.godbolt.org) como es el código
assembly del acceso a atributos alineados y desalineados en 2
arquitecturas a tu elección.

{{ proj("Medición de performance") }}

Armate un programa que incremente en 1 los elementos de un array varias
veces y mida el tiempo que requirió una iteración.

Algo así:

```cpp
#define ROUNDS 100
uint64_t test_uint32_t(uint32_t *buf, size_t num_elems) {
    uint64_t minimum_time = UINT64_MAX;

    for (size_t r = 0; r < ROUNDS; ++r) {
        struct timespec begin, end;
        clock_gettime(CLOCK_MONOTONIC, &begin);
        for (size_t i = 0; i < num_elems; ++i)
            ++buf[i];
        clock_gettime(CLOCK_MONOTONIC, &end);

        // calcular el tiempo entre 'end' y 'begin' en
        // nanosegundos y guardar en 'minimum_time' el
        // mínimo entre este y el anterior.
    }

    return minimum_time;
}
```

El programa deberá reservar memoria en el heap y llamar a `test_uint32_t`
varias veces cambiando el puntero `buf` incrementándolo con
offsets incrementales.

```cpp
#define SLACK 8
int main(int argc, char* argv[]) {
    const size_t buf_sz = /* por argumento */
    uint8_t *buf = malloc(buf_sz * sizeof(*buf));

    const size_t num_elems = (buf_sz / sizeof(uint32_t)) - SLACK;

    // imprimir los resultados de ...
    test_uint32_t((uint32_t*) (buf + 0), num_elems);
    test_uint32_t((uint32_t*) (buf + 1), num_elems);
    test_uint32_t((uint32_t*) (buf + 2), num_elems);
    test_uint32_t((uint32_t*) (buf + 3), num_elems);
    test_uint32_t((uint32_t*) (buf + 4), num_elems);
    test_uint32_t((uint32_t*) (buf + 5), num_elems);
    test_uint32_t((uint32_t*) (buf + 6), num_elems);
    test_uint32_t((uint32_t*) (buf + 7), num_elems);
    free(buf);
    return 0;
}
```

`malloc` retorna un puntero alineado: *"suitably aligned for any built-in
type"* según su [página de
manual](https://man7.org/linux/man-pages/man3/malloc.3.html).

Salvo con los offsets múltiplos de 4, `test_uint32_t` recibe un buffer
desalineado.

Cuáles son los tiempos para cada offset para un buffer de 1024 bytes?

Tomando como referencia el tiempo para el offset 0, cuál es la
diferencia respecto a los otros offsets en términos porcentuales (aka
"para el offset 1 el tiempo fue +20% más lento") ?

Y para buffers de 2048, 4096, 8192 y 16384 bytes?

Y si en vez de `uint32_t` usaras `uint16_t` ? y `uint64_t` ?

Extra: armate un versión template `uint64_t test(T *buf, size_t num_elems)`

#### Lecturas adicionales

 - [Data alignment: Straighten up and fly right](https://developer.ibm.com/articles/pa-dalign/)

## Alineación natural

Queda preguntarse cuál es la alineación correcta en un `struct`?

Es siempre 4 bytes?

El hecho es que **depende de la arquitectura y de los flags del
compilador**.

La alineación debería ser tal que el atributo, según su tipo, no
requiera un acceso desalineado.

En otras palabras, se pondrá tanto padding como el necesario para que el
atributo quede alineado.

Exactamente *"que un atributo quede alineado"* **depende** de la
arquitectura y del size del atributo.

En **mi** caso obtuve los siguientes sizes y direcciones (offsets) de
cada atributo:

```cpp
struct dii_t {  // size  addr
    double a;   // 8     0x00 múltiplo de a 8
    int b;      // 4     0x08 múltiplo de a 4
    int c;      // 4     0x0c múltiplo de a 4
};

sizeof(struct dii_t);   // size múltiplo de 8
(unsigned long) 16

struct idi_t {  // size  addr
    int a;      // 4     0x00 múltiplo de 4
    double b;   // 8     0x08 múltiplo de 8; se necesitaron +4 de padding
    int c;      // 4     0x10 múltiplo de 4
};

sizeof(struct idi_t);   // size múltiplo de 8
(unsigned long) 24

struct ssd_t {  // size  addr
    short a;    // 2     0x00 múltiplo de 2
    short b;    // 2     0x02 múltiplo de 2; se necesitaron +4 de padding
    double c;   // 8     0x08 múltiplo de 8
};

sizeof(struct ssd_t);   // size múltiplo de 8
(unsigned long) 16

struct csc_t {  // size  addr
    char a;     // 1     0x00 múltiplo de 1
    short b;    // 2     0x02 múltiplo de 2; se necesitaron +1 de padding
    char c;     // 1     0x04 múltiplo de 1
};

sizeof(struct csc_t);   // size múltiplo de 2
(unsigned long) 6
```

Por ejemplo, el atributo `b` de `struct csc_t` es un `short` de 2 bytes y su
dirección alienada sería un múltiplo de 2. De ahí que el entre el
atributo anterior de 1 byte y `b` se agregue un byte de padding.

> El size del atributo built-in más largo **no** determina la alineación
> en general. La alineación es según el size de cada atributo.

Lo que sí, el size del atributo más largo determina el padding del final
del `struct`.

Considerá a `struct csc_t`. Debería tener un size de 5 bytes
incluyendo el padding **interno** pero su size es de 6 bytes.

Tiene 1 byte de padding **al final**.

Para qué? Para alinear al *siguiente* `struct` en el caso que se tenga
un array (`struct csc_t x[2];`).

Si el compilador no hiciera eso, los atributos del siguiente `struct`
quedarían desalineados.


```cpp;diagram
|------------- x[0] ----------|------------- x[1] ----------|
|char|    |- short -|char|    |char|    |- short -|char|    :
:    :    :         :    :    :    :    :         :    :    :
|----|----|----|----|----|----|----|----|----|----|----|----|
0    1    2    3    4    5    6    7    8    9   10   11   12
                _________|----|         ^___________
               /                                    \
(gracias al padding al final del struct, x[1] queda alineado)

|------------- x[0] -----|------------- x[1] -----|
|char|    |- short -|char|char|    |- short -|char|
:    :    :         :    :    :    :         :    :
|----|----|----|----|----|----|----|----|----|----|----|----|
0    1    2    3    4    5    6    7    8    9   10   11   12
                                   ^___________
                                               \
(si no estuviera dicho padding, x[1] quedaría desalineado)
```

#### Fun fact

Cuánto debería dar `sizeof(struct id_t)`?

```cpp
struct id_t {
    int i;
    double d;
};
```

Haciendo cuentas debería dar 16 bytes. Y en **mi** caso es así **salvo**
cuando compilo en 32 bits.

En 32 bits esa estructura mide 12 bytes: el `double` *no* queda alineado
a un múltiplo de 8.

> La alineación y padding **dependen de la arquitectura y de los flags del
> compilador**.


#### Ejercicios

{{ ej() }}

Tomá las estructuras `dii_t`, `idi_t`, `ssd_t`, `csc_t` y `id_t` mencionadas
arriba y verificá su tamaño con `sizeof`, el tamaño de cada uno de sus
atributos y el *offset* de cada atributo respecto al principio de la
estructura.

Tip: podés calcular el offset instanciando la estructura y calculando la
diferencia entre las direcciones de cada atributo contra el primero o
bien podés usar `offsetof` si tu compilador lo soporta.

{{ ej() }}

Reordená los atributos de las estructuras `dii_t`, `idi_t`,
`ssd_t`, `csc_t` y `id_t` tal que su size sea el mínimo.

Técnicas como estas pueden ahorrar **mucha** memoria si el programa hace un
uso intensivo de `struct`.

Tip: `double > int > short > char`

{{ ej() }}

Cuál es el size y los offsets de estas estructuras?

```cpp
struct sp_t {
    short a;
    void *p;
};

struct sc2_t {
    short a;
    char b[15];
};
```

Cómo afecta al layout un puntero? Y un array?

{{ ej() }}

Explícito es mejor que implícito.

Saber que `struct id_t` tiene cierto layout está bien, pero cuando es
como aun así depende del compilador, es mejor poner un *static assert*.

*Verificar es mejor que suponer*.

Poné un [`static_assert`](https://en.cppreference.com/w/cpp/language/static_assert)
para asegurarte
que tu `struct` tenga el tamaño esperado.

{{ ej() }}

Compilá en 64 y en 32 bits el ejercicio anterior con el *static assert*
sobre `struct id_t`. Qué resultados obtuviste?

Hacé lo mismo para `struct sp_t`.


## Alineación y *packed*

Cuando se necesita certeza, lo mejor es indicarle al compilador que se
desea una alineación específica. No es algo estándar
de C pero virtualmente todos los compiladores lo permiten.

Por ejemplo si queremos una estructura *compacta* sin padding, lo que
queremos es que los atributos estén alineados a 1 byte o **packed**:

```cpp
struct icic_packed_t {
    int a;
    char b;
    int c;
    char d;
} __attribute__((packed));
```

El [tag](https://gcc.gnu.org/onlinedocs/gcc-3.3/gcc/Type-Attributes.html)
`__attribute__((packed))`
le indica a `GCC` que los atributos del
`struct` deben estar alineados a 1 byte. También funciona para `clang`,
otros compiladores pueden tener alguna notación similar.

```cpp
struct icic_packed_t p1;
memset(&p1, 0xff, sizeof(p1));

p1.a = 1;
p1.b = 2;
p1.c = 3;
p1.d = 4;

hexview(&p1, sizeof(p1))
0x7ff1dd74d020: 01 00 00 00
0x7ff1dd74d024: 02 03 00 00
0x7ff1dd74d028: 00 04

sizeof(p1)
(unsigned long) 10
```

Como verás, ahora sí la estructura tiene 10 bytes. Ningún byte de
padding.

Es común encontrarse estructuras compactas, alienadas a 1 byte, en
paquetes de red y en los formatos de los archivos.

Son estructuras para *transferir datos* por lo que se prioriza el
espacio por sobre la velocidad de acceso a los atributos.

Y si querés un acceso rápido, alineado, combinado con un layout
compacto?

Jaja, todo no se puede! Pero si realmente necesitas acceso rápidos podés
usar 2 estructuras, una compacta y la otra no y copiar de una a la otra.

```cpp
read_from_file(&p1, file); // El formato del archivo es compacto

s1.a = p1.a;    // Hacemos la copia a una estructura
s1.b = p1.b;    // que está alineada al tamaño natural
s1.c = p1.c;    // Pagamos el costo de acceder a atributos desalineados
s1.d = p1.d;    // y la copia una sola vez

process(&s1);   // Hacemos uso de una estructura alineada y "más rápida"
```


#### Ejercicios

{{ ej() }}

Cuál *crees* que es el tamaño de `struct icic_t s_arr[10]`? Y el de `struct
icic_packed_t p_arr[10]`? Verificá si acertaste o no.

{{ ej(hazard=True, tricky=True) }}

Toma la siguiente estructura alineada a 4 bytes ya inicializada:

```cpp
struct icic_t s2 = { .a=1, .b=2, .c=3, .d=4 };
```

Ahora create una función que guarde en los bytes de padding un mensaje
secreto.

```cpp
save_secret(&s2, "cookie");
```

Tip: si casteas `&s2` a un `char *` podrás leer y escribir de a un byte
ignorando el hecho de que `s2` es un `struct icic_t`. Si sabes cuáles son los
bytes de padding podrás ocultar información ahí.

El resultado debería ser el siguiente:

```cpp
hexview(&s2, sizeof(s2));
0x7f371cb36010: 01 00 00 00
0x7f371cb36014: 02 63 6f 6f
0x7f371cb36018: 03 00 00 00
0x7f371cb3601c: 04 6b 69 65
```

De más esta decir que `save_secret` **es un hack** y que funcionará sólo
bajo condiciones **muy especificas** de arquitectura y compilador.

{{ ej(hazard=True) }}

Los paquetes de red Ethernet son los bloques de transmisión elementales
que le dan vida a nuestras redes modernas.

El protocolo establece un límite mínimo para estos paquetes de 64 bytes.

```cpp
void send_pkt(const char *pkt, size_t sz) {
    char min_pkt[64];
    if (sz < 64) {
        // Copiar el paquete a un buffer de tamaño 64, el mínimo
        // impuesto por el protocolo Ethernet
        memcpy(min_pkt, pkt, sz);
        sz = 64;

        // El paquete a enviar es ahora nuestro buffer privado
        // que sabemos que tiene 64 bytes
        pkt = min_pkt;
    }

    assert(sz >= 64);
    send_pkt_to_network(pkt, sz);
}
```

Como verás si el paquete original `pkt` es más chico que el mínimo, la
función usa `min_pkt`. La diferencia entre el tamaño de ambos es
*padding*.

Imaginate ahora el siguiente código de juguete:

```cpp
void send_pkt_to_network(const char *pkt, size_t sz) {
    // hexview aquí
}

void nothing() {
    char buf[] = "echos from the past echos from the past echos from the past echos";
    return;
}

int main() {
    nothing();
    send_pkt("ethernet pkt here", 17);
}
```

Verificá con `hexview` qué se está
enviando realmente. Solo el paquete original `"ethernet pkt here"` o
algo más?

Podés profundizar leyendo [@Arkin-EtherLeak] y [@SilenceWire, capítulo
6]


{{ ej(tricky=True) }}

El formato de archivo de las
imágenes [BMP](https://en.wikipedia.org/wiki/BMP_file_format)
tiene tres estructuras: `struct bitmap_header`, `struct dib_header`
y la imagen en sí en `struct pixel_storage`.

Implementate un programa que reciba una imagen por línea de comandos y
genere otra imagen espejada en el eje horizontal y en el vertical.

Para simplificar, asumí que el archivo *no* tiene compresión,
ni tiene una tabla de colores (*palette*) y que el formato del pixel es
de 24 bits (3 bytes).

#### Lecturas adicionales

 - [Structure packing](http://www.catb.org/esr/structure-packing/)

