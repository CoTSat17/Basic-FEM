import pygame
from menus import Menus, PointList
from camera import Camera
from buttons import Buttons

def mousedown_events(event):
        mouse_position = pygame.mouse.get_pos()
        if event.button == 2: #Checks Mid Button
                camera.previous_mouse_pos = mouse_position
        if event.button == 1: #Checks Left Button
                if not menus.mouse_in_menu(mouse_position) and button_add_nodes.active == 1: #If corresponding button is active
                        point_list.add_point(mouse_position) #Ads a node
                else:
                        buttons.mouse_in_button(mouse_position) #Checks if a button was clicked





pygame.init()
screen_x = 1280
screen_y = 720

screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True
background_color = "white"


camera = Camera((screen_x/2, screen_y/2))

#POINTS Definition
point_list = PointList(camera)

#FONT Definition
text_size = 20
letra = pygame.font.SysFont("arial",text_size)


# MENU Definition
menus = Menus(screen=screen)
menu_bot = menus.create_menu(100,"B", "gray")


# BUTTONS Definition
buttons = Buttons(letra)
button_add_nodes = buttons.add_button((10,10), (100,25), menu_bot, "Add Nodes")


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
                        mousedown_events(event=event)


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