
## Source code

Fenced code block, as in Markdown

```cpp
void inc() {
    ++counter;
    const char* c = "hello world!";
}
```

Parameters are added and separated with `;`.
This is handled by `filters/magic.py3` and they're passed directly
to
[listings](https://es.overleaf.com/learn/latex/Code_listing#Reference_guide)

```nasm;numbers=left;frame=leftline
mov     eax, DWORD PTR counter[rip]
add     eax, 1
mov     DWORD PTR counter[rip], eax
```

### Inline code highlight

Plain inline code **must** be highlighted for C++ automatically `new int[12]`.

Inline with a *class* will be highlighted to that language
`abstract`{.java} (java).

To ensure that something is **not** highlighted, add a non-existent
*class* `new int[12]`{.none}

But plain fenced code **must not** be highlighted:

```
const char* msg = "hello";  // después de la 'o', el compilador
```

## Columns

Use the `on_columns` macro to put two pieces of text side by side into
two or more columns (currently only in 2 columns)

{% from 'templ/columns.j2' import on_columns %}

Code:

{% call(separator) on_columns() %}
```nasm
mov     eax, DWORD PTR counter[rip]
add     eax, 1
mov     DWORD PTR counter[rip], eax
```
{{ separator }}
```cpp
void inc() {
    ++counter;
}
```
{% endcall %}

Text (currently the text cannot span more than one page)

{% call(separator) on_columns() %}
{{ lipsum(min=5, max=10) }}
{{ separator }}
{{ lipsum(min=5, max=10) }}
{% endcall %}

## Graphviz

{% from 'templ/diagrams.j2' import graphviz %}

{% call graphviz() %}
```dot
digraph G {
    a_1-> a_2 -> a_3 -> a_1;
}
```
{% endcall %}

## Exercises and Projects


{{ ej() }}

Create una función ...

{{ ej() }}

Create otra función ...

{{ proj("Medición de performance") }}

Armate un programa que ...

{{ proj("Otra Medición de performance") }}

Armate un otro programa que ...


## Tables

---------------------   ---------------------   -----------------
`strdup`  →  siempre    `strcpy`  →  siempre    `memcpy` →  nunca
`strndup` →  siempre    `strncpy` →  a veces
---------------------   ---------------------   -----------------

## Emoji

Support for emojis in fenced code blocks:

```
// ⚠ alert
// 😈evil
// 💣boom
```

But they **are not** supported in inline codes.

In plain text, no problem: ⚠ alert, 😈evil, 💣boom

## Images

**Without caption**:

{% from 'templ/figures.j2' import fig %}
{% call fig("img/cpp_logo.png") %}{% endcall %}

**With caption at bottom**:

{% call fig("img/cpp_logo.png") %}
Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.
{% endcall %}

**Without caption; text around the figure**:


{% call fig("img/cpp_logo.png", position='left') %}{% endcall %}
Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.

Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.

Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.

**With caption; text around the figure**:

{% call fig("img/cpp_logo.png", position='left') %}
Some caption here bla bla bla
bal bal bal
{% endcall %}
Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.

Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.

Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.

Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.

## Footnotes

Foo bar^[Asumiendo que la función de hash *bla bla bla*.]

Otro bla^[https://foo.com  `int` `mov`{.nasm}]

*Very long are supported but **not** multiline (paragraphs)*:

Otro bla very long^[
Aptent taciti ultrices lobortis natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim. Mus
luctus vulputate netus rutrum nunc, hendrerit euismod nam sed nostra,
taciti nunc vehicula habitant orci class, cubilia auctor pulvinar. Proin
nostra rutrum volutpat, dictumst magnis egestas eleifend natoque varius
orci, urna donec placerat euismod hymenaeos, bibendum sed semper. Tempor
commodo dis nascetur torquent, ac erat ultrices ligula mauris, ac ipsum
volutpat sit aptent ut vivamus, mollis eget tristique. Senectus urna
mauris nam nibh, cum non hendrerit justo.
]


## Citations

Caso de citar a "item1": [see @item1 p. 34-35].

Caso de citar a "item2 y 3": [@item2 p. 30; see also @item3].

Cross-reference of figures ("humanlabel-for-referencing" in this case): [@fig:humanlabel-for-referencing]

