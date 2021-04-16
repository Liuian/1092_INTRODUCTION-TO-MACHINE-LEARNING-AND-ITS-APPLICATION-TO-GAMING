"""
The template of the main script of the machine learning process
"""
import random
import os.path
import pickle

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        filename = 'model.pickle'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))
        self.ball_served = False
        self.des_x = 0
        self.des_vx = 0
        self.des_vy = 0
        self.prev_ball_x = 0
        self.prev_ball_y = 0
        self.current_ball_x = 0
        self.current_ball_y = 0
        self.plat = 75
        self.plat_prev = 75

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_LEFT"
        #若遊戲開始
        else:
            if scene_info["frame"]==0 or scene_info["frame"]==1:
                self.des_x = 100
                self.current_ball_y=scene_info["ball"][1]
                self.current_ball_x=scene_info["ball"][0]
            #設好變數放進pickle檔裡面
            else:
                self.prev_ball_x = self.current_ball_x
                self.prev_ball_y = self.current_ball_y
                self.current_ball_x=scene_info["ball"][0]
                self.current_ball_y=scene_info["ball"][1]
                #self.plat_prev = self.plat
                #self.plat = scene_info["platform"][0]
                #plat_v = self.plat - self.plat_prev
                
                if self.current_ball_y>self.prev_ball_y:
                    if self.current_ball_x>self.prev_ball_x:
                        self.des_x=(400-self.current_ball_y)+self.current_ball_x	
                    else:
                        self.des_x=self.current_ball_x-(400-self.current_ball_y)

                if self.current_ball_y<self.prev_ball_y:
                    self.des_x=80
                self.prev_ball_x = scene_info["ball"][0]
                self.prev_ball_y = scene_info["ball"][1]

            while self.des_x>200 or self.des_x < 0:
                if self.des_x>200:
                    self.des_x=(200-(self.des_x-200))
                else:
                    self.des_x = -self.des_x

            self.des_vx = self.current_ball_x - self.prev_ball_x
            self.des_vy = self.current_ball_y - self.prev_ball_y

            px = scene_info["platform"][0] + 20
            ny = scene_info["ball"][1]
            nx = scene_info["ball"][0]
            
            command = self.model.predict([[nx, ny, px, self.des_vx, self.des_vy, self.des_x]])

        if command == 0: return "NONE"
        elif command == 1: return "MOVE_LEFT"
        else: return "MOVE_RIGHT"

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
