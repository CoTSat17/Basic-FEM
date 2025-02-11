import pygame
from menus import Menus, Camera, PointList


class Button:
        def __init__(self, position:tuple[int,int], text:str, menu:Menus):
                self.position = position
                self.text = text
                self.menu = menu
                self.state = 1







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


menus = Menus(screen=screen)

menu_bot = menus.create_menu(100,"B", "red")



while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                
                if event.type == pygame.MOUSEWHEEL:
                        if event.y >0:
                                camera.zoom *= 1.1
                        else:
                                camera.zoom *= 0.9
                        print(camera.zoom)

                if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 2:
                                camera.previous_mouse_pos = pygame.mouse.get_pos()
                        if event.button == 1:
                                point_list.add_point(pygame.mouse.get_pos())




        screen.fill(background_color)

        camera.update_position(pygame.mouse.get_pressed()[1],pygame.mouse.get_pos())
        point_list.draw_points(screen)

        # MENU SURFACES
        rect = pygame.Rect((10,0),(100,100))
        pygame.draw.rect(menu_bot,"white",rect=rect)
        menus.change_sufaces(pygame.mouse.get_pos(), event)
        menus.blit_surfaces(screen=screen)

        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(60)  

pygame.quit()