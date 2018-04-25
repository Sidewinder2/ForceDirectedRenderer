import pygame as pg

class NodeRenderer:
    node_color = dict()
    node_color["selected"] = (0,255,0)
    node_color["unselected"] = (255,255,255)

    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y
        self.new_x = x  # used in physics calculations
        self.new_y = y  # used in physics calculations
        self.connections = set()    # the nodes it's connected to
        self.selected = False   # if the node has been selected by the user
        font = pg.font.Font(None, 24)
        self.txt_surface = font.render(self.name, True, (0, 0, 0))

    def addConnection(self,node):
        self.connections.add(node)

    def removeConnection(self,node):
        if node in self.connections:
            self.connections.remove(node)

    def renderNode(self,surface, render_names, render_name_selected = True):
        if self.selected:
            pg.draw.circle(surface, NodeRenderer.node_color["selected"], [int(self.x), int(self.y)], 5)
        else:
            pg.draw.circle(surface, NodeRenderer.node_color["unselected"], [int(self.x), int(self.y)], 5)
        if render_names or (render_name_selected and self.selected):

            surface.blit(self.txt_surface, (self.x,self.y))