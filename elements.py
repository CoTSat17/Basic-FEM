import pygame
from menus import Point

class Elements():
        def __init__(self):
                self.element_list = []
                self.new_element_nodes = []

        def add_dalaunay_element(self, points_list:list[Point]):
                """
                From the points generated in "dalaunay" generates the corresponding elements
                """
                for points in points_list:
                        new_element = Element(points)
                        self.element_list.append(new_element)                        



        def add_element_manually(self, node):
                """
                Adds the selected "node" to the new element that's being created, when it reaches 4 saves the new element
                """
                if node not in self.new_element_nodes:
                        self.new_element_nodes.append(node)
                if len(self.new_element_nodes) == 4:
                        new_element = Element(self.new_element_nodes.copy())
                        self.element_list.append(new_element)
                        self.new_element_nodes.clear()
                        print(new_element)
                
        

        def draw_elements(self, screen:pygame.Surface):
                """
                Draws the elements into the main screen
                """
                for element in self.element_list:
                        element.draw_element(screen)




class Element():
        def __init__(self, nodes:list[Point, Point]):
                self.nodes = nodes
                print(nodes)
        
        def __str__(self):
                node_txt = "\t".join(str(node.id) for node in self.nodes)
                return node_txt
        
        def draw_element(self, screen:pygame.Surface):
                """
                Draws the element into hte main screen
                """
                points = []
                for node in self.nodes:
                        points.append(node.position)

                pygame.draw.polygon(screen,"black",points=points,width=2)


                        # start_position = self.nodes[i].position
                        # try:
                        #         end_position = self.nodes[i+1].position
                        # except:
                        #         end_position = self.nodes[0].position
                        # pygame.draw.line(screen, "black", start_position, end_position)