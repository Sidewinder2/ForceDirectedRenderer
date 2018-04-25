import pygame as pg
import os
import UIGraph
import ClickHandler
import UIButton
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
    for x in range(0):
        nodes.append(str(x))
    # add a bunch of ndoes to the renderer
    UIGraph.GraphRenderer.addNodes(nodes, screen_width, screen_height)

    # make a test selection
    UIGraph.GraphRenderer.selectNodes((0, 0), (200, 200))

    # randomly add connections between the nodes
    for x in range(0):
        UIGraph.GraphRenderer.addConnections(nodes[randint(0, len(nodes) - 1)], nodes[randint(0, len(nodes) - 1)])

    # create some buttons
    UIButton.GreenButton(coords = (300,40), dimensions = (200,20), text = "Remove Selected Nodes", color = (255,255,255), text_color = (255,255,255))





    # wiki bot stuff
    from selenium import webdriver
    from time import sleep
    from random import shuffle

    gatherWikiStuff = True
    visited_webpages = set()
    unvisited_webpages = set()


    webpage_queue = list()
    total_link_count = 0
    timedelay = 600

    max_nodes = 40
    max_page_links = 5

    if gatherWikiStuff:

        # initialize driver as chrome
        driver = webdriver.Chrome()
        # tell driver to go to website
        current_url = 'https://en.wikipedia.org/wiki/Google'
        driver.get(current_url)
        sleep(1)

        UIGraph.GraphRenderer.addNodes([current_url.replace('https://en.wikipedia.org/wiki/',"")], screen_width, screen_height)
        unvisited_webpages.add(current_url)
        # Supergraph.addnode(current_url, override = False)







    # main loop
    while not console_shutdown:

        # close wikibot when it's visited enough pages
        if len(visited_webpages) >= max_nodes and gatherWikiStuff:
            driver.close()
            gatherWikiStuff = False

        # wiki bot stuff
        timedelay -= 1
        if timedelay < 0 and gatherWikiStuff:
            timedelay = 150
            if (len(visited_webpages) < max_nodes and len(unvisited_webpages) > 0):
                elems = driver.find_elements_by_xpath("//a[@href]")
                page_link_count = 0  # tracks valid links per page
                shuffle(elems)  # randomize the link order

                for elem in elems:
                    linktext = elem.get_attribute("href")
                    if (max_page_links == -1) or (max_page_links > 0 and page_link_count < max_page_links):
                        if is_valid_link(linktext):
                            if linktext not in visited_webpages and linktext not in unvisited_webpages:
                                # addnode(linktext, override = false)
                                # addconnections(current_url, linktext)
                                UIGraph.GraphRenderer.addNodes([linktext.replace('https://en.wikipedia.org/wiki/',"")], screen_width, screen_height)
                                UIGraph.GraphRenderer.addConnections(current_url.replace('https://en.wikipedia.org/wiki/',""),linktext.replace('https://en.wikipedia.org/wiki/',""))

                                unvisited_webpages.add(linktext)
                                webpage_queue.append(linktext)
                                page_link_count += 1
                                total_link_count += 1
                    else:
                        break

                print(current_url, "page edges: ", page_link_count, "total nodes: ",
                      len(visited_webpages) + len(unvisited_webpages), "total edges: ", total_link_count)

                # move on to the next page
                current_url = webpage_queue.pop(0)
                unvisited_webpages.remove(current_url)
                visited_webpages.add(current_url)
                driver.get(current_url)






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
                    ClickHandler.ClickHandler.leftMbPress(pg.mouse.get_pos())
            # mouse release
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:   # left release
                    ClickHandler.ClickHandler.leftMbRelease(pg.mouse.get_pos())

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

        # calculate node positions and render them
        #UIGraph.GraphRenderer.computeForces()
        UIGraph.GraphRenderer.computeForcesGrid()
        UIGraph.GraphRenderer.renderNodes(screen, False)
        #GraphRenderer.GraphRenderer.renderNodeForces(screen)
        UIGraph.GraphRenderer.renderNodeConnections(screen)
        ClickHandler.ClickHandler.renderSelectionBox(screen)
        UIButton.UIButton.renderButtons(screen)

        #print(UIGraph.GraphRenderer.getNodeGridSpace(200))

        # wipe the display
        pg.display.flip()
        clock.tick(30)





def is_valid_link(linktext):
    if linktext.count("https://en.wikipedia.org") == 0:
        return False

    blacklist_items = ["#","Portal:","Special:","Category:","Help:","Wikipedia:","Template:","Template_talk:",
                       "Talk:","File:","Help:","w/index",".png",".jpg"]
    for item in blacklist_items:
        if linktext.count(item):
            return False
    return True








if __name__ == '__main__':
    pg.init()
    main()

    pg.quit()