from enum import IntEnum
import random


### Generates a maze with only one path from any given cell to another
class Maze():
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.cellCount = width * height
    self.sets = DisjointSets(self.cellCount)
    self.graph = MazeGraph(self.cellCount)
    self.__generate()

  # Method to generate the maze
  def __generate(self):
    generatedCells = [i for i in range(self.cellCount)]

    # Loop over cells until minimum spanning tree is reached
    while(self.graph.getEdgeCount() < self.cellCount - 1):
      # Randomly select from generated cells using Fisher-Yates algorithm
      for i in range(self.cellCount - 1, 1, -1):
        nextCellIndex = random.randint(0, i)
        nextCell = generatedCells[nextCellIndex]
        self.__swap(nextCellIndex, i, generatedCells)

        neighbor = None
        neighbors = self.__randomNeighbors()
        # Loop over neighboring cells until cell is merged or all neighbors exhausted
        for counter in range(0, 4):
          neighbor = self.__getNeighborCell(nextCell, neighbors[counter])
          if (neighbor != -1 and not self.sets.sameSet(nextCell, neighbor)):
            self.sets.union(nextCell, neighbor)
            self.graph.addEdge(nextCell, neighbor)
            break
        # Break early if requirements are met
        if (self.graph.getEdgeCount() == self.cellCount - 1):
          break

  # Method to get the current maze (for response)
  def getMaze(self):
    return self.graph.cellMap()

  def __swap(self, firstIndex, secondIndex, array):
    firstValue = array[firstIndex]
    array[firstIndex] = array[secondIndex]
    array[secondIndex] = firstValue

  def __randomNeighbors(self):
    neighbors = [0,1,2,3]
    for i in range(3, 0, -1):
      self.__swap(i, random.randint(0, i), neighbors)
    return neighbors
  
  def __getNeighborCell(self, cell, direction):
    match(direction):
      case 0: # NORTH
          northNeighbor = cell - self.width
          return -1 if northNeighbor < 0 else northNeighbor
      case 1: # EAST
          # If (cell + 1) % width == 0, then cell is at the end of a row
          return -1 if (cell + 1) % self.width == 0 else cell + 1
      case 2: # SOUTH
          southNeighbor = cell + self.width
          return -1 if southNeighbor >= self.cellCount else southNeighbor
      case 3: # WEST
          # If cell % width == 0, then cell is at the start of a row
          return -1 if cell % self.width == 0 else cell - 1
      case _:
          return -1


### Used to track disjoint parts of the maze durring generation, ensuring result is a spanning tree
### Implements the Union-Find algorithim
class DisjointSets():
  def __init__(self, numSets):
    self.sets = [-1] * numSets

  def find(self, element):
    if (self.sets[element] < 0):
      return element
    self.sets[element] = self.find(self.sets[element])
    return self.sets[element]
  
  def union(self, first, second):
    firstRoot = self.find(first)
    secondRoot = self.find(second)
    if (firstRoot != secondRoot):
      if (self.sets[firstRoot] < self.sets[secondRoot]):
        self.sets[secondRoot] = firstRoot
      elif (self.sets[secondRoot] < self.sets[firstRoot]):
        self.sets[firstRoot] = secondRoot
      elif (self.sets[firstRoot] == self.sets[secondRoot]):
        self.sets[secondRoot] = firstRoot
        self.sets[firstRoot] -= 1
      return True
    return False
  
  def sameSet(self, first, second):
    return self.find(first) == self.find(second)


### Manages rendering info for an individual cell in maze
class Cell():
  def __init__(self):
    self.doors = [True] * 4

  def setDoor(self, door):
    self.doors[door] = False

  def getDoors(self):
    return self.doors

  # Enum to easily identify a wall based on direction
  class Doors(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

  def getPaths(self):
    paths = []
    for wall in range(4):
      if not self.doors[wall]:
        paths.append(wall)
    return paths

  def __str__(self):
    paths = self.getPaths()
    return str(paths)


### Graph used to track maze pathing
class MazeGraph():
  def __init__(self, vertexCount):
    self.edgeCount = 0
    self.adjacencyLists = {}
    for i in range(vertexCount):
      self.adjacencyLists[i] = None

  def getEdgeCount(self):
    return self.edgeCount
  
  def __containsVertex(self, search):
    return self.adjacencyLists[search] != None
  
  # Method to add an edge between two cells in the graph, indicating a path from one to the other
  def addEdge(self, first, second):
    if (self.__containsEdge(first, second)):
      return
    self.__addDirectedEdge(first, second)
    self.__addDirectedEdge(second, first)
    self.edgeCount += 1

  def __addDirectedEdge(self, first, second):
    oldHead = self.adjacencyLists[first]
    if (oldHead is None):
      self.adjacencyLists[first] = self.Node(second)
    else:
      self.adjacencyLists[first] = self.Node(second, oldHead)

  def __containsEdge(self, first, second):
    if (self.__containsVertex(first) and self.__containsVertex(second)):
      current = self.adjacencyLists[first]
      while(current != None):
        if (current.vertex == second):
          return True
        current = current.next
    return False

  # TODO: THIS WILL PROBABLY BREAK IF MAZE IS NOT SQUARE (e.g. 5x5/45x45/100x100)
  def cellMap(self):
    cells = {}
    for key, currentNode in self.adjacencyLists.items():
      
      newCell = Cell()
      while (currentNode != None):
          wallReference = key - currentNode.vertex
          if (wallReference < 0):
              if (wallReference == -1):
                  newCell.setDoor(Cell.Doors.EAST)
              else:
                  newCell.setDoor(Cell.Doors.SOUTH)
          else:
              if (wallReference == 1):
                  newCell.setDoor(Cell.Doors.WEST)
              else:
                  newCell.setDoor(Cell.Doors.NORTH)
          currentNode = currentNode.next
      cells[key] = newCell.getPaths()
    return cells

  # Subclass of MazeGraph used to identify cells in the graph
  class Node():
    def __init__(self, otherVertex:int, nextNode=None):
      self.vertex:int = otherVertex
      self.next:self = nextNode
