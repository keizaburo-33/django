import pickle
import base64
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from machine.models import User
from .script.board import Board
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
    if cell=="start":
        board = Board()
        encode_and_save_session(request, board, "board")
        return HttpResponse(board.get_flatten_board())
    board=get_session_object(request,"board")
    board.putstone(cell)
    encode_and_save_session(request, board, "board")
    return HttpResponse(board.get_flatten_board())


def test_view(request):
    return render(request, "test.html")
