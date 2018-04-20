import VectorMath
import pygame as pg
import UIGraph
import UIButton

class ClickHandler:
    mouse_press_coords = (0, 0)  # mouse coords at time of left click
    mouse_release_coords = (0, 0)  # mouse coords at time of left release
    mouse_is_down = False
    
    def leftMbPress(coords = (0,0)):
        ClickHandler.mouse_press_coords = coords
        ClickHandler.mouse_is_down = True

    def leftMbRelease(coords=(0, 0)):
        ClickHandler.mouse_release_coords = coords
        ClickHandler.mouse_is_down = False

        # select group of nodes if you made a selection box big enough to not be an accident or single click
        if VectorMath.distance(ClickHandler.mouse_press_coords, ClickHandler.mouse_release_coords) > 10:
            UIGraph.GraphRenderer.selectNodes(ClickHandler.mouse_press_coords, ClickHandler.mouse_release_coords)
        else:
            # if single click, check for buttons
            for button in UIButton.UIButton.buttons:
                button.checkClicked(ClickHandler.mouse_release_coords)


    def renderSelectionBox(surface, color = (255,255,255)):
        # renders a selection box in given color
        if ClickHandler.mouse_is_down:
            width = pg.mouse.get_pos()[0] - ClickHandler.mouse_press_coords[0]
            height =  pg.mouse.get_pos()[1] - ClickHandler.mouse_press_coords[1]
            pg.draw.rect(surface, color, [ClickHandler.mouse_press_coords,(width,height)], 1)