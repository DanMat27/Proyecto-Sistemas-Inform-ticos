'''
* Grupo 1363
* Pareja 8
* File: views.py
'''

from django.http import HttpResponseForbidden, HttpResponse
import json
from django.shortcuts import render
from datamodel.models import Game, Move, Counter, GameStatus
from django.shortcuts import redirect
from django.urls import reverse
from logic.forms import UserForm, MoveForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from datamodel import constants
from django.core.exceptions import ValidationError
from django.http import Http404
from urllib.parse import urlencode

# Funcion anonymous_required
# Desc: Comprueba si no hay un usuario autenticado en la sesion
# Si lo hay, devuelve error (solo se aceptan anonimos)
def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            Counter.objects.inc()
            return HttpResponseForbidden(
                errorHTTP(request, exception="Action restricted to anonymous users"))
        else:
            return f(request)
    return wrapped


# Funcion errorHTTP
# Desc: Renderiza el template de error en la aplicacion
def errorHTTP(request, exception=None):
    context_dict = {}
    context_dict[constants.ERROR_MESSAGE_ID] = exception
    return render(request, "mouse_cat/error.html", context_dict).content


# Funcion index_service
# Desc: Renderiza el template del index y borra la informacion guardada en
# la sesion (referente a las repeticiones y ultimos movimientos)
def index_service(request):
    if 'simulation' in request.session:
        if request.session['simulation'] is not None:
            try:
                game = Game.objects.get(id=request.session['simulation'])
            except:
                return render(request, "mouse_cat/index.html")
            Game.objects.all().filter(id=request.session['simulation']).delete()
            request.session['simulation'] = None
        if 'last_move' in request.session:
            if 'last_move' is not None:
                request.session['last_move'] = None

    return render(request, "mouse_cat/index.html")


# Funcion login_service
# Desc: Realiza el login de un usuario anonimo, mediante un formulario, y guarda 
# su informacion en la sesion
@anonymous_required
def login_service(request):

    user_form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                request.session['counter'] = 0
                return redirect(reverse('landing'))
            else:
                form.add_error(None, 'Usuario/clave no válidos')
                return render(request, 'mouse_cat/login.html', {'user_form': form})
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            form.add_error(None, 'Usuario/clave no válidos')
            return render(request, 'mouse_cat/login.html', {'user_form': form})

    else:
        return render(request, 'mouse_cat/login.html', {'user_form': user_form})


# Funcion logout_service
# Desc: Realiza el log out de un usuario guardado en la sesion
def logout_service(request):
    if not request.user.is_authenticated:
        Counter.objects.inc()
        return redirect(reverse('login'))

    user = request.user
    logout(request)
    return render(request, 'mouse_cat/logout.html', {'user': user})


# Funcion de signup_service
# Desc: Crea un nuevo usuario en la BD, mediante un formulario, y guarda su informacion 
# en la sesion para que empiece logueado
@anonymous_required
def signup_service(request):

    user_form = SignupForm()

    if request.method == 'POST':
        user_form = SignupForm(data=request.POST)

        if user_form.is_valid():

            try:
                validate_password(request.POST.get('password'), user=None, password_validators=None)
            except ValidationError as e:
                for error in e.error_list:
                    user_form.add_error(None, error)
                return render(request, 'mouse_cat/signup.html', {'user_form': user_form})

            if request.POST.get('password') != request.POST.get('password2'):
                user_form.add_error(None, 'La clave y su repetición no coinciden.')
                return render(request, 'mouse_cat/signup.html', {'user_form': user_form})

            user = user_form.save()

            if user is not None:

                user.set_password(user.password)
                user.save()

                login(request, user)

                request.session['counter'] = 0

                return redirect(reverse('landing'))

            else:
                user_form.add_error(None, 'Error de registro.')
                return render(request, 'mouse_cat/signup.html', {'user_form': user_form})

        else:
            user_form.add_error(None, 'Usuario duplicado.')
            return render(request, 'mouse_cat/signup.html', {'user_form': user_form})

    else:

        return render(request, 'mouse_cat/signup.html', {'user_form': user_form})


# Funcion counter_service
# Desc: Obtiene el singleton de counter_service y renderiza el html de counter 
# con sus valores (el global posee el numero de fallos del sistema)
def counter_service(request):

    # get session variable
    if "counter" in request.session:
        request.session["counter"] += 1
    else:
        request.session["counter"] = 1

    global_counter = Counter.objects.get_current_value()

    return render(request, "mouse_cat/counter.html", {'counter_session': request.session["counter"],
                                                      'counter_global': global_counter})


