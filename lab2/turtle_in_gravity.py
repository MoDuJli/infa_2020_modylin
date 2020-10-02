import turtle

turtle.speed(10)


def motion(v_x, v_y, a):
    turtle.shape('circle')
    x = 0
    y = 0
    dt = 0.05
    for i in range(1000):
        x += v_x * dt
        y += v_y * dt
        v_y -= a * dt
        turtle.goto(x, y)
        if y < 0:
            v_y = -0.9 * v_y


motion(5, 60, 9.8)
