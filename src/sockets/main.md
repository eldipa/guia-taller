#### Ejercicios

##### [ej:]

Implementate una funcion que lea de un socket y retorne una linea de
texto. Esto es, que lea del socket y retorne lo leido hasta que
encuentre un `'\n'`.

```cpp
std::string get_line(Socket& sk);
```

##### [ej:]

Modificá ligeramente la funcion para que retorne lineas que finalizan en
un `char` pasado por parámetro (no necesariamente `'\n'`)

```cpp
std::string get_line(Socket& sk, const char endl='\n');
```

##### [ej:]

Implementate una funcion que lea un socket y retorne un mensaje de texto
delimitado por un string dado por parámetro.

```cpp
std::string get_msg(Socket& sk, const std::string& delim="\n");
```

A diferencia de `get_line`, el delimitador de `get_msg` puede constar de
más de un caracter.

Tip: si el delimitador tuviese N caracteres, `get_msg` seria equivalente
a llamar a `get_line` N veces, 1 por cada caracter del delimitador,
siempre que todas menos la primer línea estén vacías.

##### [ej:]

Implementate una funcion que *escapee* un caracter *prohibido* prefijando otro.

```cpp
std::string escape(
    const std::string& msg,
    const char forbidden,
    const char escape
);
```

La funcion tambien debe *escapear* al caracter de escape.

Algunos ejemplos:

```cpp
escape("foo;bar", ";", "|");
"foo|;bar"

escape("foo;;bar|baz", ";", "|");
"foo|;|;bar||baz"
```

##### [ej:]

Como es de esperarse, implementate ahora la inversa:

```cpp
std::string unescape(
    const std::string& msg,
    const char escape
);
```

Algunos ejemplos:

```cpp
unescape("foo|;bar", "|");
"foo;bar"

unescape("foo|;|;bar||baz", "|");
"foo;;bar|baz"
```

##### [ej:]

Los protocolos de texto rara vez permiten datos binarios crudos. En
cambio suelen *encodear* los datos binarios en texto.

Implementate una funcion que tome cualquier byte que no sea letra o
número y lo reemplaze por el caracter de escape seguido por el byte
encodeado en base 64.

```cpp
std::string encode(
    const std::vector<char>& data,
    const char escape
);
```

Por ejemplo:

```cpp
encode({'h','e','l','l','o','!'}, '%');
hello%21

encode({'f','o','o','%','o','o'}, '%');
foo%25oo
```

##### [ej:]

Implementate ahora `decode`. Imagino que sabras lo que hace.




##### [ej:]

Un *request* HTTP 1.1 consta de una linea con el request en sí seguido
por cero o lineas con los headers y un payload opcional.

Haya o no un payload, luego de los headers le sigue un linea vacia.

Acá hay dos ejemplos con y sin payload. En ambos marqué explicitamente
el fin de línea `"\r\n"`.

```
GET / HTTP/1.1\r\n
Host: www.google.com\r\n
\r\n

POST /new HTTP/1.1\r\n
Host: example.com\r\n
Content-Type: application/x-www-form-urlencoded\r\n
Content-Length: 17\r\n
\r\n
d=%6d%61%67%69%63
```

Usando `get_line`, `get_msg` y `decode`, implementate una funcion que
lea de un socket y retorne una linea con el request, un diccionario con
los headers y un vector de `char` con el payload decodeado.

```cpp
void read_request(
    Socket& skt,
    std::string& req,
    std::map<std::string, std::string>& headers,
    std::vector<char>& payload
);
```

Para el ejemplo del `POST`, `read_request` debería retornar:

 - `req` → `"POST /new HTTP/1.1"`
 - `headers` →
    ```cpp
    {
        "Host" : "example.com",
        "Content-Type" : "application/x-www-form-urlencoded",
        "Content-Length" : "17",
    }
    ```
 - `payload` → `{'d','=','m','a','g','i','c'}`

##### [ej:]