# Funcion create_game_service
# Desc: Crea un juego nuevo en la BD con el usuario conectado como el gato
def create_game_service(request):
    if not request.user.is_authenticated:
        Counter.objects.inc()
        return redirect(reverse('login'))

    user = request.user
    game = Game(cat_user=user)

    game.save()

    return render(request, "mouse_cat/new_game.html", {'game': game})


# Funcion join_game_service
# Desc: Se une el usuario conectado como el raton al juego creado no activo de mayor id
# Tambien puedes unirte a un juego creado no activo elegido en select game
def join_game_service(request, game_id=None):

    if not request.user.is_authenticated:
        Counter.objects.inc()
        return redirect(reverse('login'))

    if game_id is not None: # Unirse a un juego desde select game

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            Counter.objects.inc()
            raise Http404("ERROR 404")

        if game.status == GameStatus.ACTIVE or game.status == GameStatus.FINISHED:
            Counter.objects.inc()
            raise Http404("ERROR 404")

        if game.mouse_user != None or game.cat_user == request.user:
            Counter.objects.inc()
            return render(request, "mouse_cat/select_game.html", {'msg_error':"No puedes unirte a un juego \
                                                                  si ya eres el gato!"})

        game.mouse_user = request.user

        game.save()        
        return render(request, "mouse_cat/join_game.html", {'game': game})

    else: # Unirse a un juego desde join game
        num_Juegos = len(Game.objects.all())

        if num_Juegos == 0:
            return render(request, "mouse_cat/join_game.html", {'msg_error': constants.JOIN_GAME_ERROR_NOGAME})

        i = 1
        cont = 1

        while i <= num_Juegos:
            try:
                game = Game.objects.get(id=cont)
            except Game.DoesNotExist:
                if i <= num_Juegos:
                    cont += 1
                    continue
                Counter.objects.inc()
                return render(request, "mouse_cat/join_game.html", {'msg_error': constants.JOIN_GAME_ERROR_NOGAME})
            i += 1
            cont += 1

        i = 1
        cont = cont - 1
        while i <= num_Juegos:
            try:
                game = Game.objects.get(id=cont)
            except Game.DoesNotExist:
                if i <= num_juegos:
                    cont -= 1
                    continue
                Counter.objects.inc()
                return render(request, "mouse_cat/join_game.html", {'msg_error': constants.JOIN_GAME_ERROR_NOGAME})

            if game.status != GameStatus.CREATED:
                i += 1
                cont -= 1
            else:
                game.mouse_user = request.user
                if game.cat_user == game.mouse_user:
                    i += 1
                    continue

                game.save()
                return render(request, "mouse_cat/join_game.html", {'game': game})

        return render(request, "mouse_cat/join_game.html", {'msg_error': constants.JOIN_GAME_ERROR_NOGAME})


