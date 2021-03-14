from __future__ import print_function, unicode_literals
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("clint")
install("PyInquirer")
install("pyfiglet==0.7")

from pyfiglet import Figlet
from PyInquirer import prompt, print_json, style_from_dict, Token, Separator
from clint.textui import colored, puts
from os import system, name
import Playlist

# Data
playlist = [
    "Si veo a tu mamá»",
    "La difícil",
    "Pero ya no",
    "La santa",
    "Yo perreo sola",
    "Bichiyal",
    "Soliá",
    "La zona",
    "Que malo",
    "Vete",
    "Ignorantes",
    "A tu merced",
    "Una vez",
    "Safaera",
    "25/8",
    "Está cabrón ser yo",
    "Puesto pa' guerrial",
    "P FKN R",
    "Hablamos mañana",
    "<3",
]
the_playlist = Playlist.Playlist(playlist=playlist)

# Styles
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: 'bold #673ab7',
})

title = Figlet(font='slant')
subtitle = Figlet(font='small')

# Acciones
main_menu_actions = ["Mostrar todas las canciones", "Editar Playlist","Mostrar el tamaño del playlist", "Vaciar Playlist"]
edit_menu_actions = ["Agregar canción al final de la lista",
                     "Agregar canción a una posición especifica",
                     "Editar canción",
                     "Eliminar canción",
                     "Mover canción dentro de la lista"
                    ]
# Menus
main_menu = [
    {
        "type": "list",
        "message": "YHLQMDLG Playlist",
        "name": "action",
        "choices": main_menu_actions + [Separator(), "Cerrar"]
    }
]

edit_menu = [
    {
        "type": "list",
        "message": "Editar Playlist",
        "name": "action",
        "choices": edit_menu_actions + [Separator(), "Volver"]
    }
]

# Preguntas
agregar_cancion = [
    {
        "type": "input",
        "message": "Nombre de la canción",
        "name": "titulo"
    }
]
agregar_cancion_posicion = [
    {
        "type": "input",
        "message": "Nombre de la canción",
        "name": "titulo"
    },
    {
        "type": "input",
        "message": "Que posición en el playlist",
        "name": "posicion"
    }
]

cambiar_titulo = [
    {
        "type": "input",
        "message": "Nuevo nombre de la cancion",
        "name": "nuevo_titulo"
    }
]

cambiar_posicion = [
    {
        "type": "input",
        "message": "Nueva posicion para la cancion",
        "name": "nueva_posicion"
    }
]

nueva_accion = [
    {
        "type": "confirm",
        "message": "¿Nueva accion?",
        "name": "nueva_accion",
    }
]

expectativa_cancion = [
    {
        "type": "input",
        "message": "Reproducciones esperadas",
        "name": "reproducciones"
    },
    {
        "type": "input",
        "message": "Skips esperados",
        "name": "skips"
    },
    {
        "type": "input",
        "message": "Repeticiones esperadas",
        "name": "repeticiones"
    },
]

def clear():
    # Windows
    if name == 'nt':
        _ = system('cls')
    # Mac and Linux
    else:
        _ = system('clear')

def mostrar_playlist():
    print()
    playlist_sorted = sorted(the_playlist.playlist)
    puts(colored.blue("Ordenado alfabeticamente."))
    for cancion in playlist_sorted:
        cancion_obj = the_playlist.playlist_dict[cancion]
        puts(colored.yellow(f"{cancion_obj.posicion}. {cancion_obj.titulo}"))
    print()

def mostrar_tamano_playlist():
    print()
    puts(colored.yellow(f"El playlist actualmente posee {len(the_playlist)} canciones."))
    print()

def edit_playlist(action):

    # Volver
    if action == "Volver":
        return

    # Agregar
    if action == edit_menu_actions[0]:
        agregar_cancion_res = prompt(agregar_cancion, style = style)
        mensaje = the_playlist.agregar_cancion(agregar_cancion_res['titulo'])

    # Agregar especificando posicion
    elif action == edit_menu_actions[1]:
        agregar_cancion_res = prompt(agregar_cancion_posicion, style=style)
        titulo = agregar_cancion_res['titulo']
        posicion = agregar_cancion_res['posicion']

        try:
            posicion = int(posicion)
        except:
            print()
            puts(colored.red("La posición no es un valor entero"))
            print()
            return

        mensaje = the_playlist.agregar_cancion_posicion(titulo=titulo, posicion=posicion)

    # Eliminar, editar o mover cancion
    else:
        # Seleccion la cancion
        seleccionar_cancion = [
            {
                "type": "list",
                "choices": the_playlist.playlist,
                "name": "cancion",
                "message": "Selecciona la canción"
            }
        ]
        cancion_seleccionada = prompt(seleccionar_cancion, style=style)

        # Editar
        if action == edit_menu_actions[2]:
            input_nuevo_titulo = prompt(cambiar_titulo, style=style)
            mensaje = the_playlist.editar_cancion(cancion_seleccionada['cancion'], input_nuevo_titulo['nuevo_titulo'])

        # Eliminar
        elif action == edit_menu_actions[3]:
            mensaje = the_playlist.eliminar_cancion(cancion_seleccionada['cancion'])

        # Mover
        elif action == edit_menu_actions[4]:
            input_nueva_posicion = prompt(cambiar_posicion, style=style)
            posicion = input_nueva_posicion['nueva_posicion']
            try:
                posicion = int(posicion)
            except:
                print()
                puts(colored.red("La posición no es un valor entero"))
                print()
                return

            mensaje = the_playlist.mover_cancion(cancion_seleccionada['cancion'], posicion)

    print()
    puts(mensaje)
    print()

