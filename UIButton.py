import pygame as pg

class UIButton:
    buttons = set()

    def __init__(self, coords = (0,0), dimensions = (30,30), text = "test", color = (255,255,255), text_color = (0,0,0)):
       self.coords = coords  # mouse coords at time of left click
       self.dimensions = dimensions
       self.text = text
       self.color = color
       self.text_color = text_color
       UIButton.buttons.add(self)

    def checkClicked(self, mouse_coords):
        # tests if button was clicked
        xedges = [self.coords[0], self.coords[0]+self.dimensions[0]]
        xedges.sort()
        yedges = [self.coords[1], self.coords[1]+self.dimensions[1]]
        yedges.sort()
        if mouse_coords[0] >= xedges[0] and mouse_coords[0] <= xedges[1]:
            if mouse_coords[1] >= yedges[0] and mouse_coords[1] <= yedges[1]:
                self.clickEvent()

    def clickEvent(self):
        # override this method for functionality
        return

    def renderButtons(surface):
        # renders all buttons
        for button in UIButton.buttons:
            # draw rectangle for button
            pg.draw.rect(surface, button.color, [button.coords,button.dimensions], 1)
            # draw
            font = pg.font.Font(None, 24)
            txt_surface = font.render(button.text, True, button.text_color)
            surface.blit(txt_surface, button.coords)



class GreenButton(UIButton):
    def clickEvent(self):
        import UIGraph
        UIGraph.GraphRenderer.removeNodes(UIGraph.GraphRenderer.selected_nodes)

