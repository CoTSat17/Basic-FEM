import pygame
from menus import Point
from elements import Elements


def delaunay_triangles(points: list[Point], element_list:Elements)->None:
        """
        Given a list of points, generates the dalaunay triangles and calls the "elemen" class to generate the elements
        """


        temp_circles = []
        nodes = points[:]
        # Get the circumcircle of the points
        for node1 in nodes:
                #Goes node by node, eliminating itself and checking conections with the other nodes
                nodes.remove(node1)
                nodes_without_node2 = nodes.copy()
                for node2 in nodes_without_node2: 
                       nodes_without_node2.remove(node2) #Eliminates the node2 until a new node1 is selected
                       for node3 in nodes_without_node2:
                                if node3 == node2:
                                        continue
                                temp_circles.append(__circle_from_3points(node1.position, node2.position, node3.position))


        # Delete the circles with another point inside, for the other saves the points that form it.
        points_of_element = []
        for circle in temp_circles:
                point_inside = False
                circle_center_x = circle[0][0]
                circle_center_y = circle[0][1]
                circle_radius = round(circle[1],2)
                points_in_border = [] # list of points that are in the perimeter of the circle

                for point in points:
                        #For each circle checks each point
                        distance_to_center = round(((circle_center_x - point.position[0])**2 + (circle_center_y - point.position[1])**2 )**(1/2), 2)
                        if distance_to_center < circle_radius:
                                point_inside = True
                                break #If a point is inside the circle breaks to check the next circle
                        elif distance_to_center == circle_radius:
                                points_in_border.append(point)
                

                if not point_inside: #If a break in the previous loop was not done
                        points_of_element.append(points_in_border)

        
        element_list.add_dalaunay_element(points_of_element)








# def draw_triangle(screen:pygame.surface, triangles_list:list[list[tuple[float,float],float]]):
#         """
#         Given a list of delaunay triangles draws the triangles on the screen
#         """
#         if len(triangles_list) == 0:
#                 return None
#         for triangle in triangles_list:
#                 pygame.draw.circle(screen, "black", triangle[0], triangle[1],2)



def __circle_from_3points(point_1:tuple[int,int], point_2:tuple[int,int], point_3:tuple[int,int]):
        """
        Gets the center and radius of a circle form 3 points
        """
        vec_1 = (point_2[0] - point_1[0], point_2[1] - point_1[1])
        vec_2 = (point_3[0] - point_1[0], point_3[1] - point_1[1])

        mp_1 = (point_1[0] + vec_1[0]/2, point_1[1] + vec_1[1]/2) #Midpoint of vector 1
        mp_2 = (point_1[0] + vec_2[0]/2, point_1[1] + vec_2[1]/2) #Midpoint of vector 2

        normal_1 = (1, -vec_1[0]/vec_1[1])
        normal_2 = (1, -vec_2[0]/vec_2[1])

        l2 = (mp_1[1] + normal_1[1]*(mp_2[0] / normal_1[0] - mp_1[0]) - mp_2[1] ) / ( normal_2[1] - normal_1[1] / normal_1[0] )

        circle_center = (mp_2[0] + normal_2[0] * l2, mp_2[1] + normal_2[1] * l2) 
        circle_radius = ( (point_1[0] - circle_center[0])**2 + (point_1[1] - circle_center[1])**2 )**(1/2)    

        return circle_center, circle_radius






if __name__ == "__main__":
        if 243.41 < 222.57:
                print("A")