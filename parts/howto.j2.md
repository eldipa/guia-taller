
## C/C++

Language names:

 - C++
 - C
 - C/C++
 - C/C++.
 - The C/C++ between words

```
In a fenced block C++
```

```cpp
// In cpp fenced block C++
```

In Math: \(C++\)

## Fonts

This is an English text. Y este está en Español.

Cyrilic is supported too: \textrussian{это текст на русском}

The `textrussian{...}` is used to tag the text so the rules of the
given language work (like how to split a word with it doesn't fit a
line).

#### Text styles

Note: in Markdown, the *italics* marker are not just italics
but emphasis that tries to highlight the text based on the context.

Normal text, *important* stuff.

\textbf{Bold text, \emph{important} stuff.}

\textit{Italic text, \emph{important} stuff.}

\underline{Underline text, \emph{important} stuff.}

\textbf{\textit{Bold italic text, \emph{important} stuff.}}

#### Using Latex

Some of the \textbf{greatest}
discoveries in \underline{science}
were made by \textbf{\textit{accident}}, \textit{or not}.

#### Using Markdown (*underline* is not supported here)

Some of the **greatest**
discoveries in science
were made by ***accident***, *or not*.

#### Russian

(latex): \textbf{это} \underline{текст} \textbf{\textit{на}} \textit{русском}

(markdown): **это** текст ***на*** *русском*


### Source code font

Font in the code should be using `Monaco` font (Russian and Unicode Math
are less supported) `const char c[] = "hello!";`:

```cpp
const char c[] = "hello! 0.95 ≈ 1 это текст на русском";
```

## Math

### Math symbols in Text

The font supports math symbols written in plain text:

Normal text (well supported): 0.95 ≈ 1 ∧ 0.5 ⟹  1/2 ∴ ∑ 3 ∃ ≤ 𝚆

Italic (less supported): *0.95 ≈ 1 ∧ 0.5 XXX 1/2 ∴ ∑ 3 ∃ ≤ XXX*

Bold (less supported): **0.95 ≈ 1 ∧ 0.5 XXX 1/2 ∴ ∑ 3 ∃ ≤ XXX**

## Math symbols in Math context

Latex, inline: \( 0.95 \approx 1 \wedge 0.5 \implies 1/2 \therefore \sum 3  \exists \le 𝚆 \)

Unicode, inline: \(0.95 ≈ 1 ∧ 0.5 ⟹  1/2 ∴ ∑ 3 ∃ ≤ 𝚆\)


Latex, block:

\[
0.95 \approx 1 \wedge 0.5 \implies 1/2 \therefore \sum 3  \exists \le 𝚆
\]

Unicode, block:

$$
0.95 ≈ 1 ∧ 0.5 ⟹  1/2 ∴ ∑ 3 ∃ ≤ 𝚆
$$

Use `\(...\)` for *inline* maths and `\[...\]` or `$$...$$` for *block* or
*display* maths.

## Emoji

Support for emojis in fenced code blocks:

```
Normal fenced code
// ⚠ alert
// 😈evil
// 💣boom
```

```cpp
C++ fenced code
// ⚠ alert
// 😈evil
// 💣boom
```

But they **are not** supported in inline codes.

In plain text, no problem: ⚠ alert, 😈evil, 💣boom

Emojis can be added by name using Jinja markup:

What's up {{ emoji('rocket') }}? All right {{ emoji('evil') }}

## Source code

Fenced code block, as in Markdown

```cpp
void inc() {
    ++counter;
    const char* c = "hello world!";
}
```

Parameters are added and separated with `;`.
This is handled by `filters/magic.py3`

```nasm;linenos;frameleft
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

#### Regression tests

This used to break: bla bla `"ethernet pkt here"` bla bla

## Columns

Use the `on_columns` macro to put two pieces of text side by side into
two or more columns (currently only in 2 columns)

{% from 'z/templ/columns.j2' import on_columns %}

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

## Include

Include a block of a file (must be a template, see `src/gfx.j2.c`;
templates should be in `src/` and final files should be in `out/src/`)

```cpp
{{ include_block('out/t/src/gfx.j2.c', 'line_example') }}
```

Include the whole file

```cpp
{{ include_block('out/src/err.h', block=None, strip=False) }}
```

Note: files that are still templates are in `out/t/src` while the files
that were already processed by Jinja2 and they are not longer templates
are in `out/src`.

## Graphviz

{% from 'z/templ/diagrams.j2' import graphviz %}

{% call graphviz() %}
```dot
digraph G {
    a_1-> a_2 -> a_3 -> a_1;
}
```
{% endcall %}

## Exercises and Projects

{% from 'z/templ/exercises.j2' import exercises %}

{% call exercises() %}
{{ ej(label="super1") }}

Create una función ...

{{ ej(label="super2") }}

Create otra función ..

{% endcall %}

{{ proj("Medición de performance", label="medperf") }}

Armate un programa que ...

{{ proj("Otra Medición de performance") }}

Armate un otro programa que ...


## Tables

---------------------   ---------------------   -----------------
`strdup`  →  siempre    `strcpy`  →  siempre    `memcpy` →  nunca
`strndup` →  siempre    `strncpy` →  a veces
---------------------   ---------------------   -----------------

## Images

**Without caption**:

{% from 'z/templ/figures.j2' import fig %}
{% call fig("out/z/img/cpp_logo.png") %}{% endcall %}

**With caption at bottom**:

{% call fig("out/z/img/cpp_logo.png", label='cpp-cap1') %}
Aptent taciti ultrices lobortis
natoque lacus vulputate facilisis,
platea odio praesent justo fermentum, nascetur ultricies enim.
{% endcall %}

**Without caption; text around the figure**:


{% call fig("out/z/img/cpp_logo.png", position='left') %}{% endcall %}
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

{% call fig("out/z/img/cpp_logo.png", position='left', label='cpp-cap2') %}
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


## Extra footage


{% from 'z/templ/boxes.j2' import extra_footage %}

{% call extra_footage() %}
Por que `assert(rdptr >= wrptr)` ? Sabemos que `wrptr` *nunca* va a
sobrepasar a `rdptr`, es un *invariante* del algoritmo.

Pero el código es un ser viviente y lo único
constante es el cambio. Basta con algún error de nuestra parte
o un refactor en el futuro y podemos caer en `wrptr > rdptr`.
{% endcall %}


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

## Cross-References

Cross-reference of figures: {{ ref("fig:cpp-cap1") }} ; {{ref("fig:cpp-cap2")}}

Cross-reference of exercises: {{ref('ej:super1')}} ; {{ref('ej:super2')}}

Cross-reference of projects: {{ref('proj:medperf')}}

Cross-references:

 - On Page: {{page("fig:cpp-cap1") }} ; range: {{page("fig:cpp-cap1", "fig:cpp-cap2") }}
 - Ref Number: {{refnum("fig:cpp-cap1") }} ; range not supported (it should be!!)
 - Fancy ref: {{ref("fig:cpp-cap1") }} ; range: {{ref("fig:cpp-cap1", "fig:cpp-cap2") }}

Cross-references (upper case version for using at the begin of a
sentence):

 - On Page: This is not supported but it should be!
 - Ref Number: not needed, it is just a number
 - Fancy ref: not needed, it begins with a number

Cross-referencing of sections: [@sec:footnotes]

`vref`: \vref{fonts}

`vpageref`: \vpageref{fonts}


