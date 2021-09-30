from django.shortcuts import redirect, render
from .models import Board, Reply
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    page = request.GET.get('page', 1)
    kw = request.GET.get('kw', '')
    cate = request.GET.get('cate', '')

    if kw:
        if cate == "subject":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "writer":
            b = Board.objects.filter(writer=kw)
        else:
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()
    pag = Paginator(b,10)
    obj = pag.get_page(page)
    context = {
        'con' : obj,
        'kw' : kw,
        'cate' : cate
    }
    return render(request, "board/index.html", context)


def detail(request, num):
    if not request.user.username:
        return redirect("acc:login_user")
    try:
        b = Board.objects.get(id=num)
        r = b.reply_set.all()
        context = {
            'con' : b,
            'rep' : r,
        }
    except:
        return render(request, "error/notfound.html")
    return render(request, "board/detail.html", context)

def create(request):
    if not request.user.username:
        return redirect("acc:login_user")
    if request.method == "POST":
        subject = request.POST.get("subject")
        writer = request.user.username
        content = request.POST.get("content")
        Board(subject=subject, writer=writer, content=content, likey=0).save()
        return redirect('board:index')

    return render(request, "board/create.html")

def delete(request, conid):
    try:
        b = Board.objects.get(id=conid)
        if b.writer == request.user.username:
            b.delete()
        else:
            return render(request, "error/forbidden.html")
    except:
        return render(request, "error/notfound.html")
    return redirect('board:index')

def update(request, conid):
    
    b = Board.objects.get(id=conid)
    if request.user.username == b.writer:
        if request.method == "POST":
            b.subject = request.POST.get("subject")
            b.content = request.POST.get("content")
            b.save()
            return redirect("board:detail", num=conid)
        context = {
            'con' : b
        }
        return render(request, "board/update.html", context)
    else:
        return render(request, "error/forbidden.html")

def create_reply(request, conid):
    b = Board.objects.get(id=conid)
    r = request.user.username
    c = request.POST.get('comment')
    p = request.user.userpic
    Reply(subject=b, replyer=r, comment=c, pic=p).save()
    return redirect('board:detail', num=conid)

def delete_reply(request, conid, num):
    r = Reply.objects.get(id=num)
    if request.user.username == r.replyer:
        r.delete()
    else:
        return render(request, "error/forbidden.html")
    return redirect("board:detail", num=conid)

def up(request, conid):
    b = Board.objects.get(id=conid)
    if request.user in b.up.all():
        return redirect("board:detail", num=conid)
    b.up.add(request.user)
    return redirect("board:detail", num=conid)

def cancel(request, conid):
    b = Board.objects.get(id=conid)
    if request.user in b.up.all():
        b.up.remove(request.user)
    return redirect("board:detail", num=conid)

# b.up.remove(request.user) 하면은 추천취소 가능해요!!
