import pygame as pg
import os
import GraphRenderer
from random import randint

def main():

    # set up screen, and rendering options
    font_size = 20

    screen_width = 1200
    screen_height = 800

    screen = pg.display.set_mode((screen_width, screen_height))
    font = pg.font.Font(None, font_size)
    clock = pg.time.Clock()

    color = pg.Color('dodgerblue2')

    # console vars
    user_input_text = ''   # current user input
    console_text_log = []
    console_shutdown = False
    console_shutdown_command = "close"

    # create a list of numbers for node names
    nodes = list()
    for x in range(100):
        nodes.append(str(x))
    # add a bunch of ndoes to the renderer
    GraphRenderer.GraphRenderer.addNodes(nodes,screen_width, screen_height)


    GraphRenderer.GraphRenderer.selectNodes((0,0),(200,200))

    # randomly add connections between the nodes
    for x in range(100):
        GraphRenderer.GraphRenderer.addConnections(nodes[randint(0,len(nodes) -1)], nodes[randint(0,len(nodes) - 1)])

    # main loop
    while not console_shutdown:

        # fill the screen with a color
        screen.fill((30, 30, 30))

        # Iterate through events, looking for user inputs
        for event in pg.event.get():

            # user hits close window
            if event.type == pg.QUIT:
                return

            # mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:   # left press
                    GraphRenderer.GraphRenderer.leftMbPress(pg.mouse.get_pos())
            # mouse release
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:   # left release
                    GraphRenderer.GraphRenderer.leftMbRelease(pg.mouse.get_pos())

            # if any keyboard key pressed
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    # if user presses enter then add text to console log
                    print(user_input_text)
                    console_text_log.insert(0,'[CLIENT] ' + user_input_text)

                    # on command, exit the console and sever connection
                    if user_input_text == console_shutdown_command:
                        console_shutdown = True
                        break

                    # reset input text
                    user_input_text = ''

                elif event.key == pg.K_BACKSPACE:
                    user_input_text = user_input_text[:-1]
                else:
                    user_input_text += event.unicode

        # drawing location variables
        console_x = 20
        console_y_increment = 20
        console_y = 20

        # print current user input

        txt_surface = font.render(":" +user_input_text, True, color)
        screen.blit(txt_surface, (console_x, console_y))

        console_y += console_y_increment

        # print  "console log"  messages below
        for t in console_text_log:
            txt_surface = font.render(t, True, color)
            screen.blit(txt_surface, (console_x, console_y))
            console_y += console_y_increment

        # calculat node positions and render them
        GraphRenderer.GraphRenderer.computeForces()
        GraphRenderer.GraphRenderer.renderNodes(screen)
        #GraphRenderer.GraphRenderer.renderNodeForces(screen)
        GraphRenderer.GraphRenderer.renderNodeConnections(screen)
        GraphRenderer.GraphRenderer.renderSelectionBox(screen)

        # wipe the display
        pg.display.flip()
        clock.tick(30)




if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()