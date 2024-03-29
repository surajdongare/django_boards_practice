from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from boards.models import Board, Post, Topic, User
from .forms import NewTopicForm

# Create your views here.

# def home(request):
#     return HttpResponse("Hello, World!")


def home(request):
    # boards = Board.objects.all()
    # boards_names = list()    # []
    # for board in boards:
    #     boards_names.append(board.name)

    # response_html = '<br>'.join(boards_names)
    # # print(response_html)
    # # return HttpResponse(response_html)
    return render(request, "home.html", context={"all_boards": Board.objects.all()})


def board_topics(request, pk):
    # # print("In board topics", type(pk))
    # try:
    #     board_obj = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404

    board_obj = get_object_or_404(Board, pk=pk)
    return render(request, "topics.html", {"board": board_obj})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )

            return redirect("board_topics", pk=board.pk)
    else:
        form = NewTopicForm()
    
    return render(request, "new_topic.html", {'board': board, 'form': form})