# Funcion select_game_service
# Desc: Renderiza la pagina de select_gamecon juegos para jugar, unirse y ver 
# repeticiones o selecciona un juego de la pagina select game. Tambien hay un
# filtro.
# Si es para jugar, te lleva a la funcion show_game
# Si es para unirse, te lleva a join_game
# Si es para ver repeticiones, te lleva a repeat_game
def select_game_service(request, game_id=None, option=None):

    if not request.user.is_authenticated:
        Counter.objects.inc()
        return redirect(reverse('login'))

    # JUEGO SELECCIONADO PARA JUGAR
    if game_id is not None:

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            Counter.objects.inc()
            raise Http404("ERROR 404")

        if game.status == GameStatus.CREATED:
            Counter.objects.inc()
            raise Http404("ERROR 404")

        if game.cat_user != request.user and game.mouse_user != request.user:
            Counter.objects.inc()
            return render(request, "mouse_cat/select_game.html", {'msg_error':"No puedes jugar en un juego \
                                                                   al que no perteneces!"})

        request.session[constants.GAME_SELECTED_SESSION_ID] = game_id
        return redirect(reverse('show_game'))

    else: # RENDERIZAR SELECT_GAME.HTML
        game_list_cat_play = []
        game_list_mouse_play = []
        game_list_join = []
        game_list_repeat = []
        game_list_filter = []
        game_list_filter_join = []
        game_list_filter_finished = []

        num_juegos = len(Game.objects.all())

        if num_juegos == 0:
            return render(request, "mouse_cat/select_game.html", {'as_cat_play': game_list_cat_play,
                                                                  'as_mouse_play': game_list_mouse_play,
                                                                  'list_join':game_list_join,
                                                                  'list_repeat':game_list_repeat})
        
        # FILTRO DE JUEGOS
        if request.method == 'POST': 
            i = 1
            cont = 1

            while i <= num_juegos:
                try:
                    game = Game.objects.get(id=cont)
                except Game.DoesNotExist:
                    if i <= num_juegos:
                        cont += 1
                        continue
                    Counter.objects.inc()
                    return render(request, "mouse_cat/select_game.html", {'list_filter':game_list_filter,
                                                                          'list_join':game_list_filter_join,
                                                                          'list_repeat':game_list_filter_finished})

                if request.POST.get('status') != '' and request.POST.get('status') != 'Status':

                    if str(game.status) == request.POST.get('status'):
                        if game.status == GameStatus.ACTIVE:
                            game_list_filter.append(game)
                        elif game.status == GameStatus.FINISHED:
                            game_list_filter_finished.append(game)
                        elif game.status == GameStatus.CREATED:
                            game_list_filter_join.append(game)

                elif request.POST.get('cat') != '' and request.POST.get('cat') != 'Cat':

                    if game.cat_user.username == request.POST.get('cat'):
                        if game.status == GameStatus.ACTIVE:
                            game_list_filter.append(game)
                        elif game.status == GameStatus.FINISHED:
                            game_list_filter_finished.append(game)
                        elif game.status == GameStatus.CREATED:
                            game_list_filter_join.append(game)

                elif request.POST.get('mouse') != '' and request.POST.get('mouse') != 'Mouse':
                    if game.status != GameStatus.CREATED:
                        if game.mouse_user.username == request.POST.get('mouse'):
                            if game.status == GameStatus.ACTIVE:
                                game_list_filter.append(game)
                            elif game.status == GameStatus.FINISHED:
                                game_list_filter_finished.append(game)
                
                else:
                    return redirect(reverse('select_game'))

                i += 1
                cont += 1

            return render(request, "mouse_cat/select_game.html", {'list_filter':game_list_filter,
                                                                  'list_join':game_list_filter_join,
                                                                  'list_repeat':game_list_filter_finished})

        # JUEGOS SIN FILTRO
        else:
            i = 1
            cont = 1
            while i <= num_juegos:
                try:
                    game = Game.objects.get(id=cont)
                except Game.DoesNotExist:
                    if i <= num_juegos:
                        cont += 1
                        continue
                    Counter.objects.inc()
                    return render(request, "mouse_cat/select_game.html", {'as_cat_play': game_list_cat_play,
                                                                          'as_mouse_play': game_list_mouse_play,
                                                                          'list_join':game_list_join,
                                                                          'list_repeat':game_list_repeat})

                if game.cat_user == request.user and game.status == GameStatus.ACTIVE:
                    game_list_cat_play.append(game)
                if game.mouse_user == request.user and game.status == GameStatus.ACTIVE:
                    game_list_mouse_play.append(game)
                if game.cat_user != request.user and game.status == GameStatus.CREATED:
                    game_list_join.append(game)
                if (game.cat_user == request.user or game.mouse_user == request.user) and game.status == GameStatus.FINISHED:
                    game_list_repeat.append(game) 
                i += 1
                cont += 1

            return render(request, "mouse_cat/select_game.html", {'as_cat_play': game_list_cat_play,
                                                                  'as_mouse_play': game_list_mouse_play,
                                                                  'list_join':game_list_join,
                                                                  'list_repeat':game_list_repeat})


