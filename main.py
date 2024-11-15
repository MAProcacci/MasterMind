import random
import flet as ft

# Game configuration
colores = ['R', 'G', 'B', 'Y', 'W', 'P', 'O', 'X']
num_fichas = 5

color_map = {
    'R': ft.colors.RED,
    'G': ft.colors.GREEN,
    'B': ft.colors.BLUE,
    'Y': ft.colors.YELLOW,
    'W': ft.colors.WHITE,
    'P': ft.colors.PURPLE,
    'O': ft.colors.ORANGE,
    'X': ft.colors.GREY,
}

def generar_combinacion_secreta(nivel):
    if nivel == 'Fácil':
        return random.sample(colores[:6], num_fichas)
    elif nivel == 'Medio':
        return [random.choice(colores[:7]) for _ in range(num_fichas)]
    elif nivel == 'Difícil':
        return [random.choice(colores) for _ in range(num_fichas)]

def obtener_pistas(combinacion_secreta, intento):
    pistas = []
    intentos_restantes = list(intento)
    secreto_restante = list(combinacion_secreta)

    for i in range(num_fichas):
        if intento[i] == combinacion_secreta[i]:
            pistas.append('X')
            intentos_restantes[i] = None
            secreto_restante[i] = None

    for i in range(num_fichas):
        if intentos_restantes[i] is not None and intentos_restantes[i] in secreto_restante:
            pistas.append('O')
            secreto_restante[secreto_restante.index(intentos_restantes[i])] = None

    return ''.join(sorted(pistas))

def crear_circulo_color(color):
    return ft.Container(
        bgcolor=color_map[color],
        width=20,
        height=20,
        border_radius=10,
    )

def mostrar_snackbar(page, mensaje, color):
    snackbar = ft.SnackBar(
        content=ft.Text(mensaje, color=color, weight=ft.FontWeight.BOLD),
        bgcolor="white",
    )
    page.overlay.append(snackbar)
    snackbar.open = True
    page.update()

def mostrar_titulo_colorido(palabra):
    colores_disponibles = list(color_map.values())
    random.shuffle(colores_disponibles)
    letras_coloridas = [
        ft.Text(
            letra,
            color=colores_disponibles[i % len(colores_disponibles)],
            size=18,
            weight=ft.FontWeight.BOLD
        )
        for i, letra in enumerate(palabra)
    ]
    return ft.Row(letras_coloridas, alignment=ft.MainAxisAlignment.CENTER)

