```{=latex}
\appendix
```

# Internal Reference

#### Inline code highlight

Plain inline code **must** be highlighted for C++ automatically `new int[12]`.

Inline with a *class* will be highlighted to that language
`abstract`{.java} (java).

To ensure that something is **not** highlighted, add a non-existent
*class* `new int[12]`{.nonexistent}

#### Fenced code highlight

Fenced code with a language like `'''cpp`{.nonexistent} **must** be highlighted:

```cpp
const char* msg = "hello";  // después de la 'o', el compilador
```

But plain fenced code **must not** be highlighted:

```
const char* msg = "hello";  // después de la 'o', el compilador
```

#### Tables

---------------------   ---------------------   -----------------
`strdup`  →  siempre    `strcpy`  →  siempre    `memcpy` →  nunca
`strndup` →  siempre    `strncpy` →  a veces
---------------------   ---------------------   -----------------

#### Emoji

Support for emojis in fenced code blocks:

```
// ⚠ alert
// 😈evil
// 💣boom
```

In inline code: `⚠ alert`, `😈evil`, `💣boom`

In plain text: ⚠ alert, 😈evil, 💣boom

#### Images

Include an image with a caption (optional). The caption **must not**
have an hyperlink (it does not work).

```
<x-img~~ src="!path images/xkcd/password_strength_936.png">
Caption text here.
</x-img~~>
```

<x-img src="!path images/xkcd/password_strength_936.png">
Caption text here.
</x-img>

#### Footnotes

Foo bar^[Asumiendo que la función de hash *bla bla bla*.]

#### Exercises and Projects

Exercises headers **must** be replaced by a `Ej C.N:` where `C` is the
chapter number and `N` is the exercise number.

##### [ej:]
Foo bar

```
##### [ej:]
Foo bar
```

Projects follows the same pattern with an optional title: `Proj C.N:` and
`Proj C.N Title:`

##### [proj:]
Without title

```
##### [proj:]
Without title
```

##### [proj: A Title]
Space ......^......^ must NOT be a space
mandatory ...

```
##### [proj: A Title]
Space       ^      ^ must NOT be a space
mandatory  -|
```
