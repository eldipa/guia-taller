
XXX intro sobre Linux COW: es un ejemplo de como las RCs pueden quedar
latentes por años incluso hasta ser subestimadas pero eventualmente
pueden explotar de maneras sorprendentes.


Analicemos primero un ejemplo mucho mas simple. El hilo principal
lanza dos hilos `t1` y `t2` que ambos llamaran a la funcion `inc()`.

```cpp
int counter = 0;

void inc() {
    ++counter;
}

int main(int argc, char* argv[]) {
    std::thread t1 {inc};
    std::thread t2 {inc};

    t1.join(); t2.join();
    return counter;
}
```

Dado que `counter` esta inicialmente en `0`. Que valor deberia tener al
finalizar el programa? Esto es, cuando `t1` y `t2` terminaron de llamar a
`inc()`?

2? Deberia, no?

La funcion `inc()` ejecuta una unica instruccion de C++ pero esto no
significa que la CPU ejecute una sola instruccion. En x86_64 son 3.

{% from 'templ/columns.j2' import on_columns %}

{% call(separator) on_columns() %}
```cpp
void inc() {
    ++counter;
}
```
{{ separator }}
```nasm
mov     eax, DWORD PTR counter[rip]
add     eax, 1
mov     DWORD PTR counter[rip], eax
```
{% endcall %}



https://godbolt.org/z/vY5csbas8

Esto se debe a que los micros actuales no operan sobre la memoria sino
sobre los registros que estan el mismo micro.

Asi el primer `mov`{.nasm} se trae el valor de
`counter` y lo guarda en el registro `eax`{.nasm}.

`add`{.nasm} incrementa en 1 el registro pero no modifica la variable.

Es recien en el segundo y ultimo `mov`{.nasm} que el valor de
`eax`{.nasm} es guardado en memoria en la variable `counter`.



{% call(separator) on_columns() %}
```nasm;numbers=left;frame=leftline
mov     eax, DWORD PTR counter[rip]
add     eax, 1
- - - - - - - - -
- - - - - - - - -
- - - - - - - - -
mov     DWORD PTR counter[rip], eax
```
{{ separator }}
```nasm;numbers=left;frame=leftline
- - - - - - - - -
- - - - - - - - -
mov     eax, DWORD PTR counter[rip]
add     eax, 1
mov     DWORD PTR counter[rip], eax
- - - - - - - - -
```
{% endcall %}



```cpp
int counter = 0;
std::mutex m;

void inc() {
    m.lock();
    ++counter;
    m.unlock();
}
```

{% call(separator) on_columns() %}
```nasm;numbers=left;frame=leftline
set     DWORD PTR mx[rip]
mov     eax, DWORD PTR counter[rip]
add     eax, 1
- - - - - - - - -
mov     DWORD PTR counter[rip], eax
del     DWORD PTR mx[rip]
- - - - - - - - -
- - - - - - - - -
- - - - - - - - -
- - - - - - - - -
- - - - - - - - -
```
{{ separator }}
```nasm;numbers=left;frame=leftline
- - - - - - - - -
- - - - - - - - -
- - - - - - - - -
set     DWORD PTR mx[rip]
- - - - - - - - -
- - - - - - - - -
set     DWORD PTR mx[rip]
mov     eax, DWORD PTR counter[rip]
add     eax, 1
mov     DWORD PTR counter[rip], eax
del     DWORD PTR mx[rip]
```
{% endcall %}



https://github.blog/2020-08-13-why-write-adrs/
