from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from .models import Maze

def index(request):
    return HttpResponse("Hello, world. You're at the maze index.")

def getMaze(request, width, height):
    if request.method != "GET":
      # Validate request params
      if (width < 4 or width > 100):
          return HttpResponseBadRequest("Invalid maze width. 4 <= WIDTH <= 100", status=400)
      if (height < 4 or height > 100):
          return HttpResponseBadRequest("Invalid maze height. 4 <= HEIGHT <= 100", status=400)

      # Generate maze with width * height dimensions
      newMaze = Maze(width, height)
      
      return JsonResponse(newMaze.getMaze(), safe=False)