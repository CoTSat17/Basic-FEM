from menus import Menus, MenuSurface
import pygame

class Buttons: 
        """
        Use to manage the collections of buttons
        """
        def __init__(self, letra):
                self.buttons = []
                self.letra = letra
        

        def add_button(self, position:tuple[int,int], size:tuple[int,int], menu:MenuSurface, text:str):
                """
                Adds a new button to a surface\n
                ::INPUT::\n
                position: position relative to the surface\n
                size: size of the buttion\n
                menu: corresponding Menu\n
                text: text to show in the button\n
                """
                new_button = Button(position,size,menu,text,self.letra)
                self.buttons.append(new_button)
                return new_button

        def blit_buttons(self):
                """
                Draws the button on the corresponding surface
                """
                for button in self.buttons:
                        pygame.draw.rect(button.menu,button.color,button.surf)
                        button.menu.blit(button.text_obj, button.text_position)


        def mouse_in_button(self, mouse_position:tuple[int,int]):
                """
                Checks if the mouse is in the buttons and changes "active"\n
                ::RETURN:: Returns true if it is and false if not, Changes the corresponding button from ".active"
                """
                for button in self.buttons:
                        button_pos = button.abs_position()
                        button_size = button.size
                        if button_pos[0] < mouse_position[0] < button_pos[0]+ button_size[0] and button_pos[1] < mouse_position[1] < button_pos[1]+ button_size[1]: 
                                button.change_active() #flips between -1 and 1 for active and inactive
                                return True
                        
                return False


class Button:
        """
        Button to show into the menus
        """
        def __init__(self, position:tuple[int,int],size:tuple[int,int] , menu:MenuSurface, text:str,letra:pygame.font):
                """
                Adds a new button to a surface\n
                ::INPUT::\n
                position: position relative to the surface\n
                size: size of the buttion\n
                menu: corresponding Menu\n
                text: text to show in the button
                """
                self.position = position
                self.size = size
                self.text = text
                self.menu = menu
                self.color = "dark gray"
                self.active = -1 # -1 is inactive 1 is active
                self.state = 1 # TODO 1 if its shown -1 if not
                self.surf = pygame.Rect(self.position, self.size)
                # Button text
                self.text_obj = letra.render(self.text, True, "White")
                self.text_position = ((self.size[0] - self.text_obj.get_width())/2 + self.position[0],
                                      (self.size[1] - self.text_obj.get_height())/2 + self.position[1],) # Auto centers the text

        def change_active(self):
                """
                Changes the button from active to inactive of inverse\n
                Also changes button colour
                """
                colors_by_active = {-1:"dark gray", 1: "black"}
                self.active *=-1
                self.color = colors_by_active[self.active]

        def abs_position(self):
                """
                Returns the position coordinates in relation with the screen and not the parent surface
                """
                menu_coord = self.menu.position
                abs_coord = (menu_coord[0]+self.position[0], menu_coord[1]+self.position[1])
                return abs_coord