import flet as ft


def main(page: ft.Page):
    page.title = "unidades de medida en Flet "

    # Contenedor con dimensiones en píxeles
    container_pixels = ft.Container(
        width=200,
        height=100,
        bgcolor=ft.colors.BLUE,
        content=ft.Text("200px x 100px"),
        alignment=ft.alignment.center,
        margin=10
    )

    # Contenedor con ancho en porcentaje
    container_percentage = ft.Container(
        width="80%",
        height=100,
        bgcolor=ft.colors.GREEN,
        content=ft.Text("80% x 100px"),
        alignment=ft.alignment.center,
        margin=10
    )

    # Contenedor con expansión
    container_expand = ft.Container(
        expand=True,
        height=100,
        bgcolor=ft.colors.RED,
        content=ft.Text("Expand x 100px"),
        alignment=ft.alignment.center,
        margin=10
    )

    # Contenedor con diferentes tipos de padding
    container_padding = ft.Container(
        width=300,
        bgcolor=ft.colors.AMBER,
        padding=ft.padding.only(left=20, top=10, right=20, bottom=30),
        content=ft.Text("Padding: L20, T10, R20, B30"),
        margin=10
    )

    # Añadir todos los contenedores a la página
    page.add(
        ft.Text("unidades de medida", size=20),
        container_pixels,
        container_percentage,
        container_expand,
        container_padding
    )

    page.update()


ft.app(target=main)
