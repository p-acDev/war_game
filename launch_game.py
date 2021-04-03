import pygame
import json
import os
from key_corresp import KEYS

class Player:
    
    def __init__(self, player_profile):
        
        with open(player_profile, "r") as f:
            profile = json.load(f)
        
        self.player_image = pygame.image.load(os.path.join('assets',
                                                           profile["player_picture"]))
        self.player_image = pygame.transform.scale(self.player_image,(profile["width"],
                                                                      profile["height"]))
        
        self.name = profile["playerName"]
        
        self.width = profile["width"]
        self.height = profile["height"]
        
        self.initialX = profile["initialX"] - self.width / 2
        self.initialY = profile["initialY"] - self.height / 2
        
        self.x = self.initialX
        self.y = self.initialY
        
        self.keyUp = profile["keyUp"]
        self.keyDown = profile["keyDown"]

    def move_player(self, keys_pressed, min_y, max_y):
        
        if (keys_pressed[KEYS[self.keyUp]]) and (self.y > min_y): # UP
            self.y -= 1
        elif (keys_pressed[KEYS[self.keyDown]]) and (self.y < max_y): # down
            self.y += 1
        
        return None

class WarGameUI:
    
    def __init__(self, config_file, color_data, player_profiles):
        
        # import the input data
        with open(config_file, "r") as f:
            self.CONFIG = json.load(f)
        with open(color_data, "r") as f:
            self.COLORS = json.load(f)

        # setup initial windows
        self.WIN = pygame.display.set_mode((self.CONFIG["windowSettings"]["WIDTH"],
                                            self.CONFIG["windowSettings"]["HEIGHT"]))
        pygame.display.set_caption(self.CONFIG["appName"])
 
        # initialize players
        self.players = []
        for profile in player_profiles:
            self.players.append(Player(profile))

    def __repr__(self):
        return self.CONFIG["appName"]

    def draw_window(self):
        
        self.WIN.fill(tuple(self.COLORS["WHITE"]))
        
        # draw player at initial pos
        for player in self.players:
            self.WIN.blit(player.player_image, (player.x,
                                                player.y))
            
        # update and refresh the app to draw everything        
        pygame.display.update()

        return None

    def main_loop(self):
        
        # control the while loop frame rate
        clock = pygame.time.Clock()
        
        run = True
        
        while run:
            # limit the while loop clock to the one in config
            clock.tick(self.CONFIG["FPS"])
            # catch all event in the app
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            keys_pressed = pygame.key.get_pressed()
            
            #left player
            self.players[0].move_player(keys_pressed,
                                        0,
                                        self.CONFIG["windowSettings"]["HEIGHT"] - self.players[0].height)
            
            # right player
            self.players[1].move_player(keys_pressed,
                                        0,
                                        self.CONFIG["windowSettings"]["HEIGHT"] - self.players[1].height)            

            # will refresh and draw the app at clock FPS    
            self.draw_window()

        pygame.quit()
        
          
    
if __name__ == "__main__":
    
    config_file = "./config.json"
    color_data = "./color_data.json"
    
    player_profile_files = ["./playerLeft.json", "./playerRight.json"]
    
    app = WarGameUI(config_file, color_data, player_profile_files)
    app.main_loop()