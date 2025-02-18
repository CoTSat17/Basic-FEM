import pygame

# Cursores
cursor_vertical_size = pygame.SYSTEM_CURSOR_SIZENS
cursor_standard = pygame.SYSTEM_CURSOR_ARROW

class Menus():
        def __init__(self, screen:pygame.Surface):
                self.screen_x = screen.get_width()
                self.screen_y = screen.get_height()
                self.menus=[]
        

        def create_menu(self, size, orientation, color:str)->"MenuSurface":
                menu_surface = MenuSurface(size, orientation, self.screen_x, self.screen_y, color)
                self.menus.append(menu_surface)
                return menu_surface


        def blit_surfaces(self, screen:pygame.Surface):
                for surf in self.menus:
                        surf.blit_surface(screen)
        
        def check_active_edges(self, mouse_position: tuple, event):
                """
                Checks if the mouse is over an active edge of a surface.
                """
                if pygame.mouse.get_pressed()[0] == False: #If mouse is no longer pressed, return to normal
                        for surf in self.menus:
                                surf.active = False
                                pygame.mouse.set_cursor(cursor_standard)
                        return None

                if event.type != pygame.MOUSEBUTTONDOWN: # If the mouse wasn't clicked in this frame returns none and stops the function
                        return None

                margin = 10
                for surf in self.menus: 
                        for i,coord in enumerate(mouse_position): #checks X and then Y.
                                if coord - margin < surf.active_edge[i] < coord + margin and surf.active_edge[i] != 0:
                                        surf.active = True
                                        pygame.mouse.set_cursor(cursor_vertical_size)
                        


        def update_surfaces(self, mouse_position:tuple):
                """
                Changes the size of the surfaces based on mouse input if "check_active_edges()" set surf.active = True
                """

                for surf in self.menus:
                        if surf.active: # True when it can be moved
                                new_height = {  "T": mouse_position[1],
                                                "B": self.screen_y - mouse_position[1],
                                                "R": self.screen_x - mouse_position[0], 
                                                "L": mouse_position[0]}
                                surf.height = new_height[surf.orientation]
                                surf.update_position(self.screen_x, self.screen_y)


        def change_sufaces(self, mouse_position:tuple, event:pygame.event):
                """
                Checks if the mouse is in top of a active surface\n
                Updates the surface following the mouse
                """
                self.check_active_edges(mouse_position, event)
                self.update_surfaces(mouse_position)


        def mouse_in_menu(self, mouse_position:tuple):
                """
                Checks if the mouse is in top of a menu sufrace, gives a margin of 20 px \n
                ::RETURN:: Retutns True if its in top of a menu
                """
                for menu in self.menus:
                        conditions = {"T": mouse_position[1] < menu.height + 20,
                                      "B": mouse_position[1] > menu.position[1] - 20,
                                      "R": mouse_position[0] > menu.position[0] - 20,
                                      "L": mouse_position[0] < menu.height + 20 } # Set of conditions depending on the orientation
                        condition = conditions[menu.orientation]
                        if condition:
                                return True
                
                return False


class MenuSurface(pygame.Surface):
        def __init__(self, size, orientation, screen_x, screen_y, color):
                self.length = 4000 #the big dimmension of the menu
                self.height = size # the small dimension of the menu
                self.orientation = orientation #the orientation/position of the menu
                self.active = False # True if it's currently changing size with the mouse.
                self.color = color
                self.update_position(screen_x, screen_y)

        def update_position(self, screen_x, screen_y):
                """
                Updates the position and dimensions of the surface when its changed
                """
                if self.height < 10:
                        self.height = 10

                dimmensions = { "T": (self.length, self.height),
                                "B": (self.length, self.height),
                                "L": (self.height, self.length),
                                "R": (self.height, self.length)} #Changes the dimensions tupple based on the orientation
                self.dimmensions = dimmensions[self.orientation]

                positions = {"T": (0, 0), "B": (0, screen_y - self.height), "L": (0,0) , "R": (screen_x - self.height ,0)} #Changes the position tupple based on the orientation
                self.position = positions[self.orientation]
                super().__init__(self.dimmensions) # generates a new surface with the updated dimensions
                self.fill(self.color)
                # Define the active edge (the mobile one), 0 means it's along the entire dimmension.
                active_edges = {"T": (0,self.height), "B": self.position, "L": (self.height,0), "R": self.position}
                self.active_edge = active_edges[self.orientation]


        def blit_surface(self, screen:pygame.Surface):
                screen.blit(self, self.position)











class Camera():
        def __init__(self, screen_center):
                self.zoom = 1
                self.position = [0,0]
                self.previous_mouse_pos = (0,0)
                self.screen_center = screen_center

        def update_position(self, wheelpressed:bool, mouse_pos:tuple):
                """
                Updates the camera position with the mousewheel
                """
                if wheelpressed:
                        mouse_pos = mouse_pos
                        mouse_movement = ((mouse_pos[0] - self.previous_mouse_pos[0]),
                                           (mouse_pos[1] - self.previous_mouse_pos[1]))
                        self.position = (self.position[0] - mouse_movement[0]/self.zoom,self.position[1] + mouse_movement[1]/self.zoom)
                        self.previous_mouse_pos = mouse_pos


        def to_camera_position(self, position:tuple[int,int])->tuple[int,int]:
                """
                Goes from a true positon from a camera position with the 
                """
                moved_position = (position[0] - self.position[0], position[1] + self.position[1])
                zoomed_position = ((moved_position[0]-self.screen_center[0])*self.zoom + self.screen_center[0],
                                   (self.screen_center[1] - (self.screen_center[1] - moved_position[1])*self.zoom))
                return zoomed_position
        

        def to_real_positon(self, position:tuple[int,int])->tuple[int,int]:
                """
                Goes from the camera position to the true position 
                """
                moved_position = (position[0] + self.position[0]*self.zoom, position[1] - self.position[1]*self.zoom)
                zoomed_position = ((moved_position[0]-self.screen_center[0])/self.zoom + self.screen_center[0],
                                   (self.screen_center[1] - (self.screen_center[1] - moved_position[1])/self.zoom))
                return zoomed_position









class PointList():
        def __init__(self, camera:Camera ):
                self.points = []
                self.camera = camera
        
        def add_point(self, position:tuple[int,int]):
                """
                Creates a "Point" instance and adds it to the list
                """
                self.points.append(Point(self.camera.to_real_positon(position), len(self.points)))

        def draw_points(self, screen:pygame.surface):
                for point in self.points:
                        pygame.draw.circle(screen,"black",self.camera.to_camera_position(point.position), 2)



class Point():
        def __init__(self, position:tuple[int,int], id:int):
                self.position = position
                self.id = id