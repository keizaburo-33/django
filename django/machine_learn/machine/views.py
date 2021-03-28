import random
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from machine.models import User
from .script.board import Board
from .script.othello_learner import OthelloPlayer
from .script.common.common_script import encode_and_save_session, get_session_object


# Create your views here.


def check_login(request):
    if "user_id" not in request.session:
        return False
    return True


def log_out(request):
    request.session.clear()
    return redirect("/login")


class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request, *args, **c):
        name = "タオ"
        password = "thao1231"
        user_id = "thao"
        info = {
            "name": name,
            "user_id": user_id,
            "password": password
        }

        if len(User.objects.filter(user_id=user_id, password=password)) == 0:
            User.objects.create(**info)
        context = {}
        if "c" in c:
            context = c["c"]

        request.session["next"] = request.META.get('HTTP_REFERER', '/top')

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = request.POST["user_id"]
        password = request.POST["password"]
        x = User.objects.filter(user_id=user_id, password=password)
        if len(x) == 0:
            return self.get(request, c={"message": "ユーザー名かパスワードが違います。"})
        request.session["user_id"] = user_id
        request.session["user_name"] = x.first().name
        return redirect("/top")


def top_view(request):
    if not check_login(request):
        return redirect("/login")
    if not "board" in request.session:
        encode_and_save_session(request, Board(), "board")
    board = get_session_object(request, "board")
    encode_and_save_session(request, board, "board")
    return render(request, "top.html")


class OthelloView(TemplateView):
    template_name = "othello.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


def put_stone(request):
    cell = request.GET["cell"]
    if cell == "start":
        turn = int(request.GET["turn"])
        board = Board()
        com_turn = 1 if turn == 2 else 2
        othello_player = OthelloPlayer(com_turn, start_read=8)
        if turn == 2:
            pos = othello_player.get_agent_put_pos(board.board, board.turn, board.pss)
            board.put_stone(pos)
        encode_and_save_session(request, board, "board")
        encode_and_save_session(request, othello_player, "othello_player")
        return HttpResponse(board.get_flatten_board())
    board: Board = get_session_object(request, "board")
    othello_player: OthelloPlayer = get_session_object(request, "othello_player")
    pos = board.num_to_pos(cell)
    if not board.is_available(pos):
        return HttpResponse("failure")
    board.put_stone(pos)
    while True:
        com_available_pos_list = board.search_available()
        if len(com_available_pos_list) == 0:
            board.pss += 1
            board.turn_change()
            encode_and_save_session(request, board, "board")
            encode_and_save_session(request, othello_player, "othello_player")
            return HttpResponse(board.get_flatten_board())
        pos = othello_player.get_agent_put_pos(board.board, board.turn, board.pss)
        board.put_stone(pos)
        if len(board.search_available()) != 0:
            break
        board.pss += 1
        board.turn_change()

    encode_and_save_session(request, board, "board")
    encode_and_save_session(request, othello_player, "othello_player")
    return HttpResponse(board.get_flatten_board())


def test_view(request):
    return render(request, "test.html")
