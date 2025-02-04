import math
import random
import pygame



## initialize pygame
pygame.init()
## change title
pygame.display.set_caption("Minesweeper")


###################### CONSTANTS ##########################
X_BORDER = 50
Y_BORDER = 50
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
##GAME
FPS = 60
TIMER_FONT = pygame.font.SysFont('Impact', 30)
BTN_FONT = pygame.font.SysFont('Arial', 15)
##BUTTON PHOTO
RST_PHOTO_WIDTH = 38
RST_PHOTO_HEIGHT = 36
#RESET BUTTON
RESET_BTN_Y = 4
RESET_BTN_WIDTH = 55
RESET_BTN_HEIGHT = 42
RESET_BTN_BORDER = 8
RESET_BTN_X = SCREEN_WIDTH / 2 - RESET_BTN_WIDTH / 2
## BLACK BOX (CORNER)
BLACK_BOX_WIDTH = 70
BLACK_BOX_HEIGHT = 35
BLACK_BOX_X_1 = SCREEN_WIDTH - BLACK_BOX_WIDTH- X_BORDER
BLACK_BOX_X_2 = X_BORDER
BLACK_BOX_Y = Y_BORDER // 2 - BLACK_BOX_HEIGHT // 2
BLACK_BOX_RADIUS = 5
## DIFFICULTY_BTN
DIF_BTN_WIDTH = 60
DIF_BTN_HEIGHT = 30
DIF_BTN_X = X_BORDER
DIF_BTN_RADIUS = 3
## CLOSE BTN
CLOSE_BTN_WIDTH = 20

####### COLORS ########
# RGB values for colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (150, 150, 150)
LIGHTER_GREY = (200, 200, 200)
DARK_GREY = (100,100,100)

## background
metal = pygame.image.load("assets/metal.png")
metal_bg = pygame.transform.scale(metal, (SCREEN_WIDTH, SCREEN_HEIGHT))
background = metal_bg


image_files = {
            "bomb": "assets/bomb.png",
            "flag": "assets/flag.png",
            "num1": "assets/num1.png",
            "num2": "assets/num2.png",
            "num3": "assets/num3.png",
            "num4": "assets/num4.png",
            "num5": "assets/num5.png",
            "num6": "assets/num6.png",
            "num7": "assets/num7.png",
            "num8": "assets/num8.png",
            "redX": "assets/redX.png",
            "dead_emoji": "assets/dead_emoji.png",
            "alive_emoji": "assets/alive_emoji.png",
            "win": "assets/win.png",
        }

def oldIsMoreThanNew(oldTime, newTime):
    def to_minutes(time_str):
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    old_minutes = to_minutes(oldTime)
    new_minutes = to_minutes(newTime)

    return old_minutes > new_minutes

## tiles CLASS
class Tile(): 
    def __init__(self, x, y, width, images):
        self.x = x
        self.y = y
        self.width = width 
        self.hiding = "nothing" # string value of what is under
        self.revealed = False # starts at false
        self.flagged = False
        self.lost = False
        self.redX = False
        self.images = images
    
    def draw(self, game_lost):
            if self.lost:
                pygame.draw.rect(SCREEN, RED, (self.x, self.y, self.width,self.width))
            else:
                pygame.draw.rect(SCREEN, LIGHT_GREY, (self.x, self.y, self.width,self.width))
            if not self.revealed:
                pygame.draw.rect(SCREEN, DARK_GREY, (self.x+0.5, self.y+0.5, self.width-1,self.width-1))
                if self.flagged:
                    self.images["flag"]["rect"].topleft= (self.x, self.y)
                    SCREEN.blit(self.images["flag"]["image"], self.images["flag"]["rect"])
            else:
                if self.hiding == "bomb":
                    self.images["bomb"]["rect"].topleft = (self.x, self.y)  # Position the image at (100, 100)
                    SCREEN.blit(self.images["bomb"]["image"], self.images["bomb"]["rect"])  # Draw the image
                    if self.flagged and game_lost:
                        self.images["redX"]["rect"].topleft = (self.x, self.y)
                        SCREEN.blit(self.images["redX"]["image"], self.images["redX"]["rect"])
                # Create a mapping of "hiding" values to the corresponding image and rect variables
                else:
                    images = {
                        "1": (self.images["num1"]["image"], self.images["num1"]["rect"]),
                        "2": (self.images["num2"]["image"], self.images["num2"]["rect"]),
                        "3": (self.images["num3"]["image"], self.images["num3"]["rect"]),
                        "4": (self.images["num4"]["image"], self.images["num4"]["rect"]),
                        "5": (self.images["num5"]["image"], self.images["num5"]["rect"]),
                        "6": (self.images["num6"]["image"], self.images["num6"]["rect"]),
                        "7": (self.images["num7"]["image"], self.images["num7"]["rect"]),
                        "8": (self.images["num8"]["image"], self.images["num8"]["rect"]),
                    }                        
                    # Check if self.hiding exists in the mapping
                    if self.hiding in images:
                        image, rect = images[self.hiding]
                        rect.topleft = (self.x, self.y)  # Position the image
                        SCREEN.blit(image, rect)  # Draw the image

