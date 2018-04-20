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

    def addConnection(self,node):
        self.connections.add(node)

    def removeConnection(self,node):
        self.connections.remove(node)

    def renderNode(self,surface):
        if self.selected:
            pg.draw.circle(surface, NodeRenderer.node_color["selected"], [int(self.x), int(self.y)], 5)
        else:
            pg.draw.circle(surface, NodeRenderer.node_color["unselected"], [int(self.x), int(self.y)], 5)