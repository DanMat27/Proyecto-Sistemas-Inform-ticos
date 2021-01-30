'''
* Grupo 1363
* Pareja 8
* File: tests_additional_P4.py
'''

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato.settings')

django.setup()
from datamodel.models import Game, Move, GameStatus
from django.contrib.auth.models import User

# Tests para comprobar finalizacion correcta de partidas
def GameEndTests():
    print("\nEjecutando GameEndTests...\n")

    # Creamos dos usuarios 
    user1 = User.objects.create_user(id=len(User.objects.all())+1, username="Alberto", password="alberto")
    user2 = User.objects.create_user(id=len(User.objects.all())+1, username="Mario", password="mario")
    user1_id = user1.id
    user2_id = user2.id

    # Creamos un juego con ambos usuarios
    game = Game(id=len(Game.objects.all())+1, cat_user=user1, mouse_user=user2)
    game.save()
    game_id = game.id
    print("Juego creado: " + str(game))
    print("Gato: " + str(game.cat_user) + ". Raton: " + str(game.mouse_user) + ".\n")

    # Realizamos movimientos hasta que el gato gana al raton
    # El gato gana si el raton no tiene casillas blancas para moverse
    print("Ejemplo de partida en la que gana el gato:")

    move1_cat = Move(origin=0, target=9, game=game, player=user1)
    move1_cat.save()
    print("Gato: 0 => 9")

    move1_mouse = Move(origin=59, target=50, game=game, player=user2)
    move1_mouse.save()
    print("Raton: 59 => 50")

    move2_cat = Move(origin=2, target=11, game=game, player=user1)
    move2_cat.save()
    print("Gato: 2 => 11")

    move2_mouse = Move(origin=50, target=41, game=game, player=user2)
    move2_mouse.save()
    print("Raton: 50 => 41")

    move3_cat = Move(origin=9, target=16, game=game, player=user1)
    move3_cat.save()
    print("Gato: 9 => 16")

    move3_mouse = Move(origin=41, target=32, game=game, player=user2)
    move3_mouse.save()
    print("Raton: 41 => 32")

    move4_cat = Move(origin=16, target=25, game=game, player=user1)
    move4_cat.save()
    print("Gato: 16 => 25")

    move4_mouse = Move(origin=32, target=41, game=game, player=user2)
    move4_mouse.save()
    print("Raton: 32 => 41")

    move5_cat = Move(origin=11, target=18, game=game, player=user1)
    move5_cat.save()
    print("Gato: 11 => 18")

    move5_mouse = Move(origin=41, target=32, game=game, player=user2)
    move5_mouse.save()
    print("Raton: 41 => 32")

    move6_cat = Move(origin=18, target=27, game=game, player=user1)
    move6_cat.save()
    print("Gato: 18 => 27")

    move6_mouse = Move(origin=32, target=41, game=game, player=user2)
    move6_mouse.save()
    print("Raton: 32 => 41")

    move7_cat = Move(origin=27, target=34, game=game, player=user1)
    move7_cat.save()
    print("Gato: 27 => 34")

    move7_mouse = Move(origin=41, target=32, game=game, player=user2)
    move7_mouse.save()
    print("Raton: 41 => 32")

    move8_cat = Move(origin=34, target=41, game=game, player=user1)
    move8_cat.save()
    print("Gato: 34 => 41")

    if game.status == GameStatus.FINISHED:
        if game.winner == 1:
            print("Ha ganado el gato!\n")
        else:
            print("Ha ganado el raton!\n")


    # Realizamos movimientos hasta que el raton gana al gato
    # El raton gana si se posiciona por encima de todos los gatos
    # Creamos un juego con ambos usuarios
    game2 = Game(id=len(Game.objects.all())+1, cat_user=user2, mouse_user=user1)
    game2.save()
    game2_id = game2.id
    print("Juego creado: " + str(game2))
    print("Gato: " + str(game2.cat_user) + ". Raton: " + str(game2.mouse_user) + ".\n")

    print("Ejemplo de partida en la que gana el raton:")

    move9_cat = Move(origin=0, target=9, game=game2, player=user2)
    move9_cat.save()
    print("Gato: 0 => 9")

    move9_mouse = Move(origin=59, target=50, game=game2, player=user1)
    move9_mouse.save()
    print("Raton: 59 => 50")

    move10_cat = Move(origin=2, target=11, game=game2, player=user2)
    move10_cat.save()
    print("Gato: 2 => 11")

    move10_mouse = Move(origin=50, target=41, game=game2, player=user1)
    move10_mouse.save()
    print("Raton: 50 => 41")

    move11_cat = Move(origin=4, target=13, game=game2, player=user2)
    move11_cat.save()
    print("Gato: 4 => 13")

    move11_mouse = Move(origin=41, target=32, game=game2, player=user1)
    move11_mouse.save()
    print("Raton: 41 => 32")

    move12_cat = Move(origin=6, target=15, game=game2, player=user2)
    move12_cat.save()
    print("Gato: 6 => 15")

    move12_mouse = Move(origin=32, target=25, game=game2, player=user1)
    move12_mouse.save()
    print("Raton: 32 => 25")

    move13_cat = Move(origin=9, target=18, game=game2, player=user2)
    move13_cat.save()
    print("Gato: 9 => 18")

    move13_mouse = Move(origin=25, target=16, game=game2, player=user1)
    move13_mouse.save()
    print("Raton: 41 => 32")

    move14_cat = Move(origin=11, target=20, game=game2, player=user2)
    move14_cat.save()
    print("Gato: 11 => 20")

    move14_mouse = Move(origin=16, target=9, game=game2, player=user1)
    move14_mouse.save()
    print("Raton: 16 => 9")

    if game2.status == GameStatus.FINISHED:
        if game2.winner == 1:
            print("Ha ganado el gato!\n")
        else:
            print("Ha ganado el raton!\n")


    # Eliminamos de la BD todo lo creado antes
    print("\nEliminando pruebas...\n")
    Move.objects.all().filter(game=game).delete()
    Move.objects.all().filter(game=game2).delete()
    Game.objects.all().filter(id=game_id).delete()
    Game.objects.all().filter(id=game2_id).delete()
    User.objects.all().filter(id=user1_id).delete()
    User.objects.all().filter(id=user2_id).delete()

    return


if __name__ == "__main__":
    GameEndTests()
