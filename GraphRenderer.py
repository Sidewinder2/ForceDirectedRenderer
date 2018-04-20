import NodeRenderer as NR
import VectorMath
from math import log10
import pygame as pg
from random import randint

class GraphRenderer:
    name_to_node = dict()
    mouse_press_coords = (0,0)  # mouse coords at time of left click
    mouse_release_coords = (0,0)    # mouse coords at time of left release
    mouse_is_down = False

    def addNodes(nodenames,xrange, yrange):
        for nodename in nodenames:
            if nodename not in GraphRenderer.name_to_node.keys():
                GraphRenderer.name_to_node[nodename] = NR.NodeRenderer(nodename,randint(0,xrange),randint(0,yrange))

    def addConnections(left,right):
        GraphRenderer.name_to_node[left].addConnection(GraphRenderer.name_to_node[right])
        GraphRenderer.name_to_node[right].addConnection(GraphRenderer.name_to_node[left])


    def computeForces(constant_force = 2,strong_force = 2000, friction_threshold = 1):
        # calculate the forces for all nodes
        for node in GraphRenderer.name_to_node.values():
            vect_sum_x = 0
            vect_sum_y = 0
            vect_sum_count = 0

            #create pulling forces between adjacent nodes
            for conn in node.connections:
                if conn != node:
                    dist = VectorMath.distance((node.x,node.y),(conn.x,conn.y))
                    direction = VectorMath.point_direction((node.x, node.y), (conn.x, conn.y))
                    pull_vect = VectorMath.polar_to_cartesian(direction,constant_force * log10(dist))
                    vect_sum_x += pull_vect[0]
                    vect_sum_y += pull_vect[1]
                    vect_sum_count += 1

            # create pushing forces from all nodes away from each other

            for conn in GraphRenderer.name_to_node.values():
                if conn != node:
                    dist = VectorMath.distance((node.x, node.y), (conn.x, conn.y))
                    direction = VectorMath.point_direction((conn.x, conn.y), (node.x, node.y))
                    pull_vect = VectorMath.polar_to_cartesian(direction,strong_force / max([1,dist ** 2]))
                    vect_sum_x += pull_vect[0]
                    vect_sum_y += pull_vect[1]
                    vect_sum_count += 1

            # store the new position in a different variable
            node.new_x = vect_sum_x
            node.new_y = vect_sum_y

        # update nodes with new positions
        for node in GraphRenderer.name_to_node.values():
            if VectorMath.distance((0,0),(node.new_x,node.new_y)) > friction_threshold:
                node.x += node.new_x #/ len(GraphRenderer.name_to_node.values()) * 2
                node.y += node.new_y #/ len(GraphRenderer.name_to_node.values()) * 2

    def selectNodes(coords1,coords2):
        # select all nodes in region
        xedges = [coords1[0],coords2[0]]
        xedges.sort()
        yedges = [coords1[1],coords2[1]]
        yedges.sort()
        for node in GraphRenderer.name_to_node.values():
            node.selected = False
            if node.x >= xedges[0] and node.x <= xedges[1]:
                if node.y >= yedges[0] and node.y <= yedges[1]:
                    node.selected = True



    def renderNodes(surface):
        for node in GraphRenderer.name_to_node.values():
            node.renderNode(surface)

    def renderNodeForces(surface,color = (0,0,255)):
        for node in GraphRenderer.name_to_node.values():
            pg.draw.line(surface, color , [int(node.x),int(node.y)],[int(node.x +(node.new_x*30)),int(node.y +(node.new_y*30))], 1)

    def renderNodeConnections(surface,color = (255,0,0)):
        for node in GraphRenderer.name_to_node.values():
            for conn in node.connections:
                pg.draw.line(surface, color , [int(node.x),int(node.y)],[int(conn.x),int(conn.y)], 1)

    def leftMbPress(coords = (0,0)):
        GraphRenderer.mouse_press_coords = coords
        GraphRenderer.mouse_is_down = True

    def leftMbRelease(coords=(0, 0)):
        GraphRenderer.mouse_release_coords = coords
        GraphRenderer.mouse_is_down = False

        # select group of nodes if you made a selection box big enough to not be an accident or single click
        if VectorMath.distance(GraphRenderer.mouse_press_coords, GraphRenderer.mouse_release_coords) > 10:
            GraphRenderer.selectNodes(GraphRenderer.mouse_press_coords, GraphRenderer.mouse_release_coords)

    def renderSelectionBox(surface, color = (255,255,255)):
        # renders a selection box in given color
        if GraphRenderer.mouse_is_down:
            width = pg.mouse.get_pos()[0] - GraphRenderer.mouse_press_coords[0]
            height =  pg.mouse.get_pos()[1] - GraphRenderer.mouse_press_coords[1]
            pg.draw.rect(surface, color, [GraphRenderer.mouse_press_coords,(width,height)], 1)