# Funcion show_game_service
# Desc: Renderiza game y muestra el tablero del juego seleccionado, permitiendo movimientos
# si está el juego activo. Si es para repetir, muestra el juego simulado para ver movimientos. 
def show_game_service(request):

    if not request.user.is_authenticated:
        Counter.objects.inc()
        return redirect(reverse('login'))

    form = MoveForm()

    if 'repeat' in request.GET: # Mostrar juego para repeticiones

        if 'simulation' in request.session:
            if request.session['simulation'] is not None:
                game_id = request.session['simulation']
                try:
                    game = Game.objects.get(id=game_id)
                except:
                    Counter.objects.inc()
                    raise Http404("ERROR 404")
            else:
                game_id = request.session[constants.GAME_SELECTED_SESSION_ID]
                game2 = Game.objects.get(id=game_id)
                game = Game(cat_user=game2.cat_user, mouse_user=game2.mouse_user, status=GameStatus.FINISHED, winner=game2.winner)
                game.save()
                request.session['simulation'] = game.id
        else:
            game_id = request.session[constants.GAME_SELECTED_SESSION_ID]
            game2 = Game.objects.get(id=game_id)
            game = Game(cat_user=game2.cat_user, mouse_user=game2.mouse_user, status=GameStatus.FINISHED, winner=game2.winner)
            game.save()
            request.session['simulation'] = game.id

        if game.status == GameStatus.ACTIVE:
            a = 0
        else:
            if game.winner == 1:
                a = 1
            else:
                a = -1  

        original_id = request.session['game_selected']

        tablero = []
        i = 0
        while i < 64:
            tablero.append(0)
            i += 1

        tablero[game.cat1] = 1
        tablero[game.cat2] = 1
        tablero[game.cat3] = 1
        tablero[game.cat4] = 1
        tablero[game.mouse] = -1

        white_cells = [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29, 31, 32, 34, 36, 38, 41, 43, 45, 47, 48, 50,
                    52, 54, 57, 59, 61, 63]
        
        msg_error = None
        if 'error' in request.GET:
            msg_error = 'Movimiento no válido!'

        return render(request, "mouse_cat/game_repetition.html", {'board': tablero, 'game': game, 'move_form': form, 'blancas':white_cells, 
                                                                   'active':a, 'original_id':original_id})

    else: # Mostrar juego para jugar 
        if 'game_selected' in request.session:
            game_id = request.session['game_selected']
        else:
            Counter.objects.inc()
            return redirect(reverse('landing'))

        game = Game.objects.get(id=game_id)

        if game.status == GameStatus.ACTIVE:
            a = 0
        else:
            if game.winner == 1:
                a = 1
            else:
                a = -1  

        tablero = []
        i = 0
        while i < 64:
            tablero.append(0)
            i += 1

        tablero[game.cat1] = 1
        tablero[game.cat2] = 1
        tablero[game.cat3] = 1
        tablero[game.cat4] = 1
        tablero[game.mouse] = -1

        white_cells = [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29, 31, 32, 34, 36, 38, 41, 43, 45, 47, 48, 50,
                    52, 54, 57, 59, 61, 63]
        
        msg_error = None
        if 'error' in request.GET:
            msg_error = 'Movimiento no válido!'

        return render(request, "mouse_cat/game.html", {'board': tablero, 'game': game, 'move_form': form, 'blancas':white_cells, 
                                                       'active':a, 'msg_error':msg_error})


# Funcion move_service
# Desc: Realiza un movimiento en un juego activo por el usuario conectado mediante
# peticion post y un formulario.
def move_service(request):

    if not request.user.is_authenticated:
        Counter.objects.inc()
        return redirect(reverse('login'))

    if request.method == 'POST': # Peticion POST permitida

        base_url = reverse('show_game')

        move_form = MoveForm(data=request.POST)

        if move_form.is_valid():
            user = request.user
            if 'game_selected' in request.session:
                game = Game.objects.get(id=request.session['game_selected'])
            else:
                Counter.objects.inc()
                raise Http404("ERROR 404")

            try:
                move = Move(origin=request.POST.get('origin'),
                            target=request.POST.get('target'), game=game, player=user)
                move.save()
                return redirect(base_url)

            except ValidationError:
                Counter.objects.inc()
                query_string = urlencode({'error':1})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
        else:
            print(move_form.errors)
            return redirect(reverse('landing'))

    # Peticion GET error
    Counter.objects.inc()
    raise Http404("ERROR 404")


# Funcion repeat_game_service
# Desc: Renderiza la pagina de repeat_game, que lista los juegos terminados para
# ver la repeticion. Si se selecciona uno, te lleva a show_game con repeat.
def repeat_game_service(request, game_id=None):

    if not request.user.is_authenticated:
        Counter.objects.inc()
        return redirect(reverse('login'))

    if game_id is not None: # Juego seleccionado para repetir movimientos

        base_url = reverse('show_game')

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            Counter.objects.inc()
            raise Http404("ERROR 404")

        if game.status == GameStatus.CREATED or game.status == GameStatus.ACTIVE:
            Counter.objects.inc()
            raise Http404("ERROR 404")

        if game.cat_user != request.user and game.mouse_user != request.user:
            Counter.objects.inc()
            raise Http404("ERROR 404")

        request.session[constants.GAME_SELECTED_SESSION_ID] = game_id
        if 'simulation' in request.session:
            if request.session['simulation'] is not None:
                try:
                    game = Game.objects.get(id=request.session['simulation'])
                except:
                    return render(request, "mouse_cat/index.html")
                Game.objects.all().filter(id=request.session['simulation']).delete()
            request.session['simulation'] = None
        query_string = urlencode({'repeat':1})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)

    else: # Renderizar repeat_game.html
        game_list_cat = []
        game_list_mouse = []

        num_juegos = len(Game.objects.all())

        if num_juegos == 0:
            return render(request, "mouse_cat/repeat_game.html", {'as_cat': game_list_cat,
                                                                  'as_mouse': game_list_mouse})

        i = 1
        cont = 1
        while i <= num_juegos:
            try:
                game = Game.objects.get(id=cont)
            except Game.DoesNotExist:
                if i <= num_juegos:
                    cont += 1
                    continue
                Counter.objects.inc()
                return render(request, "mouse_cat/repeat_game.html", {'as_cat': game_list_cat,
                                                                      'as_mouse': game_list_mouse})

            if game.status == GameStatus.CREATED or game.status == GameStatus.ACTIVE:
                i += 1
                cont += 1
                continue
            if game.cat_user == request.user:
                game_list_cat.append(game)
            if game.mouse_user == request.user:
                game_list_mouse.append(game)
            i += 1
            cont += 1

        return render(request, "mouse_cat/repeat_game.html", {'as_cat': game_list_cat,
                                                              'as_mouse': game_list_mouse})

