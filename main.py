#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font
import urandom
import sys


ev3 = EV3Brick()


#реклама
NauRobot_font = Font(size = 32, bold = True)
ev3.screen.set_font(NauRobot_font)
ev3.screen.draw_text(52, 25, ' Nau')
ev3.screen.draw_text(42, 65, 'Robot')
ev3.screen.draw_circle(90, 60, 80)
ev3.screen.draw_circle(91, 60, 80)
ev3.screen.draw_circle(92, 60, 80)
ev3.screen.draw_circle(93, 60, 80) 
ev3.speaker.play_file(SoundFile.MAGIC_WAND)
while not Button.CENTER in (ev3.buttons.pressed()):
    pass
ev3.speaker.play_file(SoundFile.CLICK)
ev3.screen.clear()
wait(300)


while True:
    width = 170  # ширина экрана
    height = 120  # длина экрана

    x = 20 # начальные координаты змеи
    y = 20 # начальные координаты змеи

    delta_x = 10 # для обновления координат x И y. 10 чтобы сразу начать двигаться
    delta_y = 0 # для обновления координат x И y. 10 чтобы сразу начать двигаться

    food_x, food_y = urandom.randint(10, 160) // 10 * 10, urandom.randint(10, 110) // 10 * 10  # еда
    
    body_list = [(x, y)]  # список для хранения координат каждой единицы тела
    body_list.append((x, y))  # добавить в лист. т.е. увеличить длину змеи на один размер(на каждой итерации он будет увеличиваться бесконечно, поэтому нужен del body_list[0]
    body_list.append((x, y))  # добавить в лист. т.е. увеличить длину змеи на один размер(на каждой итерации он будет увеличиваться бесконечно, поэтому нужен del body_list[0]
   
    game_over = False

    bill = 0  # счет
    bill_font = Font(size = 12, bold = True)
    billend_font = Font(size = 30, bold = True)

    def snake():  # функция отображения змеи и еды и счета на экране
        global x, y, food_x, food_y, game_over, bill  # сделать эти переменные глобальными потому что они инициализируются вне функции
        x = (x + delta_x) % 180  # для обновления координат x И y. Чтобы координаты оставались в пределах экрана.
        y = (y + delta_y) % 130  # для обновления координат x И y. Если дошол до края, выйти с другой стороны %

        if ((x, y) in body_list):  # если координаты головы змеи есть в теле этого змеи, значит змея ударилась об себя
            game_over = True
            ev3.speaker.beep(500,700)
           
        body_list.append((x, y))  # добавить в лист. т.е. увеличить длину змеи на один размер(на каждой итерации он будет увеличиваться бесконечно, поэтому нужен del body_list[0]

        if (food_x == x and food_y == y):  # если съел еду, случайно где то разместить еду но не на змее
            ev3.speaker.beep(400, 50)
            bill += 1  # съел, счет увеличиваем
            while ((food_x, food_y) in body_list):  # случайно выбирать место для еды, но если место оказалось на теле змеи тогда снова случайно выбрать
                food_x, food_y = urandom.randint(10, 160) // 10 * 10, urandom.randint(10, 110) // 10 * 10  # еда
        else:
            del body_list[0]  # постоянно удалять лишне увеличивающееся тело. тело увеличивается только когда съедена еда(т.е. del body_list[0] этот код проскакивается)
        ev3.screen.draw_circle(food_x, food_y, 5, fill=True)  # вывести на экран еду
        ev3.screen.set_font(bill_font)  
        ev3.screen.draw_text(88, 1, bill)  # вывести на экран счет
        for (i, j) in body_list:
            ev3.screen.draw_circle(i, j, 5, fill=True)  # вывести на экран змею
        
        wait(150)
        ev3.screen.clear()


    while not game_over: #ev3.speaker.beep()
        
        if Button.DOWN in (ev3.buttons.pressed()) or Button.UP in (ev3.buttons.pressed()) or Button.RIGHT in (ev3.buttons.pressed()) or Button.LEFT in (ev3.buttons.pressed()):     
            
            if Button.DOWN in (ev3.buttons.pressed()):
                delta_x = 0
                if (delta_y != -10):
                    delta_y = 10
                        
            elif Button.UP in (ev3.buttons.pressed()):
                delta_x = 0
                if (delta_y != 10):
                    delta_y = -10

            elif Button.RIGHT in (ev3.buttons.pressed()):
                if (delta_x != -10):  # это нужно чтобы невозможно было движение в противоположное направление сразу
                    delta_x = 10
                delta_y = 0

            elif Button.LEFT in (ev3.buttons.pressed()):
                if (delta_x != 10):  # это нужно чтобы невозможно было движение в противоположное направление сразу
                    delta_x = -10
                delta_y = 0
            
            snake()  # после нажатия сразу показать экран, без задержек
            
        else:  # даже если ничего не нажато змея будет двигаться
            snake()


    # реклама конца
    e = 1
    while e < 5:   
        ev3.screen.draw_circle(food_x, food_y, 5, fill=True)
        for (i, j) in body_list:
            ev3.screen.draw_circle(i, j, 5, fill=True)
        ev3.screen.draw_circle(food_x, food_y, 5, fill=True)
        ev3.screen.set_font(bill_font)
        e = e + 1    
        wait(150)
        ev3.screen.clear()
        wait(150)
    
    while not Button.CENTER in (ev3.buttons.pressed()):     # геймовер. если ...
        ev3.screen.draw_circle(food_x, food_y, 5, fill=True)
        ev3.screen.set_font(bill_font)
        ev3.screen.draw_text(88, 1, bill)
        for (i, j) in body_list:
            ev3.screen.draw_circle(i, j, 5, fill=True)
        if Button.LEFT in(ev3.buttons.pressed()):
            sys.exit() #если нажать кнопку влево вырубить всю программу
    wait(200)
    ev3.screen.clear()
    while not Button.CENTER in (ev3.buttons.pressed()):          
        ev3.screen.set_font(billend_font)
        ev3.screen.draw_text(85, 1, bill)
    
    ev3.screen.clear()
    ev3.speaker.play_file(SoundFile.CONFIRM)

    