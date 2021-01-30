'''
* Grupo 1363
* Pareja 8
* File: test_query.py
'''

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato.settings')

django.setup()
from datamodel.models import Game, Move, GameStatus
from django.contrib.auth.models import User


def main():
    print("\nEjecutando pruebas...\n")

    # Comprobamos si existe el user con id=10. Si no, se crea.
    try:
        user = User.objects.get(id=10)
    except User.DoesNotExist:
        user = User.objects.create_user(id=10, username="Miguel",
                                        password="miguel")

    # Comprobamos si existe el user con id=11. Si no, se crea.
    try:
        user2 = User.objects.get(id=11)
    except User.DoesNotExist:
        user2 = User.objects.create_user(id=11, username="Aitor",
                                         password="aitor")

    # El usuario con id=10 crea el juego
    try:
        game = Game.objects.get(id=1)
    except Game.DoesNotExist:
        game = Game(cat_user=user)
        game.save()

    # Busqueda de juegos con un solo usuario
    i = 1
    flag = False
    game_id_menor = None
    print("There are " + str(len(Game.objects.all())) + " games.")
    print("With one player:")
    while i <= len(Game.objects.all()):
        try:
            game_b = Game.objects.get(id=i)
            if flag is False:
                game_id_menor = game_b
            if game_b.cat_user is not None:
                if game_b.status == GameStatus.CREATED:
                    print("\tGame " + str(game_b.id) + " " + str(game.cat_user))
            i += 1
        except Game.DoesNotExist:
            i += 1

    if game_id_menor is not None:
        game_id_menor.mouse_user = user2
        game_id_menor.save()
        print("\nGame " + str(game_b.id) + " " + str(game_b.status) + " Usuarios: Gato -> " + str(game_b.cat_user) + \
              ", Raton -> " + str(game.mouse_user))
    else:
        print("\nThere are no games...\n")

    # Mover el gato 2 de la casilla 2 a la 11
    try:
        move = Move.objects.get(id=1)
    except Move.DoesNotExist:
        move = Move(origin=2, target=11, game=game_id_menor, player=user)
        move.save()
    print("Move: Origin -> " + str(move.origin) + ", Target -> " + str(move.target) + ", Player -> " + str(move.player) \
          + ", Date -> " + str(move.date))

    # Mover el raton de la casilla 59 a la 52
    try:
        move = Move.objects.get(id=2)
    except Move.DoesNotExist:
        move = Move(origin=59, target=52, game=game_id_menor, player=user2)
        move.save()
    print("Move: Origin -> " + str(move.origin) + ", Target -> " + str(move.target) + ", Player -> " + str(move.player) \
          + ", Date -> " + str(move.date))


if __name__ == "__main__":
    main()