def main(page: ft.Page):
    page.title = "Mastermind"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 800
    page.window.height = 1000

    nivel = 'Fácil'
    intentos_maximos = 6
    combinacion_secreta = generar_combinacion_secreta(nivel)
    intentos = 0
    info_lista = []

    def adivinar(e):
        nonlocal intentos, info_lista
        colores_seleccionados = [circle.content.data for circle in input_circles]

        if None in colores_seleccionados:
            mostrar_snackbar(page, "Debes seleccionar un color para cada círculo.", ft.colors.RED)
            return

        intento = ''.join(colores_seleccionados)

        if len(intento) != num_fichas or not all(c in colores[:6] if nivel == 'Fácil' else (c in colores[:7] if nivel == 'Medio' else c in colores) for c in intento):
            mostrar_snackbar(page, "Combinación inválida. Asegúrate de usar los colores correctos y de la longitud correcta.", ft.colors.RED)
            return

        intentos += 1
        pistas = obtener_pistas(combinacion_secreta, intento)

        if pistas == 'X' * num_fichas:
            mostrar_snackbar(page, f"¡Felicidades! Has adivinado la combinación en {intentos} intentos.", ft.colors.BLUE)
            adivinar_button.disabled = True
            mostrar_combinacion_secreta()
            return

        if intentos >= intentos_maximos:
            mostrar_snackbar(page, f"Lo siento, has agotado tus intentos. La combinación secreta era: {''.join(combinacion_secreta)}", ft.colors.RED)
            adivinar_button.disabled = True
            mostrar_combinacion_secreta()
            return

        intento_circulos = ft.Row([crear_circulo_color(c) for c in intento])
        pistas_texto = ft.Text(f"Pistas: {pistas}", size=20, weight=ft.FontWeight.BOLD)
        info_linea = ft.Row([ft.Text(f"Intento {intentos}: ", size=20, weight=ft.FontWeight.BOLD), intento_circulos, pistas_texto])
        info_lista.append(info_linea)

        info_container.content = ft.Column(info_lista, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        info_container.update()

        for i in range(num_fichas):
            input_circles[i].content = ft.Container(
                bgcolor=ft.colors.BLACK,
                width=50,
                height=50,
                border_radius=25,
                border=ft.border.all(2, ft.colors.CYAN),
                data=None
            )
            input_circles[i].update()

    def mostrar_combinacion_secreta():
        for i in range(num_fichas):
            clave_circles[i].content = ft.Container(
                bgcolor=color_map[combinacion_secreta[i]],
                width=50,
                height=50,
                border_radius=25,
                border=ft.border.all(2, ft.colors.CYAN),
            )
            clave_circles[i].update()

    def cambiar_nivel(e):
        nonlocal nivel, combinacion_secreta, intentos, info_lista
        nivel = nivel_dropdown.value
        combinacion_secreta = generar_combinacion_secreta(nivel)
        intentos = 0
        info_lista = []
        mostrar_snackbar(page, "¡Bienvenido a Mastermind!", ft.colors.BLUE)
        adivinar_button.disabled = False
        for i in range(num_fichas):
            clave_circles[i].content = ft.Container(
                bgcolor=ft.colors.BLACK,
                width=50,
                height=50,
                border_radius=25,
                border=ft.border.all(2, ft.colors.CYAN),
                data=None
            )
            input_circles[i].content = ft.Container(
                bgcolor=ft.colors.BLACK,
                width=50,
                height=50,
                border_radius=25,
                border=ft.border.all(2, ft.colors.CYAN),
                data=None
            )
            clave_circles[i].update()
            input_circles[i].update()
        info_container.content = ft.Column(info_lista, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        info_container.update()
        actualizar_menus_colores()

    def seleccionar_color(color, index):
        input_circles[index].content = ft.Container(
            bgcolor=color_map[color],
            width=50,
            height=50,
            border_radius=25,
            border=ft.border.all(2, ft.colors.CYAN),
            data=color
        )
        input_circles[index].update()
        color_menus[index].open = False
        color_menus[index].update()

    def actualizar_menus_colores():
        colores_disponibles = colores[:6] if nivel == 'Fácil' else (colores[:7] if nivel == 'Medio' else colores)
        for i in range(num_fichas):
            color_menus[i].items = [
                ft.PopupMenuItem(
                    content=ft.Container(
                        bgcolor=color_map[color],
                        width=50,
                        height=50,
                        border_radius=25,
                    ),
                    on_click=lambda e, color=color, index=i: seleccionar_color(color, index)
                ) for color in colores_disponibles
            ]
            color_menus[i].update()

    def cambiar_intentos(e):
        nonlocal intentos_maximos, intentos, info_lista
        intentos_maximos = int(intentos_dropdown.value)
        intentos = 0
        info_lista = []
        mostrar_snackbar(page, f"Número de intentos cambiado a {intentos_maximos}.", ft.colors.BLUE)
        adivinar_button.disabled = False
        for i in range(num_fichas):
            input_circles[i].content = ft.Container(
                bgcolor=ft.colors.BLACK,
                width=50,
                height=50,
                border_radius=25,
                border=ft.border.all(2, ft.colors.CYAN),
                data=None
            )
            input_circles[i].update()
        info_container.content = ft.Column(info_lista, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        info_container.update()

    output_field1 = mostrar_titulo_colorido("¡Bienvenido a")
    output_field2 = mostrar_titulo_colorido("Mastermind!")
    adivinar_button = ft.ElevatedButton(text="Adivinar", on_click=adivinar)
    pistas_field = ft.Text(value="", size=20)

    clave_label = ft.Text("Clave:", size=20, weight=ft.FontWeight.BOLD)
    clave_circles = [
        ft.Container(
            content=ft.Container(
                bgcolor=ft.colors.BLACK,
                width=50,
                height=50,
                border_radius=25,
                border=ft.border.all(2, ft.colors.CYAN),
                data=None
            ),
            width=50,
            height=50,
            border_radius=25,
            border=ft.border.all(2, ft.colors.CYAN)
        ) for _ in range(num_fichas)
    ]

    input_circles = [
        ft.Container(
            content=ft.Container(
                bgcolor=ft.colors.BLACK,
                width=50,
                height=50,
                border_radius=25,
                border=ft.border.all(2, ft.colors.CYAN),
                data=None
            ),
            width=50,
            height=50,
            border_radius=25,
            border=ft.border.all(2, ft.colors.CYAN),
            on_click=lambda e, i=i: mostrar_menu_colores(e, i)
        ) for i in range(num_fichas)
    ]

    color_menus = [
        ft.PopupMenuButton(
            items=[],
            data=None
        ) for i in range(num_fichas)
    ]

    def mostrar_menu_colores(e, index):
        color_menus[index].open = True
        color_menus[index].update()

    output_container = ft.Container(
        content=ft.Column(
            [
                ft.Row([output_field1], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([output_field2], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([clave_label] + clave_circles, alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border=ft.border.all(2, ft.colors.CYAN),
        border_radius=10,
        padding=10,
        margin=10,
        width=420,
    )

    input_container = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [ft.Row([input_circles[i], color_menus[i]], alignment=ft.MainAxisAlignment.CENTER) for i in range(num_fichas)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                adivinar_button,
                pistas_field,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border=ft.border.all(2, ft.colors.CYAN),
        border_radius=10,
        padding=10,
        margin=10,
        width=700,
    )

    info_container = ft.Container(
        content=ft.Column(info_lista, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        border=ft.border.all(2, ft.colors.CYAN),
        border_radius=10,
        padding=10,
        margin=10,
        width=430,
        height=530,
    )

    nivel_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Fácil"),
            ft.dropdown.Option("Medio"),
            ft.dropdown.Option("Difícil"),
        ],
        value="Fácil",
        on_change=cambiar_nivel,
        width=100,
    )

    intentos_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("6"),
            ft.dropdown.Option("9"),
            ft.dropdown.Option("12"),
        ],
        value="6",
        on_change=cambiar_intentos,
        width=70,
    )

    page.add(
        ft.Column(
            [
                ft.Row([
                    ft.Row([ft.Text("Nivel de Dificultad:", size=20), nivel_dropdown], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Text("Número de Intentos:", size=20), intentos_dropdown], alignment=ft.MainAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER),
                output_container,
                info_container,
                ft.Container(height=20),
                input_container,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    actualizar_menus_colores()

ft.app(target=main)