# Funcion get_move_service
# Desc: Devuelve, por peticion POST, el siguiente movimiento en el orden que toque,
# o el anterior movimiento, de un juego que se está reproduciendo.
def get_move_service(request):

    if request.method == 'POST': # Peticion POST permitida
        game_id = request.session[constants.GAME_SELECTED_SESSION_ID]

        shift = int(request.POST.get('shift'))

        if shift == 1: # Siguiente movimiento

            # Obtenemos anterior movimiento (guardado en sesion)
            if 'last_move' in request.session:
                if request.session['last_move'] is not None:
                    last_move = request.session['last_move']
                else:
                    last_move = 0
            else:
                last_move = 0

            num_moves = len(Move.objects.all())
            i = 0
            flag = 0
            next = False
            if last_move == 0:
                previous = False
            else:
                previous = True
            nextMove = None
            # Bucle para buscar el siguiente movimiento
            while i < num_moves:
                try:
                    move = Move.objects.get(id=last_move+1)
                except Move.DoesNotExist:
                    Counter.objects.inc()
                    last_move += 1
                    i += 1
                    continue
                
                # Si se encuentra, se guardan los valores 
                if move.game.id == game_id:
                    if flag == 1:
                        next = True
                        break
                    nextMove = move
                    origin = move.origin
                    target = move.target
                    previous = True
                    flag = 1

                last_move += 1
                i += 1 

            # Si no se encuentra, es que ya ha acabado el juego
            if nextMove is None:
                dump = json.dumps({'error_msg':'Error. El juego ya ha finalizado!'})
                response = HttpResponse(dump, content_type='application/json')
                return response

            # Guardamos movimiento encontrado en la sesion
            request.session['last_move'] = nextMove.id

            # Devolvemos respuesta Http con el diccionario json del siguiente movimiento
            dump = json.dumps({'origin':origin, 'target':target, 'previous':previous, 'next':next})
            response = HttpResponse(dump, content_type='application/json')
            return response
 
        elif shift == -1: # Anterior movimiento

            # Obtenemos anterior movimiento (guardado en sesion)
            if 'last_move' in request.session:
                if request.session['last_move'] is not None:
                    last_move = request.session['last_move']
                else:
                    last_move = 0
            else:
                last_move = 0

            i = last_move
            flag = 0
            next = False
            previous = False
            prevMove = None
            origin = 0
            target = 0
            # Bucle para buscar el anterior movimiento
            while i >= 1:
                try:
                    move = Move.objects.get(id=i)
                except Move.DoesNotExist:
                    Counter.objects.inc()
                    i -= 1
                    continue
                
                 # Si se encuentra, se guardan los valores 
                if move.game.id == game_id:
                    if flag == 1:
                        request.session['last_move'] = i
                        previous = True
                        break
                    next = True
                    prevMove = move
                    origin = move.origin
                    target = move.target
                    flag = 1

                i -= 1 

            # Si no se encuentra, estamos en el inicio de la partida
            if i == 0:
                request.session['last_move'] = None

            # Devolvemos respuesta Http con el diccionario json del anterior movimiento
            dump = json.dumps({'origin':origin, 'target':target, 'previous':previous, 'next':next})
            response = HttpResponse(dump, content_type='application/json')
            return response

        else: # Shift no permitido
            Counter.objects.inc()
            raise Http404("ERROR 404")

    else: # Peticion GET no permitida
        Counter.objects.inc()
        raise Http404("ERROR 404")