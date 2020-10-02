import turtle
from random import *

turtle.speed(10)
turtle.shape('turtle')
turtle.color('red')
for n in range(1, 100, 1):
    turtle.forward(randint(15, 60))
    turtle.right(randint(1, 360))
    turtle.left(randint(1, 360))
