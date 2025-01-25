from random import choice
import os

file_dir = os.path.dirname(__file__)
red = os.path.join(file_dir, "icons/red.webp")
yellow = os.path.join(file_dir, "icons/yellow.webp")
purple = os.path.join(file_dir, "icons/purple.webp")
green = os.path.join(file_dir, "icons/green.webp")
blue = os.path.join(file_dir, "icons/blue.webp")
cyan = os.path.join(file_dir, "icons/cyan.webp")
orange = os.path.join(file_dir, "icons/orange.webp")

colors = {"I": cyan, "O": yellow, "T": purple, "S": green, "Z": red, "J": blue, "L": orange}

shapes = {
    "I": [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],

        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],

        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],

        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]
    ],

    "J": [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],

        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 1]],

        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]]
    ],

    "L": [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],

        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 0]],

        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]]
    ],

    "O": [[[0, 1, 1],
           [0, 1, 1]]],

    "S": [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],

        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]],

        [[0, 0, 0],
         [0, 1, 1],
         [1, 1, 0]],

        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],

    "T": [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]],

        [[0, 0, 0],
         [1, 1, 1],
         [0, 1, 0]],

        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],

    "Z": [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],

        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]],

        [[0, 0, 0],
         [1, 1, 0],
         [0, 1, 1]],

        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]]
    ]
}

class Tetromino:
    def __init__(self):
        self.name = choice(list(shapes.keys()))
        self.shapes = shapes[self.name]
        self.icon = colors[self.name]
        self.coords = None
        self.last_coords = None
        self.x = 3
        self.y = 0
        self.__rotation = 0
        self.get_positions()

    def get_positions(self) -> None:
        self.last_coords = self.coords
        coords = []
        for y, row in enumerate(self.shapes[self.__rotation]):
            for x, block in enumerate(row):
                if block:
                    coords.append((self.x + x, self.y + y))
        self.coords = coords

    
    def rotate(self, direction) -> list[tuple[int, int]]: 
        self.__rotation = (self.__rotation + direction) % 4
        self.get_positions()
    
    def move(self, x, y) -> None:
        self.x += x
        self.y += y
        self.get_positions()

    def reset(self) -> None:
        self.x = 3
        self.y = 0
        self.__rotation = 0
        self.get_positions()
    

    