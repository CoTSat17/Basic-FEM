import pygame
from menus import Menus, Camera, PointList


class Buttons: 
        """
        Use to manage the collections of buttons
        """
        def __init__(self):
                self.buttons = []
        

        def add_button(self, position:tuple[int,int], size:tuple[int,int], menu:Menus, text:str, color="white"):
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
                for button in self.buttons:
                        pygame.draw.rect(button.menu,button.color,button.surf)



class Button:
        """
        Button to show into the menus
        """
        def __init__(self, position:tuple[int,int],size:tuple[int,int] , menu:Menus, text:str, color="white"):
                self.position = position
                self.size = size
                self.text = text
                self.menu = menu
                self.color = color
                self.state = 1

                self.surf = pygame.Rect(self.position, self.size)







pygame.init()
screen_x = 1280
screen_y = 720

screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True
background_color = "black"


camera = Camera((screen_x/2, screen_y/2))
point_list = PointList(camera)

letra = pygame.font.SysFont("arial",40)
user_text= ""

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
                        if event.button == 2: #Checks if the button has been clicked it this frame
                                camera.previous_mouse_pos = pygame.mouse.get_pos()
                        if event.button == 1 and not menus.mouse_in_menu(pygame.mouse.get_pos()):  
                                #Checks if the left button has been clicked taking into account the menus
                                point_list.add_point(pygame.mouse.get_pos())


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