Armate un par de funciones para enviar y recibir `std::list<int>` y
`std::map<std::string, std::string>` a traves de un socket usando
[JSON](https://es.wikipedia.org/wiki/JSON).

Hay varias librerias para C y C++. Usá la que más te guste.

Tip: vas a tener que enviar algun delimitador despues de cada objeto
JSON para que el receptor del mensaje sepa cuando empieza y termina uno.
Obviamente tendras que elegir un delimitador que sepas que no va a
aparecer en el JSON para que el receptor no se lo confunda (y vos no
tengas que hacer el escapeo)
Ironicamente, un byte que no sea texto, como `'\0'`, es perfecto.

##### [ej:]

Modificá la siguiente estructura para garantizar que `type` sea de 8
bits sin signo, `size` sea de 32 bits sin signo y `data` sea un puntero
a enteros de 8 bits sin signo.

Garantizar ademas que la estructura no tienen padding.

```cpp
struct msg_t {
    char type;
    int size;
    char *data;
};
```

Tip: usar `<stdint.h>`


##### [ej:]

Implementate ahora una funcion que lea un `struct msg_t`. Esto es, que
lea 1 bytes (`type`), 4 bytes (`size`) y luego lea N bytes donde N es el
valor `size`.

Suponiendo que `size` esta en big endian, deberas convertirlo al
endianess de tu máquina.

```cpp
struct msg_t* recv_msg(Socket& skt);
```

##### [ej:]

Supongamos que queremos enviar strings de longitud variable y encodeamos
sus longitudes en un `uint16_t`.

Implementate entonces:

```cpp
void send_str(Socket& skt, const std::string& str);
```

Supone que la longitud deba ser enviada en big endian.


##### [ej:]

Para strings chicos `uint16_t` es demasiado grande y `uint8_t` ya
alcanzaria.

Modificá `send_str` para que envia un string encodeando su longitud en
un `uint8_t` o en un `uint16_t` si la longitud es chica y puede ser
representada en un `uint8_t` o no.

##### [ej:]

Ahora implementate la funcion para leer un string que fue enviada por
`send_str` del ejercicio anterior.

```cpp
std::string recv_str(Socket& skt);
```

Tip: de alguna manera tendrás que deducir a partir del primer byte si se
trata de un string cuya longitud fue encodeada en un `uint8_t` o en un
`uint16_t`. Lo más fácil es que el primer byte tenga el bit mas
significativo en 0 si se uso `uint8_t` o en 1 si se uso `uint16_t`.

Puede que tengas que modificar `send_str` si este detalle no lo tuviste
en cuenta.

##### [ej:]

Armate un par de funciones para enviar y recibir `std::list<int>` y
`std::map<std::string, std::string>` a traves de un socket usando
[MessagePack](https://github.com/msgpack).





Nos queda un problema practico a resolver. Con IP sabemos como rutear y
hacer llegar datos de una máquina a la otra y con TCP sabemos como hacer
para que el delivery sea confiable.

Pero como podemos saber cual es la direccion IP y puerto del
destinatario?.

Es fácil recordar nombres simbolicos como `google.com`, no así una IP
`172.217.172.110` y menos aun una IPv6 que tiene 16 bytes.

*Domain Name System* o DNS es un servicio que funciona como la lista de
contactos de tu celular solo que en vez de mappear nombres de personas a
numeros de telefono, DNS mappea nombres de máquinas a direcciones IP.

Digamos que queremos saber la direccion de `google.com`. Podemos usar
herramientas como `dig` y `nslookup` para hacer la query o en la jerga,
*resolver un dominio*.

```shell
$ nslookup google.com
Server:         8.8.8.8
Address:        8.8.8.8#53

Non-authoritative answer:
Name:   google.com
Address: 172.217.173.14
Name:   google.com
Address: 2800:3f0:4002:801::200e
```

`nslookup` nos retornó 2 IPs: `172.217.173.14` y `2800:3f0:4002:801::200e`

Cada nombre de máquina o *dominio* puede mappearse a mas de una
direccion. Por ejemplo cuando el host soporta tanto IPv4 como IPv6 como
fue este caso.

Otro escenario es cuando detras de un dominio hay multiples máquinas,
todas ofreciendo el mismo servicio. DNS puede retornar la direccion IP
de estas máquinas para que el cliente elija a cual conectarse.

Esta idea de disponer multiples maquinas es por redundancia: si una se
cae, los clientes aun pueden conectarse al resto.

Veamos como obtener estas direcciones de forma programatica.

Historicamente se utilizaba `gethostbyname()` y `getservbyname()`.

Con la llegada de IPv6 se decidió ofrecer una API unificada y
genérica para trabajar tanto con IPv4 como IPv6: `getaddrinfo()`

`getaddrinfo()` *resolverá* un nombre de dominio a una IP usando el
sistema de DNS y *resolverá* un nombre de servicio a un puerto TCP o UDP.

```cpp
int getaddrinfo(
    const char *node,
    const char *service,
    const struct addrinfo *hints,
    struct addrinfo **res
);
```

Los 2 primeros argumentos corresponden al dominio y servicio que
queremos resolver.

El último argumento, `res` es un puntero a una lista: `getaddrinfo` no
retorna una sino varias respuestas por lo que la funcion alloca espacio
(presuntamente en el heap) y las retorna.

Como todo recurso esta en nosotros **liberarlo** con `freeaddrinfo`.

Y `hints` ? `getaddrinfo` puede retornar varios resultados pero eso no
significa que estemos interesados en todos ellos.

Si queremos usar TCP, no nos interesa UDP.

Aqui es donde entra `hints`: ponemos que tipo de
direcciones estamos buscando en `hints` y `getaddrinfo` hará el filtrado
por nosotros.


```cpp
struct addrinfo hints;
struct addrinfo *result, *rp;

// Definimos a `hints` para buscar solo direcciones IPv4 para TCP
memset(&hints, 0, sizeof(struct addrinfo));
hints.ai_family = AF_INET;  /* Símbolo para IPv4 */
hints.ai_socktype = SOCK_STREAM; /* Símbolo para TCP */

// Hacemos el lookup o resolución de google.com para el servicio HTTP
int s = getaddrinfo("google.com", "http", &hints, &result);
if (s != 0) {
    fprintf(stderr, "Address lookup failed: %s\n", gai_strerror(s));
    // exit
}

// Iteramos para cada respuesta.
for (rp = result; rp != NULL; rp = rp->ai_next) {
    // ...  XXX
}

// Liberamos la lista
freeaddrinfo(result);
```




El sistema de DNS es un esfuerzo coordinados de los paises.

getaddrinfo

Texto o binario?

HTTP 1.1 -> texto
HTTP 2 -> binario ???
HTTP 3 -> binario basado en QUIC ???


Banner grabber
Proxy
NAT
