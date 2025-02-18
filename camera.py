
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

