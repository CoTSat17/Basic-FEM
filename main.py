import pygame
from menus import Menus, MenuSurface, Camera, PointList



class Buttons: 
        """
        Use to manage the collections of buttons
        """
        def __init__(self):
                self.buttons = []
        

        def add_button(self, position:tuple[int,int], size:tuple[int,int], menu:MenuSurface, text:str, color="white"):
                """
                Adds a new button to a surface\n
                ::INPUT::\n
                position: position relative to the surface\n
                size: size of the buttion\n
                menu: corresponding Menu\n
                text: text to show in the button
                """
                self.buttons.append(Button(position,size,menu,text,color))


        def blit_buttons(self):
                """
                Draws the button on the corresponding surface
                """
                for button in self.buttons:
                        pygame.draw.rect(button.menu,button.color,button.surf)
                        button.menu.blit(button.text_obj, button.text_position)


        def mouse_in_button(self, mouse_position:tuple[int,int]):
                """
                Checks if the mouse is in the buttons\n
                ::RETURN:: Returns true if it is and false if not, Changes the corresponding button from ".active"
                """
                for button in self.buttons:
                        button_pos = button.abs_position()
                        button_size = button.size
                        if button_pos[0] < mouse_position[0] < button_pos[0]+ button_size[0] and button_pos[1] < mouse_position[1] < button_pos[1]+ button_size[1]: 
                                button.active *= -1 #flips between -1 and 1 for active and inactive
                                return True
                        
                return False


class Button:
        """
        Button to show into the menus
        """
        def __init__(self, position:tuple[int,int],size:tuple[int,int] , menu:MenuSurface, text:str, color="white"):
                self.position = position
                self.size = size
                self.text = text
                self.menu = menu
                self.color = color
                self.active = -1 # -1 is inactive 1 is active
                self.state = 1

                self.surf = pygame.Rect(self.position, self.size)
                self.text_obj = letra.render(self.text, True, "White")
                self.text_position = ((self.size[0] - self.text_obj.get_width())/2 + self.position[0],
                                      (self.size[1] - self.text_obj.get_height())/2 + self.position[1],) # Auto centers the text

        def abs_position(self):
                """
                Returns the position coordinates in relation with the screen and not the parent surface
                """
                menu_coord = self.menu.position
                abs_coord = (menu_coord[0]+self.position[0], menu_coord[1]+self.position[1])
                return abs_coord




pygame.init()
screen_x = 1280
screen_y = 720

screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True
background_color = "black"


camera = Camera((screen_x/2, screen_y/2))
point_list = PointList(camera)

#FONT Definition
text_size = 20
letra = pygame.font.SysFont("arial",text_size)


# MENU Definition
menus = Menus(screen=screen)
menu_bot = menus.create_menu(100,"B", "red")
# BUTTONS Definition
buttons = Buttons()
buttons.add_button((10,10), (50,50), menu_bot, "test", "green")


while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                
                if event.type == pygame.MOUSEWHEEL: #Camera zoom updating
                        if event.y >0:
                                camera.zoom *= 1.1
                        else:
                                camera.zoom *= 0.9

                if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        if event.button == 2: #Checks if the button has been clicked it this frame
                                camera.previous_mouse_pos = mouse_position
                        if event.button == 1:
                                if not menus.mouse_in_menu(mouse_position):  #True if left clicked outside the menu
                                        point_list.add_point(mouse_position)
                                if buttons.mouse_in_button(mouse_position):
                                        pass


        screen.fill(background_color)



        camera.update_position(pygame.mouse.get_pressed()[1],pygame.mouse.get_pos()) #Changes the camera position when clicked

        point_list.draw_points(screen) #Draws the points in the screen



        # MENU SURFACES
        menus.change_sufaces(pygame.mouse.get_pos(), event)
        buttons.blit_buttons() # Draws the buttons of the surface
        menus.blit_surfaces(screen=screen)


        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(60)  

pygame.quit()