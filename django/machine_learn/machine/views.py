from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from machine.models import User
from .script.board import Board


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
        name = "ケイ"
        password = "abc303"
        user_id = "kei"
        info = {
            "name": name,
            "user_id": user_id,
            "password": password
        }

        if len(User.objects.filter(user_id=user_id, password=password)) == 0:
            User.objects.create(**info)
        context={}
        if "c" in c:
            context=c["c"]

        request.session["next"] = request.META.get('HTTP_REFERER','/top')

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



def TopView(request):
    if not check_login(request):
        print(request.session)
        return redirect("/login")
    # if not "board" in request.session:
    #     request.session["board"] = Board()
    # board = request.session["board"]
    # board.add()
    # print(board.x)
    return render(request, "top.html")
