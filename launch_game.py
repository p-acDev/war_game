import pygame
import json
import os

class Player:
    
    def __init__(self, player_profile):
        
        with open(player_profile, "r") as f:
            profile = json.load(f)
        
        self.player_image = pygame.image.load(os.path.join('assets',
                                                           profile["player_picture"]))
        self.player_image = pygame.transform.scale(self.player_image,(profile["width"],
                                                                      profile["height"]))
        
        
        self.playerInitialX = profile["initialX"] - profile["width"] / 2
        self.playerInitialY = profile["initialY"] - profile["height"] / 2

        
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
        self.WIN.fill(tuple(self.COLORS["WHITE"]))
        
        
        # initialize players
        self.players = []
        for profile in player_profiles:
            self.players.append(Player(profile))

    def __repr__(self):
        return self.CONFIG["appName"]

    def draw_window(self):
        
        # draw player at initial pos
        for player in self.players:
            self.WIN.blit(player.player_image, (player.playerInitialX,
                                                player.playerInitialY))
        
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
            
            # will refresh and draw the app at clock FPS    
            self.draw_window()

        pygame.quit()    
    
if __name__ == "__main__":
    
    config_file = "./config.json"
    color_data = "./color_data.json"
    
    player_profile_files = ["./playerLeft.json", "./playerRight.json"]
    
    app = WarGameUI(config_file, color_data, player_profile_files)
    app.main_loop()