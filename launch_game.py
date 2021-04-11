import pygame
import pygame_menu
import pygame.freetype
import json
import os
from key_corresp import KEYS
pygame.init()


class Player(pygame.Rect):

    def __init__(self, player_profile):

        with open(player_profile, "r") as f:
            self.profile = json.load(f)

        self.player_image = pygame.image.load(os.path.join('assets',
                                                           self.profile["player_picture"]))
        self.player_image = pygame.transform.scale(self.player_image,(self.profile["width"],
                                                                      self.profile["height"]))
        self.player_image = pygame.transform.rotate(self.player_image, self.profile["rotate"])

        self.name = self.profile["playerName"]

        self.width = self.profile["width"]
        self.height = self.profile["height"]

        self.initialX = self.profile["initialX"] - self.width / 2
        self.initialY = self.profile["initialY"] - self.height / 2

        self.velocity = self.profile["velocity"]

        self.x = self.initialX
        self.y = self.initialY

        self.keyUp = self.profile["keyUp"]
        self.keyDown = self.profile["keyDown"]

        self.bulletSpeed = self.profile["bulletSpeed"]
        self.keyFire = self.profile["keyFire"]
        self.bullets = []
        self.fireGuns = self.profile["fireGuns"]
        self.bulletWidth = self.profile["bulletWidth"]
        self.bulletHeight = self.profile["bulletHeight"]
        self.bulletColor = self.profile["bulletColor"]

        self.pv = self.profile["PV"]

        self.dead = False

    def move_player(self, keys_pressed, min_y, max_y):

        if (keys_pressed[KEYS[self.keyUp]]) and (self.y > min_y + self.velocity):  # UP
            self.y -= self.velocity
        elif (keys_pressed[KEYS[self.keyDown]]) and (self.y < max_y - self.velocity):  # down
            self.y += self.velocity

        return None

    def fire(self, keys_pressed):
        if keys_pressed[KEYS[self.keyFire]]:
            for fireGunNumber in self.fireGuns.keys():
                bullet = pygame.Rect(self.x + self.fireGuns[fireGunNumber]["xpos"],
                                     self.y + self.fireGuns[fireGunNumber]["ypos"],
                                     self.bulletWidth,
                                     self.bulletWidth)
                if len(self.bullets) <= 1:
                    self.bullets.append(bullet)

        return None

    def bullet_traj(self, x_min, x_max):
        for bullet in self.bullets:
            if self.name == "left":
                bullet.x += self.bulletSpeed

            elif self.name == "right":
                bullet.x -= self.bulletSpeed

            if (bullet.x < x_min) or (bullet.x > x_max):
                self.bullets.remove(bullet)

        return None

    def check_collision(self, other_player):

        for bullet in other_player.bullets:
            if self.colliderect(bullet):
                self.pv -= 1
                other_player.bullets.remove(bullet)

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

        # draw the remaining PV
        self.GAME_FONT = pygame.font.Font(pygame.font.get_default_font(), 36)
        
        # initialize players
        self.players = []
        for profile in player_profiles:
            self.players.append(Player(profile))

    def __repr__(self):
        return self.CONFIG["appName"]

    def draw_winner(self, player):
        
        winner_msg = self.GAME_FONT.render("The Winner is " + player.name,
                                           True,
                                           self.COLORS[player.bulletColor])
        
        self.WIN.blit(winner_msg,
                      (self.CONFIG["windowSettings"]["WIDTH"]/2 - winner_msg.get_width()/2,
                       self.CONFIG["windowSettings"]["HEIGHT"]/2 - winner_msg.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)
        
        return None

    def draw_window(self):
        
        self.WIN.fill(tuple(self.COLORS["WHITE"]))
        
        # draw players
        for player in self.players:
            
            player_info = self.GAME_FONT.render("PV: " + str(player.pv),
                                                True,
                                                self.COLORS[player.bulletColor])
            
            self.WIN.blit(player_info, (player.profile["displayPvX"],
                                        player.profile["displayPvY"]))
            self.WIN.blit(player.player_image, (player.x,
                                                player.y))
            for bullet in player.bullets:
                if bullet:
                    pygame.draw.rect(self.WIN,
                                     self.COLORS[player.bulletColor],
                                     bullet)
        
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
            
            # handle player movement and fire
            for i, player in enumerate(self.players):
                player.move_player(keys_pressed,
                                   80,  # to leave blank a line a top
                                   self.CONFIG["windowSettings"]["HEIGHT"] - self.players[0].height)
                player.fire(keys_pressed)
                player.bullet_traj(0, self.CONFIG["windowSettings"]["WIDTH"])
            
                if player.pv <= 0:
                    if i == 0:
                        winner = self.players[1]
                    else:
                        winner = self.players[0]
                    self.draw_winner(winner)
                    run = False
                
            # handle the colisions
            self.players[0].check_collision(self.players[1])
            self.players[1].check_collision(self.players[0])
            
            # will refresh and draw the app at clock FPS    
            self.draw_window()

        pygame.quit()

           
if __name__ == "__main__":

    config_file = "./config.json"
    color_data = "./color_data.json"

    player_profile_files = ["./playerLeft.json", "./playerRight.json"]

    app = WarGameUI(config_file, color_data, player_profile_files)
    app.main_loop()
