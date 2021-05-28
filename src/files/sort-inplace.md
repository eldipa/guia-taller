#### Challenge: ordenar las líneas de un archivo *inplace*

Todos hemos aprendido el mítico `bubblesort` uno de los **peores**
algoritmos de ordenamiento.

> *"I think the bubble sort would be the wrong way to go."*
> [Barack Obama](https://www.youtube.com/watch?v=koMpGeZpu4Q).

Pero he aquí un caso en donde brilla.

Se tiene un archivo con una palabra en cada línea y se quiere ordenar
este archivo **inplace**, esto es: moviendo las líneas de lugar dentro
del archivo sin usar ningún archivo temporal y sin cargar todo el
archivo a memoria.

*Ready for the challenge?*

**[Spoiler alert]** A continuación esta mi solución.

```cpp
#include <stdio.h>
#include <string.h>

#define BUFSZ 512

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    FILE* f = fopen(argv[1], "r+t");
    if (!f) return 2;

    // double buffer
    char buf[2][BUFSZ];

    int changed;
    do {
        changed = 0;
        int i = 0;

        long prev_word_pos = ftell(f);
        char* prev_word = fgets(buf[i % 2], BUFSZ, f);
        if (!prev_word) break;
        ++i;
        while (1) {
            long cur_word_pos = ftell(f);
            char* cur_word = fgets(buf[i % 2], BUFSZ, f);
            if (!cur_word) break;
            ++i;
            if (strncmp(prev_word, cur_word, BUFSZ) > 0) {
                fseek(f, prev_word_pos, SEEK_SET);

                fputs(cur_word, f);
                cur_word_pos = ftell(f); // update the new "cur" word position
                fputs(prev_word, f);
                strncpy(cur_word, prev_word, BUFSZ-1); // update "cur" word
                cur_word[BUFSZ-1] = 0;
                changed = 1;
            }

            prev_word_pos = cur_word_pos;
            prev_word = cur_word;
        }

        fseek(f, 0, SEEK_SET); // restart
    } while (changed);

    fclose(f);
    return 0;
}
```
