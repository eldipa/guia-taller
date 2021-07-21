// Esta es una serie de mini-ejemplos de como usar SDL2_gfx,
// una libreria para SDL2 que permite dibujar ciertas primitivas
// en pantalla de maner muy simple.
//
// Tener en cuenta que este codigo *NO* hace un buen game loop
// ya que tiene un sleep (SDL_Delay) fijo pero para el proposito
// de mostrar estos mini-ejemplos alcanza.
//
// Compilar con:
// gcc `sdl2-config --cflags` -std=c11 gfx.c -lSDL2 -lSDL2_gfx -o gfx
//
// Ejecutar como:
// gfx example_number

#include <stdio.h>
#include <assert.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>

#define WIDTH 640
#define HEIGHT 480
#define MIN ((HEIGHT < WIDTH) ? HEIGHT : WIDTH)

#define N 7

int main(int argc, char* argv[]) {
    int ret = -1;

    if (argc != 2) {
        fprintf(stderr, "Unexpected argument count.\nUsage:\n  %s example-number\n", argv[0]);
        return ret;
    }

    int example_number = atoi(argv[1]);
    if (!(0 <= example_number && example_number < N)) {
        fprintf(stderr, "Unexpected example number.\n");
        return ret;
    }

    if (SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "SDL_Init failed: %s\n", SDL_GetError());
        return ret;
    }

    SDL_Window *window = SDL_CreateWindow("SDL2 GFX", 100, 100, WIDTH, HEIGHT, SDL_WINDOW_OPENGL);
    if (!window) {
        fprintf(stderr, "SDL_CreateWindow failed: %s\n", SDL_GetError());
        SDL_Quit();
        return ret;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer) {
        fprintf(stderr, "SDL_CreateRenderer failed: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return ret;
    }

    SDL_Event e;
    int begin = 1;

    int quit = 0;
    while (!quit)
    {
        if (SDL_PollEvent(&e))
        {
            if (e.type == SDL_QUIT)
                quit = 1;
        }
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
        SDL_RenderClear(renderer);

        {% block rhombus_params -%}
        const short rhombus_x[] = {WIDTH/2, WIDTH, WIDTH/2, 0};
        const short rhombus_y[] = {0, HEIGHT/2, HEIGHT, HEIGHT/2};
        assert(sizeof(rhombus_x) == sizeof(rhombus_y));
        const int rhombus_n_points = sizeof(rhombus_x)/sizeof(rhombus_x[0]);
        {%- endblock %}

        {% block triangle_params -%}
        const short triangle_x[] = {WIDTH/2, WIDTH, 0};
        const short triangle_y[] = {0, HEIGHT-1, HEIGHT-1}; // offset a little to see the line
        assert(sizeof(triangle_x) == sizeof(triangle_y));
        const int triangle_n_points = sizeof(triangle_x)/sizeof(rhombus_x[0]);
        {%- endblock %}

        switch (example_number) {
            case 0:
                if (begin) printf("Ejemplo de como dibujar lineas\n");
                {% block line_example -%}
                lineRGBA(renderer, 0, 0, WIDTH, HEIGHT, 0xff, 0x00, 0x00, 0xff);
                lineRGBA(renderer, WIDTH, 0, 0, HEIGHT, 0x00, 0xff, 0x00, 0xff);
                lineRGBA(renderer, 0, HEIGHT/2, WIDTH, HEIGHT/2, 0x00, 0x00, 0xff, 0xff);
                {%- endblock %}
                break;
            case 1:
                if (begin) printf("Ejemplo de como dibujar un circulo\n");
                {% block circle_example -%}
                circleRGBA(renderer, WIDTH/2, HEIGHT/2, MIN/2, 0x00, 0xff, 0x00, 0xff);
                {%- endblock %}
                break;
            case 2:
                if (begin) printf("Ejemplo de como dibujar un circulo y rellenarlo\n");
                {% block filled_circle_example -%}
                filledCircleRGBA(renderer, WIDTH/2, HEIGHT/2, MIN/2, 0x00, 0xff, 0x00, 0xff);
                {%- endblock %}
                break;
            case 3:
                if (begin) printf("Ejemplo de como dibujar un rectangulo y rellenarlo traslucido\n");
                {% block alpha_box_example -%}
                boxRGBA(renderer, 0, 0, 100, 100, 0x00, 0xff, 0x00, 0xff);
                boxRGBA(renderer, 50, 50, 150, 150, 0xff, 0x00, 0x00, 0x60);
                {%- endblock %}
                break;
            case 4:
                if (begin) printf("Ejemplo de como dibujar un rombo\n");
                {% block rhombus_example -%}
                polygonRGBA(renderer, rhombus_x, rhombus_y, rhombus_n_points, 0xff, 0x00, 0x00, 0xff);
                {%- endblock %}
                break;
            case 5:
                if (begin) printf("Ejemplo de como dibujar un triangulo\n");
                {% block triangle_example -%}
                polygonRGBA(renderer, triangle_x, triangle_y, triangle_n_points, 0xff, 0x00, 0x00, 0xff);
                {%- endblock %}
                break;
            case 6:
                if (begin) printf("Ejemplo de como dibujar una elipse y rellenarla\n");
                {% block ellipse_example -%}
                filledEllipseRGBA(renderer, WIDTH/2, HEIGHT/2, WIDTH/2, HEIGHT/4, 0xff, 0x00, 0x00, 0xff);
                {%- endblock %}
                break;
            default:
                fprintf(stderr, "Unexpected example number.\n");
                SDL_DestroyRenderer(renderer);
                SDL_DestroyWindow(window);
                SDL_Quit();
                return ret;
        }

        SDL_RenderPresent(renderer);
        SDL_Delay(10);
        begin = 0;
    }

    ret = 0;

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return ret;
}
