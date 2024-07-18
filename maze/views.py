from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
import json
from .models import Maze

class MazeView(APIView):

  ## Generate a maze
  def get(self, request, width, height):
    # Validate request params
    errroMessage = Maze.validateMazeParams(width, height)
    if (errroMessage is not None):
      return HttpResponseBadRequest(errroMessage, status=400)

    # Generate maze with width * height dimensions
    newMaze = Maze(width, height)
    output = newMaze.getMaze()
      
    return JsonResponse(output, safe=False)
  

  ## Solve a maze
  def post(self, request, width, height):
    # Solve Maze
    mazeData = json.loads(request.data)
    
    # Validate request params
    errroMessage = Maze.validateMazeParams(width, height, mazeData)
    if (errroMessage is not None):
      return HttpResponseBadRequest(errroMessage, status=400)
    
    # Initialize maze and solve
    mazeSolver = Maze(width, height, mazeData)
    solvedPath = mazeSolver.solveMaze()
    
    return JsonResponse(solvedPath, safe=False)