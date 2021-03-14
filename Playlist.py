from clint.textui import colored, puts
from PyInquirer import prompt, print_json, style_from_dict, Token, Separator

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

confirmacion = [
    {
        "type": "confirm",
        "message": "¿Está seguro que desea vaciar la lista?",
        "name": "confirmacion",
    }
]

class Cancion:
    def __init__(self, titulo, posicion):
        self.titulo = titulo
        self.posicion = posicion

    def cambiar_posicion(self, posicion):
        self.posicion = posicion
    def cambiar_titulo(self, titulo):
        self.titulo = titulo

class Playlist:
    def __init__(self, playlist: list):
        self.playlist = playlist
        self.playlist_canciones = []
        self.playlist_dict = {}

        for i, cancion in enumerate(self.playlist):
            cancion_obj = Cancion(titulo=cancion, posicion=i + 1)
            self.playlist_canciones.append(cancion_obj)
            self.playlist_dict[cancion] = cancion_obj

    def agregar_cancion(self, titulo):

        if len(self.playlist) >= 35:
            return colored.red(f"El playlist ya posee 35 canciones.")

        if titulo in self.playlist:
            return colored.red(f"La canción '{titulo}' ya estaba agregada al playlist.")

        if not titulo in self.playlist:
            self.playlist.append(titulo)
            self.playlist_canciones.append(Cancion(titulo, len(self.playlist) + 1))
            self.playlist_dict[titulo] = Cancion(titulo, len(self.playlist) + 1)
            return colored.green(f"{titulo} ha sido agregada a la playlist exitosamente")

    def agregar_cancion_posicion(self, titulo, posicion):
        if posicion <= 0:
            return colored.red("La posicion que ingreso no es valida.")

        if len(self.playlist) >= 35:
            return colored.red(f"El playlist ya posee 35 canciones.")

        if titulo in self.playlist:
            return colored.red(f"La canción '{titulo}' ya estaba agregada al playlist.")

        if not titulo in self.playlist:

            for i, cancion in enumerate(self.playlist_canciones):
                if cancion.posicion >= posicion:
                    cancion.cambiar_posicion(cancion.posicion + 1)
                    self.playlist[i] = cancion.titulo
                    self.playlist_canciones[i] = cancion
                    self.playlist_dict[cancion.titulo] = cancion

            self.playlist.insert(posicion - 1, titulo)
            self.playlist_canciones.insert(posicion - 1, Cancion(titulo, posicion=posicion))
            self.playlist_dict[titulo] = Cancion(titulo, posicion=posicion)

            return colored.green(f"{titulo} ha sido agregada a la playlist exitosamente")

    def editar_cancion(self, titulo, nuevo_titulo):
        cancion = self.playlist_dict[titulo]
        cancion.cambiar_titulo(nuevo_titulo)

        index = self.playlist.index(titulo)
        self.playlist[index] = cancion.titulo
        self.playlist_canciones[index] = cancion
        del self.playlist_dict[titulo]
        self.playlist_dict[nuevo_titulo] = cancion

        return colored.green(f"Se ha cambiado el nombre de '{titulo}' a '{nuevo_titulo}' con exito.")

    def eliminar_cancion(self, titulo):
        if len(self.playlist) == 1:

            self.vaciar_playlist()
        else:
            index = self.playlist.index(titulo)
            self.playlist.pop(index)
            self.playlist_canciones.pop(index)
            posicion_eliminada = self.playlist_dict[titulo].posicion
            del self.playlist_dict[titulo]

            for i, cancion in enumerate(self.playlist_canciones):
                if cancion.posicion > posicion_eliminada:
                    cancion.cambiar_posicion(cancion.posicion - 1)
                    self.playlist[i] = cancion.titulo
                    self.playlist_canciones[i] = cancion
                    self.playlist_dict[cancion.titulo] = cancion

            return colored.green(f"La cancion '{titulo}' ha sido eliminada del playlist con exito.")

    def vaciar_playlist(self):
        confirmacion_vaciar = prompt(confirmacion, style=style)["confirmacion"]
        if confirmacion_vaciar:
            self.playlist = []
            self.playlist_canciones = []
            self.playlist_dict = {}
            return colored.green(f"El playlist ha sido vaciado con exito.")
        else:
            return colored.green(f"")

    def mover_cancion(self, titulo, posicion):

        if posicion <= 0 or posicion > len(self.playlist):
            return colored.red("La posicion indicada no es valida.")

        cancion = self.playlist_dict[titulo]
        posicion_vieja = cancion.posicion
        otra_cancion = self.playlist_canciones[posicion - 1]

        otra_cancion.cambiar_posicion(posicion_vieja)
        cancion.cambiar_posicion(posicion)

        self.playlist[posicion - 1], self.playlist[posicion_vieja - 1] = cancion.titulo, otra_cancion.titulo
        self.playlist_canciones[posicion - 1], self.playlist_canciones[posicion_vieja - 1] = cancion, otra_cancion

        del self.playlist_dict[titulo]
        self.playlist_dict[titulo] = cancion
        del self.playlist_dict[otra_cancion.titulo]
        self.playlist_dict[otra_cancion.titulo] = otra_cancion

        return colored.green(f"Se ha movido '{titulo}' a la posicion {posicion} con exito.")

    def __len__(self):
        return len(self.playlist)

