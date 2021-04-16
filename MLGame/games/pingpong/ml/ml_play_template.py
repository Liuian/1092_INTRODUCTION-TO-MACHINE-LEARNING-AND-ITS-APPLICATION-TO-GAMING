"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    import random
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False    #self.ball_served記錄球被發出去了沒
        self.side = side
        self.ball_x = 0
        self.prev_ball_x = 0
        self.ball_y = 0
        self.prev_ball_y = 0
        self.des_x = 100             #75 is initial place

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        #if game pass pr game over -> reset
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            return "RESET"

        #if self.ball_served is False, serve the ball
        if not self.ball_served:    
            self.ball_served = True
            rand = self.random.randint(0, 1)
            if rand == 0:
                #print("left")
                return "serve_to_left"
                #???command = "SERVE_TO_RIGHT"
            else:
                return "serve_to_right"
                #print("right")
                #???command = "SERVE_TO_RIGHT"

        #if self.ball_serve is true, move the plate
        else:                       
            #update the parmeters
            self.prev_ball_x = self.ball_x
            self.prev_ball_y = self.ball_y
            self.ball_x = scene_info["ball"][0]
            self.ball_y = scene_info["ball"][1]
            velo_ball_x = self.ball_x - self.prev_ball_x
            velo_ball_y = self.ball_y - self.prev_ball_y

            if self.side == "1P":
                #judge the ball's x destination
                if velo_ball_y > 0:          #ball go down
                    if velo_ball_x < 0:      #ball move left
                        self.des_x = self.ball_x - (420 - self.ball_y)
                    else:                    #ball move right
                        self.des_x = self.ball_x + (420 - self.ball_y)
                else:                        #ball move up   
                    self.des_x = 100
                #adjest the destination into the scene
                while self.des_x > 200 or self.des_x < 0:
                    if self.des_x > 200:
                        self.des_x = (200 - (self.des_x - 200))
                    else:
                        self.des_x = -self.des_x
                #judge the cammand
                if scene_info["frame"] < 150:
                    return "NONE"
                #elif scene_info["platform_1P"][1] <
                elif scene_info["platform_1P"][0] + 20 < self.des_x: #plate at ball's right, plate move left
                    #print("l_r ", self.des_x, scene_info["platform_1P"][0])
                    return "MOVE_RIGHT"
                elif scene_info["platform_1P"][0] + 20 > self.des_x:
                    #print("m_r ", self.des_x, scene_info["platform_1P"][0])
                    return "MOVE_LEFT"
                else:
                    #print("n")
                    return "NONE"
                #return command
            
            #if self.side == 2P
            else:                           
                #judge the ball's x destination
                if velo_ball_y < 0:          #ball move up
                    if velo_ball_x < 0:      #ball move left
                        self.des_x = self.ball_x - (self.ball_y - 80)
                    else:                    #ball move right
                        self.des_x = self.ball_x + (self.ball_y - 80)
                else:                        #ball move down   
                    self.des_x = 100
                #adjest the destination into the scene
                while self.des_x > 200 or self.des_x < 0:
                    if self.des_x > 200:
                        self.des_x = (200 - (self.des_x - 200))
                    else:
                        self.des_x = -self.des_x
                #judge the cammand
                if scene_info["frame"] < 150:
                    return "NONE"
                #elif scene_info["platform_1P"][1] <
                elif scene_info["platform_2P"][0] + 20 < self.des_x: #plate at ball's right, plate move left
                    #print("mor ", self.des_x, scene_info["platform_2P"][0])
                    return "MOVE_RIGHT"
                elif scene_info["platform_2P"][0] + 20 > self.des_x:
                    #print("mol ", self.des_x, scene_info["platform_2P"][0])
                    return "MOVE_LEFT"
                else:
                    #print("n")
                    return "NONE"
                #return command
            
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False