class GameState():
    def __init__  (self, difficulty):
        self.difficulty = difficulty
        self.updateSettings()

        self.images = load_and_scale_images(image_files, (self.TILE_WIDTH, self.TILE_WIDTH), (38, 36))
        ## when making tiles and tiles and buttons give them each images

        ## gameState properties
        self.buttons = []
        self.tiles = []
        self.gameOn = True ## always true unless user quits
        self.running = True ## true while in single game
        self.first = True
        self.game_over = False
        self.game_lost = False
        self.game_won = False
        self.background_image = pygame.image.load("assets/metal.png")
        self.showEnd = True

        ## Time
        self.elapsed_seconds = 0
        self.clock = pygame.time.Clock()
        self.filename = "highscores.txt"


        ##### NEW  ######
        self.board = [] ## Board will be a 2D array to store the rows of the board
        ## This will make it easier for the AI to get around with actions and cords
        ## Such as left, right, up, and down
    
    def check_board_touched(self):
        return any(tile.revealed == True for tile in self.tiles)
    

    def find_neighbours(self, tile):
        print(tile.x)



    def ai_solve(self):
        if not self.check_board_touched(): ## if the player has not made the first move
            print("not touched")
            tile = self.board[len(self.board[0])// 2][len(self.board)//2]
            game_state.first_click(tile)
            game_state.place_nums()
            game_state.first = False
            game_state.reveal_around(tile)
            tile.revealed = True

        solving = True
        while solving:
            start_board = self.tiles

            for tile in self.tiles:

                if tile.revealed and tile.hiding != "bomb" or tile.hiding != "nothing":
                    # num = tile.hiding

                    self.find_neighbours(tile)
            
            if start_board == self.tiles:
                break
                

            ## 1) Visit a revealed tile
            ## 2) Add that tile to a array
            ## 3)


            
        

    def game_over_actions(self, won):
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        if seconds < 10:
            seconds = str(0)+ str(seconds)
        
        time = str(minutes) + ":" + str(seconds)
        
        if self.difficulty == "Easy":
            index = 0
        elif self.difficulty == "Medium":
            index = 1
        else:
            index = 2
        with open(self.filename, "r") as file:
            lines = file.readlines()
            highscore = lines[index]
            highscoreStrip = highscore.strip()
            

            if won:
                
                if oldIsMoreThanNew(highscoreStrip, time):
                    lines[index]=time+"\n"
                


                with open(self.filename, "w") as file:
                    file.writelines(lines)

    
                self.images["win"]["rect"].topleft= (SCREEN_WIDTH / 2 - 19, SCREEN_HEIGHT / 3)
                SCREEN.blit(self.images["win"]["image"], self.images["win"]["rect"])
                high_score_txt = TIMER_FONT.render("Highscore: " + str(highscoreStrip), True, (0, 255, 0)) 
                userTime = TIMER_FONT.render(str(time), True, (0, 255, 0)) 

            else:
                self.images["dead_emoji"]["rect"].topleft= (SCREEN_WIDTH / 2 - 19, SCREEN_HEIGHT / 3)
                SCREEN.blit(self.images["dead_emoji"]["image"], self.images["dead_emoji"]["rect"])
                high_score_txt = TIMER_FONT.render("Highscore: " + str(highscoreStrip), True, BLACK) 
                userTime = TIMER_FONT.render(str(time), True, RED) 



        
        
        
        SCREEN.blit(high_score_txt,(SCREEN_WIDTH / 2 - high_score_txt.get_width() // 2, (SCREEN_HEIGHT / 4) - high_score_txt.get_height() // 2))

        SCREEN.blit(userTime,(SCREEN_WIDTH / 2 - userTime.get_width() // 2, SCREEN_HEIGHT / 6 - userTime.get_height() // 2))

        
    def drawTiles(self):
        for tile in self.tiles:
            tile.draw(self.game_lost)
    def updateSettings(self):
        if self.difficulty == "Easy":
            self.TILE_WIDTH = 50
            self.TILE_X_NUM = 10
            self.TILE_Y_NUM = 13
            self.BOMB_NUM = 20
        elif self.difficulty == "Medium":
            self.TILE_WIDTH = 25
            self.TILE_X_NUM = 20
            self.TILE_Y_NUM = 25
            self.BOMB_NUM = 50
        else:
            self.TILE_WIDTH = 20
            self.TILE_X_NUM = 25
            self.TILE_Y_NUM = 30
            self.BOMB_NUM = 110

    def makeTiles(self):
        x = X_BORDER
        y = Y_BORDER

        for i in range(self.TILE_Y_NUM):
            row = []
            for j in range(self.TILE_X_NUM):
                tile = Tile(x, y, self.TILE_WIDTH, self.images)
                self.tiles.append(tile)
                row.append(tile)
                
                x += self.TILE_WIDTH
            self.board.append(row)
            x = X_BORDER
            y += self.TILE_WIDTH

    ## show all the bombs (used when game lost)
    def reveal_all_bombs(self):
        for tile in self.tiles:
            if tile.hiding == "bomb":
                tile.revealed = True

    ## check for win, lose, or none
    def checkWin(self):
        for tile in self.tiles:
            if tile.hiding != "bomb" and tile.revealed == False:
                return False
        return "Won"

    # place numbers
    def place_nums(self):
        for tile in self.tiles:
            if tile.hiding == "bomb":
                x = self.tiles.index(tile)
                # Get the row and column of the current tile
                row = x // self.TILE_X_NUM
                col = x % self.TILE_X_NUM

                # Check neighbors dynamically (CHATGPT)
                for dx, dy in [
                    (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
                    (0, -1),          (0, 1),    # Left,       Right
                    (1, -1), (1, 0), (1, 1)     # Bottom-left, Bottom, Bottom-right
                ]:
                    neighbor_row = row + dx
                    neighbor_col = col + dy

                    # Ensure the neighbor is within bounds
                    if 0 <= neighbor_row < self.TILE_Y_NUM and 0 <= neighbor_col < self.TILE_X_NUM:
                        neighbor_index = neighbor_row * self.TILE_X_NUM + neighbor_col
                        neighbor_tile = self.tiles[neighbor_index]

                        # if its not a bomb -> if it nothing -> 1 else += 1
                        if neighbor_tile.hiding != "bomb":
                            if neighbor_tile.hiding == "nothing":
                                neighbor_tile.hiding = "1"
                            else:
                                neighbor_tile.hiding = str(int(neighbor_tile.hiding) + 1)

    def first_click(self, tile):
        # Determine the one-tile radius around the clicked tile
        restricted_positions = set()
        for dx, dy in [ # learn what this is 
            (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
            (0, -1),          (0, 1),    # Left,       Right
            (1, -1), (1, 0), (1, 1),     # Bottom-left, Bottom, Bottom-right
            (0, 0)                       # The clicked tile itself
        ]:
            neighbor_x = tile.x + dx * self.TILE_WIDTH
            neighbor_y = tile.y + dy * self.TILE_WIDTH
            for i, sq in enumerate(self.tiles): ## ????
                if sq.x == neighbor_x and sq.y == neighbor_y:
                    restricted_positions.add(i)

        # place correct amount of bombs till max without 1 tile radius
        bombs_placed = 0
        while bombs_placed < self.BOMB_NUM:
            rand_num = random.randint(0, len(self.tiles) - 1)
            if rand_num not in restricted_positions and self.tiles[rand_num].hiding != "bomb":
                self.tiles[rand_num].hiding = "bomb"
                bombs_placed += 1

    ## reveal all bombs (When player loses)
    def reveal_bombs(self): 
        for tile in self.tiles:
            if tile.hiding == "bomb":
                tile.revealed = True

    def draw_timer(self):
        over_max = 999
        if self.elapsed_seconds >= over_max:
            self.elapsed_seconds == over_max
        text = TIMER_FONT.render(str(self.elapsed_seconds), True, RED)  # Red NUM
        SCREEN.blit(text, (X_BORDER + (self.TILE_WIDTH * self.TILE_X_NUM) - (BLACK_BOX_WIDTH/2) - text.get_width() // 2, (Y_BORDER / 2) - text.get_height() // 2))
        ## Change 513 to reliable variable

    def find_flags_placed(self):
        num_flagged = 0
        for tile in self.tiles:
            if tile.flagged and not tile.revealed:
                num_flagged+=1
        return num_flagged
    
    def find_bombs_w_flags(self):
        num_flag_bomb = 0
        for tile in self.tiles:
            if tile.flagged and tile.hiding == "bomb":
                num_flag_bomb+=1
        return num_flag_bomb
    
    ## writes the number of bombs left based on flags
    def write_bombs_left(self):
        flags_placed = self.find_flags_placed()
        text = TIMER_FONT.render(str(self.BOMB_NUM-flags_placed), True, RED)  # White text
        SCREEN.blit(text, (X_BORDER + (BLACK_BOX_WIDTH /2)- text.get_width() // 2, (Y_BORDER/2) - text.get_height() // 2))
        ## change random variables
        
    def reveal_around(self, tile):
        # Find the index of the tile in the list
        x = self.tiles.index(tile)
        
        # Stop if the tile is already revealed or a bomb
        if self.tiles[x].revealed or self.tiles[x].hiding == "bomb":
            return
        
        # Reveal the tile
        self.tiles[x].revealed = True

        # Only continue recursion if the tile is empty
        if self.tiles[x].hiding != "nothing":
            return
        
        # Check neighbors dynamically
        for dx, dy in [
            (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
            (0, -1),          (0, 1),    # Left,       Right
            (1, -1), (1, 0), (1, 1)     # Bottom-left, Bottom, Bottom-right
        ]:
            neighbor_x = self.tiles[x].x + dx * self.TILE_WIDTH
            neighbor_y = self.tiles[x].y + dy * self.TILE_WIDTH
            
            # Find the neighbor tile
            for neighbor in self.tiles:
                if neighbor.x == neighbor_x and neighbor.y == neighbor_y:
                    self.reveal_around(neighbor)  # Recursive call
                    break

    
    def draw_background(self):
        background = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        SCREEN.blit(background, (0, 0))




# Function to load, scale, and retrieve rects
def load_and_scale_images(image_files, tile_size, emoji_size):
    images = {}
    for key, path in image_files.items():
        image = pygame.image.load(path)
        # Scale differently based on type
        size = emoji_size if "emoji" in key or key == "win" else tile_size
        images[key] = {
            "image": pygame.transform.scale(image, size),
            "rect": pygame.transform.scale(image, size).get_rect()
        }
    return images

## button CLASS
class Button():
    def __init__(self, x, y, width, height, corner_curv, bg_color, hover_bg_color, image, image_rect, text):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        self.image = image
        self.image_rect = image_rect
        self.text = text
        self.corner_curv = corner_curv
    
    def draw_btn(self):
        # Change color if hovered
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(SCREEN, self.hover_bg_color, self.rect, 0, self.corner_curv)
        else:
            pygame.draw.rect(SCREEN, self.bg_color, self.rect, 0, self.corner_curv)

        if self.image == None:
            text_surface = BTN_FONT.render(self.text, True, LIGHTER_GREY)
            text_rect = text_surface.get_rect(center=self.rect.center)
            SCREEN.blit(text_surface, text_rect)
        else:
            self.image_rect.topleft = ( ## this centers it in the middle of the rectangle
    self.rect[0] + (self.rect[2] - self.image_rect.width) // 2,  # x-coordinate
    self.rect[1] + (self.rect[3] - self.image_rect.height) // 2  # y-coordinate
)
            SCREEN.blit(self.image, self.image_rect)
        







difficulty = "Easy"

game_on = True
start_ticks = 0
while game_on:
    
    game_state = GameState(difficulty)
    game_state.makeTiles()
    

    ## make reset buttons
    alive_button = Button(RESET_BTN_X, RESET_BTN_Y, RESET_BTN_WIDTH,RESET_BTN_HEIGHT, RESET_BTN_BORDER, DARK_GREY, RED, game_state.images["alive_emoji"]["image"], game_state.images["alive_emoji"]["rect"], None)
    dead_button = Button(RESET_BTN_X, RESET_BTN_Y, RESET_BTN_WIDTH,RESET_BTN_HEIGHT, RESET_BTN_BORDER, DARK_GREY, RED, game_state.images["dead_emoji"]["image"], game_state.images["dead_emoji"]["rect"], None)
    win_button = Button(RESET_BTN_X, RESET_BTN_Y, RESET_BTN_WIDTH,RESET_BTN_HEIGHT, RESET_BTN_BORDER, DARK_GREY, RED, game_state.images["win"]["image"], game_state.images["win"]["rect"], None)

    END_SCREEN_X = X_BORDER + (game_state.TILE_X_NUM * game_state.TILE_WIDTH)/9
    END_SCREEN_Y = Y_BORDER + (game_state.TILE_X_NUM * game_state.TILE_WIDTH)/9
    END_SCREEN_WIDTH = 4*(game_state.TILE_X_NUM * game_state.TILE_WIDTH)/5
    END_SCREEN_HEIGHT = 4*(game_state.TILE_Y_NUM * game_state.TILE_WIDTH)/10
    
    DIF_BTN_Y = Y_BORDER + (game_state.TILE_WIDTH * game_state.TILE_Y_NUM) +10

    ## make change difficulty buttons
    easy_btn = Button(DIF_BTN_X, DIF_BTN_Y, DIF_BTN_WIDTH, DIF_BTN_HEIGHT, DIF_BTN_RADIUS, DARK_GREY, LIGHT_GREY, None, None, "Easy")
    game_state.buttons.append(easy_btn)
    medium_btn = Button(DIF_BTN_X + 20 + DIF_BTN_WIDTH, DIF_BTN_Y, DIF_BTN_WIDTH, DIF_BTN_HEIGHT, DIF_BTN_RADIUS, DARK_GREY, LIGHT_GREY, None, None, "Medium")
    game_state.buttons.append(medium_btn)
    hard_btn = Button(DIF_BTN_X + 40 + (2*DIF_BTN_WIDTH), DIF_BTN_Y, DIF_BTN_WIDTH, DIF_BTN_HEIGHT, DIF_BTN_RADIUS, DARK_GREY, LIGHT_GREY, None, None, "Hard")
    game_state.buttons.append(hard_btn)

    close_btn = Button(END_SCREEN_X+ END_SCREEN_WIDTH - CLOSE_BTN_WIDTH-2, END_SCREEN_Y+2, CLOSE_BTN_WIDTH, CLOSE_BTN_WIDTH, 4, RED, LIGHT_GREY, None, None, "X")
    game_state.buttons.append(close_btn)

    game_state.write_bombs_left() ## should be total bombs
    while game_state.running:
        
        if game_state.game_lost:
            game_state.reveal_all_bombs()
        elif not game_state.game_over and not game_state.first:
            game_state.elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.running = False
                game_on = False

            # Check for key presses
            if not game_state.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        mouse_pos = pygame.mouse.get_pos()
                        for tile in game_state.tiles:
                            if tile.x < mouse_pos[0] and tile.x + game_state.TILE_WIDTH> mouse_pos[0] and tile.y < mouse_pos[1] and tile.y + game_state.TILE_WIDTH> mouse_pos[1]:
                                if tile.flagged == False:
                                    tile.flagged = True
                                else: 
                                    tile.flagged=False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if mouse_pos[0] > 550 and mouse_pos[1] > 750 and not game_state.game_over:
                    ## if the player clicks the bottom right and the game is not over
                    game_state.ai_solve()

                for button in game_state.buttons:
                    if button.x < mouse_pos[0] and button.x + DIF_BTN_WIDTH> mouse_pos[0] and button.y < mouse_pos[1] and button.y + DIF_BTN_HEIGHT> mouse_pos[1]:
                        if game_state.game_over:
                            if button.text == "X":
                                game_state.showEnd = False
                        if button.text != "X":
                            difficulty = button.text
                            game_state.running = False
                        

                if mouse_pos[0] > RESET_BTN_X and mouse_pos[1] > RESET_BTN_Y and mouse_pos[0] < (RESET_BTN_X+RESET_BTN_WIDTH) and mouse_pos[1] < (RESET_BTN_Y+RESET_BTN_HEIGHT):
                    game_state.running = False
        
                if not game_state.game_over:
                    if event.button == 3:
                        ## flag tile
                        for tile in game_state.tiles:
                            if tile.x < mouse_pos[0] and tile.x + game_state.TILE_WIDTH> mouse_pos[0] and tile.y < mouse_pos[1] and tile.y + game_state.TILE_WIDTH> mouse_pos[1]:
                                if tile.flagged == False:
                                    tile.flagged = True
                                else: 
                                    tile.flagged=False
                    else:
                        for tile in game_state.tiles:
                            if tile.x < mouse_pos[0] and tile.x + game_state.TILE_WIDTH> mouse_pos[0] and tile.y < mouse_pos[1] and tile.y + game_state.TILE_WIDTH> mouse_pos[1]:
                                if not tile.flagged:
                                    if game_state.first:
                                        start_ticks = pygame.time.get_ticks()
                                        game_state.first_click(tile)
                                        game_state.place_nums()
                                        game_state.first = False
                                    if tile.hiding == "bomb": ## if you uncover a bomb / lose
                                        tile.lost = True
                                        game_state.game_over = True
                                        game_state.game_lost = True
                                    game_state.reveal_around(tile)
                                    tile.revealed = True
                    

        
        ## draw background
        SCREEN.blit(background, (0, 0))
        ## timer words
        pygame.draw.rect(SCREEN, BLACK, (BLACK_BOX_X_1, BLACK_BOX_Y, BLACK_BOX_WIDTH, BLACK_BOX_HEIGHT), 0, BLACK_BOX_RADIUS)
        pygame.draw.rect(SCREEN, BLACK, (BLACK_BOX_X_2, BLACK_BOX_Y, BLACK_BOX_WIDTH, BLACK_BOX_HEIGHT), 0, BLACK_BOX_RADIUS)

        game_state.draw_timer()

        flags_placed = game_state.find_flags_placed()

        bombs_w_flags = game_state.find_bombs_w_flags()


        if game_state.checkWin():
            game_state.game_over = True
            game_state.game_won = True

        game_state.drawTiles()

        easy_btn.draw_btn()
        medium_btn.draw_btn()
        hard_btn.draw_btn()



        if game_state.game_over: 
            if game_state.showEnd:
                pygame.draw.rect(SCREEN, LIGHTER_GREY, (END_SCREEN_X, END_SCREEN_Y, END_SCREEN_WIDTH, END_SCREEN_HEIGHT))
                close_btn.draw_btn()
                game_state.game_over_actions(game_state.game_won)
            # Display bombs with flags since the game is over
            game_state.write_bombs_left()
            if game_state.game_won:
                # Game over and player won
                win_button.draw_btn()
            elif game_state.game_lost:
                # Game over and player lost
                dead_button.draw_btn()
        else:
            # Game is not over, display flags placed
            game_state.write_bombs_left()
            # Show alive button
            alive_button.draw_btn()

        pygame.display.update()
        game_state.clock.tick(FPS)
pygame.quit()