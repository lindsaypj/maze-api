# Maze API

### Deployment
[http://18.191.133.226:8000/](http://18.191.133.226:8000/)

[Demo Client Application](http://maze-client.s3-website.us-east-2.amazonaws.com/)

## Endpoints
### GET /maze/\<width>x\<height>/
Generates a random maze of size width/height. Returns Maze object containing each cell in the maze. For each cell, there is an array of directions that can be traversed.

Note:
 - Width and height must be between 4 and 100 (inclusive)
 - 0 = North, 1 = East, 2 = South, 3 = West
```
   0
3 [ ] 1
   2
```

Example:

GET `http://18.191.133.226:8000/maze/5x5/`

Response:
```
{
  "0": [1],
  "1": [2, 3],
  "2": [2],
  "3": [2],
  "4": [2],
  "5": [1],
  "6": [0, 2, 3],
  "7": [0, 1],
  "8": [0, 2, 3],
  "9": [0, 2],
  "10": [2],
  "11": [0, 1],
  "12": [1, 2, 3],
  "13": [0, 1, 2, 3],
  "14": [0, 3],
  "15": [0, 1, 2],
  "16": [1, 3],
  "17": [0, 2, 3],
  "18": [0],
  "19": [2],
  "20": [0, 1],
  "21": [3],
  "22": [0, 1],
  "23": [1, 3],
  "24": [0, 3]
}
```
<img src="https://github.com/user-attachments/assets/d73b64dd-bb7f-48af-9a0d-b79d15673c4b" width="250" height="250" alt="Example five by five maze fully rendered" />

### POST /maze/\<width>x\<height>/
Solves a given maze of size width/height. Returns an array of cells to traverse (in order) from start to end of the maze.

Notes:
 - Width and height must be between 4 and 100 (inclusive)
 - Maze data must match the given width/height
 - Assumes starting point of cell 0 (top left) to cell n (bottom right)

Example:

POST `http://18.191.133.226:8000/maze/5x5/`
Request Body:
```
{
  "0": [1, 2],
  "1": [1, 2, 3],
  "2": [3],
  "3": [1],
  "4": [2, 3],
  "5": [0],
  "6": [0, 2],
  "7": [2],
  "8": [1, 2],
  "9": [0, 2, 3],
  "10": [1, 2],
  "11": [0, 3],
  "12": [0, 2],
  "13": [0, 2],
  "14": [0],
  "15": [0, 1],
  "16": [1, 3],
  "17": [0, 1, 2, 3],
  "18": [0, 1, 3],
  "19": [3],
  "20": [1],
  "21": [1, 3],
  "22": [0, 1, 3],
  "23": [1, 3],
  "24": [3]
}
```

Response:
```
[0, 1, 6, 11, 10, 15, 16, 17, 22, 23, 24]
```
<img src="https://github.com/user-attachments/assets/1c5a775c-fbe1-4f89-95b9-d72bf85bbf2b" width="250" height="250" alt="Example Five by five maze fully rendered with solved path" />

### Possible additions
 - Modify POST `http://18.191.133.226:8000/maze/5x5/` to accept custom start and end locations
