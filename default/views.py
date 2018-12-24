from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from default.models import Todo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def index(request):
    return render(request,"index.html")


@login_required
def todolist(request):
    dataset =Todo.objects.filter(user=request.user)
    todolist = []
    for item in dataset:
        temp ={"id":item.id,"content":item.content}
        todolist.append(temp)
    res ={"todolist":todolist}
    return JsonResponse(res)

@csrf_exempt
@login_required
def todoadd(request):
    todo = request.POST['todo']
    Todo.objects.create(content=todo,user=request.user)
    res ={"success":"true"}
    return JsonResponse(res)


@csrf_exempt
@login_required
def todoupdate(request,todoid):
    content = request.POST['todo']
    todo = Todo.objects.get(id=todoid)
    todo.content =content
    todo.save()
    res ={"success":"true"}
    return JsonResponse(res)

@login_required
def tododel(request,todoid):
    Todo.objects.get(id=todoid).delete()
    res ={"success":"true"}
    return JsonResponse(res)


def mylogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect("/")
        else:
            errmsg = "用户名/密码输入错误"
        return render(request, 'login.html',{'errmsg':errmsg})
    else:
        return render(request, 'login.html',{'errmsg':""})


@login_required
def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username = username).exists():
            user = User.objects.create_user(username, '',password)
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            errmsg = "该用户名已被注册"
            return render(request, 'register.html',{'errmsg':errmsg})
    else:
        return render(request, 'register.html', {'errmsg': ""})
