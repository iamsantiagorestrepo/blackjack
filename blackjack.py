import flet as ft
import random

def main(page: ft.Page):
    # Configuración inicial de la página con un tema visual
    page.title = "Blackjack Básico"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#205210"  # Metallic blue for modern gym vibe
    page.scroll = "auto"
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#1E88E5",  # Azul metálico
            secondary="#FFCA28",  # Ámbar
            surface="#2A2A2A",  # Fondo de contenedores
            on_primary="#FFFFFF",
            on_secondary="#1A1A1A",
            on_background="#FFFFFF",
            on_surface="#FFFFFF"
        )
    )
    # Eliminamos page.bgimage ya que la URL no funciona consistentemente; usamos el color del tema
    # Si quieres usar una imagen local, descomenta y ajusta la ruta:
    # page.bgimage = ft.Image(src="D:/programming/flet/flet/backgrounds/casino_table.jpg", fit="cover", opacity=0.8)

    # Inicializar variables globales
    global player_hand, dealer_hand, deck
    suits = ['♠', '♥', '♦', '♣']  # Símbolos de palos
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [rank + suit for suit in suits for rank in ranks]
    player_hand = []
    dealer_hand = []

    # Componentes de la interfaz
    player_cards_container = ft.Row(controls=[], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
    player_value = ft.Text(value="Tu total: 0", size=16, color="#FFFFFF")
    dealer_cards_container = ft.Row(controls=[], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
    dealer_value = ft.Text(value="Total del dealer: ?", size=16, color="#FFFFFF")
    mensaje = ft.Text(value="", size=16, color="#FFFFFF")
    hit_button = ft.ElevatedButton(
        text="Hit",
        icon="add_circle",
        on_click=lambda e: hit(),
        style=ft.ButtonStyle(
            bgcolor="#FFCA28",
            color="#1A1A1A",
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=5
        )
    )
    stand_button = ft.ElevatedButton(
        text="Stand",
        icon="check_circle",
        on_click=lambda e: stand(),
        style=ft.ButtonStyle(
            bgcolor="#FFCA28",
            color="#1A1A1A",
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=5
        )
    )
    restart_button = ft.ElevatedButton(
        text="Reiniciar",
        icon="refresh",
        on_click=lambda e: restart_game(),
        style=ft.ButtonStyle(
            bgcolor="#FF5252",
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=5
        )
    )

    # Función para calcular valor de la mano
    def calculate_hand(hand):
        value = 0
        aces = 0
        for card in hand:
            if card.startswith('10'):
                rank = '10'
            else:
                rank = card[:-1]
            if rank in ['J', 'Q', 'K']:
                value += 10
            elif rank == 'A':
                aces += 1
            else:
                value += int(rank)
        value_with_aces = value
        for _ in range(aces):
            if value_with_aces + 11 <= 21:
                value_with_aces += 11
            else:
                value_with_aces += 1
        return value_with_aces

    # Función para repartir carta
    def deal_card(hand):
        global deck
        if deck:
            card = random.choice(deck)
            deck.remove(card)
            hand.append(card)
            return card
        return None

    # Función para mostrar cartas en la interfaz
    def display_cards(hand, container, hide_second=False):
        container.controls.clear()
        for i, card in enumerate(hand):
            card_text = card
            card_color = "#000000" if card[-1] in ['♠', '♣'] else "#FF0000"  # Negro para espadas/tréboles, rojo para corazones/diamantes
            if hide_second and i == 1:
                # Mostrar carta oculta para el dealer
                container.controls.append(
                    ft.Container(
                        content=ft.Text("🂠", size=40, color="#FFFFFF"),
                        width=80,
                        height=120,
                        bgcolor="#4A4A4A",
                        border=ft.border.all(2, "#FFFFFF"),
                        border_radius=8,
                        alignment=ft.alignment.center
                    )
                )
            else:
                # Mostrar carta como un contenedor estilizado
                container.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(card_text, size=20, color=card_color),
                                ft.Text(card[-1], size=30, color=card_color)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=0
                        ),
                        width=80,
                        height=120,
                        bgcolor="#FFFFFF",
                        border=ft.border.all(2, "#000000"),
                        border_radius=8,
                        alignment=ft.alignment.center
                    )
                )
        page.update()

    # Función para inicializar el juego
    def start_game():
        global player_hand, dealer_hand
        player_hand.clear()
        dealer_hand.clear()
        for _ in range(2):
            deal_card(player_hand)
            deal_card(dealer_hand)
        display_cards(player_hand, player_cards_container)
        display_cards(dealer_hand, dealer_cards_container, hide_second=True)
        player_value.value = f"Tu total: {calculate_hand(player_hand)}"
        dealer_value.value = f"Total del dealer: {calculate_hand(dealer_hand) if not dealer_hand else '?'}"
        mensaje.value = ""
        hit_button.disabled = False
        stand_button.disabled = False
        page.update()

    # Función para verificar el estado del juego
    def check_game_status():
        player_total = calculate_hand(player_hand)
        if player_total > 21:
            mensaje.value = "¡Te pasaste! Pierdes."
            mensaje.color = "red"
            dealer_play()
            disable_buttons()
        page.update()

    # Función para deshabilitar botones al finalizar
    def disable_buttons():
        hit_button.disabled = True
        stand_button.disabled = True
        page.update()

    # Función al hacer "Hit"
    def hit():
        deal_card(player_hand)
        display_cards(player_hand, player_cards_container)
        player_value.value = f"Tu total: {calculate_hand(player_hand)}"
        check_game_status()

    # Función al hacer "Stand"
    def stand():
        dealer_play()

    # Función para el turno del dealer
    def dealer_play():
        display_cards(dealer_hand, dealer_cards_container, hide_second=False)
        dealer_total = calculate_hand(dealer_hand)
        while dealer_total < 17:
            deal_card(dealer_hand)
            display_cards(dealer_hand, dealer_cards_container)
            dealer_total = calculate_hand(dealer_hand)
        player_total = calculate_hand(player_hand)
        dealer_value.value = f"Total del dealer: {dealer_total}"
        if dealer_total > 21:
            mensaje.value = "¡El dealer se pasó! Ganaste."
            mensaje.color = "green"
        elif player_total > dealer_total:
            mensaje.value = "¡Ganaste!"
            mensaje.color = "green"
        elif player_total < dealer_total:
            mensaje.value = "¡Perdiste!"
            mensaje.color = "red"
        else:
            mensaje.value = "¡Empate!"
            mensaje.color = "yellow"
        disable_buttons()
        page.update()

    # Función para reiniciar el juego
    def restart_game():
        global deck
        deck = [rank + suit for suit in suits for rank in ranks]
        start_game()

    # Iniciar el juego al cargar la página
    start_game()

    # Agregar elementos a la página
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Blackjack Básico", size=24, weight="bold", color="#FFFFFF"),
                    ft.Text("Mano del Dealer", size=18, color="#FFFFFF"),
                    dealer_cards_container,
                    dealer_value,
                    ft.Divider(height=20, color="#FFFFFF"),
                    ft.Text("Tu Mano", size=18, color="#FFFFFF"),
                    player_cards_container,
                    player_value,
                    ft.Row(
                        [hit_button, stand_button, restart_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    mensaje
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            padding=20,
            bgcolor="#00000080",  # Fondo semitransparente para el contenedor
        )
    )

ft.app(target=main)