def expectativas_por_cancion():
    print()
    puts(colored.red("Ingresa las expectativas por cancion..."))
    print()

    reproducciones_por_cancion = []
    skips_por_cancion = []
    repeticiones_por_cancion = []

    mas_reproducida = ""
    menos_reproducida = ""
    mas_skip = ""
    menos_skip = ""
    mas_repetida = ""
    menos_repetida = ""
    primera_cancion = ""
    ultima_cancion = ""

    for cancion in the_playlist.playlist:
        puts(colored.blue(cancion))
        expectativa = prompt(expectativa_cancion, style=style)

        if the_playlist.playlist_dict[cancion].posicion == 1:
            primera_cancion = the_playlist.playlist_dict[cancion].posicion

        if the_playlist.playlist_dict[cancion].posicion == len(the_playlist):
            ultima_cancion = the_playlist.playlist_dict[cancion].posicion

        repr = expectativa['reproducciones']
        skip = expectativa['skips']
        rep = expectativa['repeticiones']

        try:
            repr = int(repr)
        except:
            return colored.red("Las reproducciones deben un numero entero...")

        try:
            rep = int(rep)
        except:
            return colored.red("Las repeticiones deben ser un numero entero...")

        try:
            skip = int(skip)
        except:
            return colored.red("Los skips deben ser un numero entero...")

        reproducciones_por_cancion.append(int(expectativa['reproducciones']))
        if repr <= min(reproducciones_por_cancion):
            menos_reproducida = cancion
        if repr >= max(reproducciones_por_cancion):
            mas_reproducida = cancion

        skips_por_cancion.append(int(expectativa['skips']))
        if skip <= min(skips_por_cancion):
            menos_skip = cancion
        if skip >= max(skips_por_cancion):
            mas_skip = cancion

        repeticiones_por_cancion.append(int(expectativa['repeticiones']))
        if rep <= min(repeticiones_por_cancion):
            menos_repetida = cancion
        if rep >= max(repeticiones_por_cancion):
            mas_repetida = cancion

    mostrar_tamano_playlist()
    puts(colored.yellow(f"La primera cancion es: {primera_cancion}"))
    puts(colored.yellow(f"La ultima cancion es: {ultima_cancion}"))
    puts(colored.yellow(f"Promedio de reproducciones esperadas por cancion {sum(reproducciones_por_cancion) / len(reproducciones_por_cancion)}"))
    puts(colored.yellow(f"Promedio de reproducciones esperadas por cancion {sum(reproducciones_por_cancion) / len(reproducciones_por_cancion)}"))
    puts(colored.yellow(f"La cancion mas reproducida es: {mas_reproducida}"))
    puts(colored.yellow(f"La cancion menos reproducida es: {menos_reproducida}"))

    puts(colored.yellow(f"Promedio de skips esperados por cancion {sum(skips_por_cancion) / len(skips_por_cancion)}"))
    puts(colored.yellow(f"La cancion mas saltada es: {mas_skip}"))
    puts(colored.yellow(f"La cancion menos saltada es: {menos_skip}"))

    puts(colored.yellow(f"Promedio de repeticiones esperadas por cancion {sum(repeticiones_por_cancion) / len(repeticiones_por_cancion)}"))
    puts(colored.yellow(f"La cancion mas repetida es: {mas_repetida}"))
    puts(colored.yellow(f"La cancion menos repetida es: {menos_repetida}"))

    return colored.green("Las expectativas han sido ingresadas correctamente")


if __name__ == '__main__':

    # Intalar librerias
    clear()

    while True:
        print(title.renderText("YHLQMDLG"))
        main_menu_action = prompt(main_menu, style=style)

        # Cerrar programa
        if main_menu_action['action'] == 'Cerrar':
            break
        # Mostrar Playlist
        elif main_menu_action['action'] == main_menu_actions[0]:
            mostrar_playlist()

        # Editar playlist
        elif main_menu_action['action'] == main_menu_actions[1]:
            edit_playlist_action = prompt(edit_menu, style=style)
            edit_playlist(edit_playlist_action['action'])

        # Mostrar tamano del playlist
        elif main_menu_action['action'] == main_menu_actions[2]:
            mostrar_tamano_playlist()

        # Vaciar playlist
        elif main_menu_action['action'] == main_menu_actions[3]:
            mensaje = the_playlist.vaciar_playlist()
            print()
            puts(mensaje)
            print()

        # Pregunta por nueva accion
        respuesta_nueva_accion = prompt(nueva_accion, style=style)
        if not respuesta_nueva_accion['nueva_accion']:
            mensaje = expectativas_por_cancion()

            print()
            puts(mensaje)
            print()