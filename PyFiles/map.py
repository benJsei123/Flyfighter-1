import random
import pygame as pg
from powerup_manager import PowerUpManager, PowerUp
from enemy_manager import EnemyManager, Enemy

class Map:
    

    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.player = game.player
        self.game_settings = game.game_settings
        self.background_surface = None
        

        #Tiles
        self.tile_blueprints = [] #holds MapTile objects
        self.visited_tiles_amount = 1
        self.visited_tiles = []
        self.tiles = []
        self.active_tile = None


        self.powerup_mgr = PowerUpManager(game=self.game,tiles=self.tiles, player=self.player) #TODO the tile should be filled or updated at some point!!
        self.enemy_mgr = EnemyManager()

        self.initialize_map()
    

    def initialize_map(self):
        self.gen_background()
        self.gen_initial_map()
        self.create_tile_blueprints()
        for tile in self.tile_blueprints:
            print(tile.position)
            print(tile.entrances)
        #TODO: Start sth like a thread here to generate new Tiles all the time
        #TODO use gen_new_tiles() somewhere here
        

    def gen_background(self):
            # Erstelle eine Surface für den Hintergrund
        background_surface = pg.Surface(self.game_settings.map_size)

        # Generiere das Hintergrundmuster wie zuvor
        tile_size = self.game_settings.small_tile_size
        checkerboard_tile = pg.Surface((tile_size, tile_size))
        checkerboard_tile.fill(pg.Color('white'))
        for x in range(0, tile_size, tile_size // 2):
            pg.draw.line(checkerboard_tile, self.game_settings.bg_line_color, (x, 0), (x, tile_size))
        for y in range(0, tile_size, tile_size // 2):
            pg.draw.line(checkerboard_tile, self.game_settings.bg_line_color, (0, y), (tile_size, y))

        # Blit das karierte Muster über den gesamten Hintergrund
        for x in range(0, self.game_settings.screen_width, tile_size):
            for y in range(0, self.game_settings.screen_height, tile_size):
                background_surface.blit(checkerboard_tile, (x, y))

        # Speichere das generierte Surface für späteren Gebrauch
        self.background_surface = background_surface



    def gen_initial_map(self):
        pass

    def gen_new_tiles(self):
        current_tile_pos = self.player.get_tile_standing_on()
        #TODO create tiles that are adjacent to current_tile_pos
        #Somewhere in here will pick a tile fom blueprints and use it.
        #using the chosen tile's "can_connect" method

    
    def create_tile_blueprints(self):
        """ Creates a bunch of blueprints of tiles to be used by gen_new_tiles and gen_initial_map"""
        tile_images = self.load_tile_images()

        num = 1
        for tile_image in tile_images:

            entrances = self.check_entrances(tile_image)
            
            self.tile_blueprints.append(MapTile(game=self.game,image=tile_image, position=(num,num),possible_spawns=[], entrances=entrances, powerup_mgr=self.powerup_mgr, enemy_mgr=self.enemy_mgr))
            print("MapTile created")
            num +=1
            
    def load_tile_images(self):
        tile_images = [pg.image.load(path) for path in self.game_settings.tile_image_paths.values()]
        return tile_images
    
    def is_transparent(self,pixel):
        """Check if pixel transparent"""
        return pixel.a == 0


    def check_entrances(self,image):
        # Koordinaten der möglichen Eingänge
        coordinates = {
            "top_left": (120, 1),
            "top_right": (330, 1),
            "right_top": (447, 100),
            "right_bottom": (447, 330),
            "bottom_right": (330, 447),
            "bottom_left": (120, 447),
            "left_bottom": (1, 330),
            "left_top": (1, 100)
        }
        
        entrances = []
        for entrance, (x, y) in coordinates.items():
            pixel = image.get_at((x, y))
            if self.is_transparent(pixel):
                entrances.append(entrance)
        
        return entrances


class MapTile:
    def __init__(self, game,image, position:tuple, entrances:list,possible_spawns:list, powerup_mgr:PowerUpManager, enemy_mgr:EnemyManager ) -> None:
        self.game = game
        self.game_settings = self.game.game_settings
        self.image = image
        self.position = position
        self.entrances = entrances #holds possible connections to other tiles
        self.powerups = [] #filled as soon place_entities called
        self.enemies = [] #filled as soon place_entities called

        self.tile_size = self.game_settings.medium_tile_size


        self.powerup_mgr = powerup_mgr
        self.enemy_mgr = enemy_mgr
        self.possible_spawn_positions = possible_spawns #holds tuples with possible spawn locations for enemies or PUs

        self.visited = False
        self.enemies_spawned = False

        self.place_entities() # should place some random entities on tile, when instantiated

    def draw(self):
        pass

    def place_entities(self):
        """ Places powerups and enemies randomly on possible spawn locations"""
        for pos in self.possible_spawn_positions:
            entity = random.choice(self.powerup_mgr.get_random_powerup(), self.enemy_mgr.get_random_enemy())

            if(isinstance(entity, PowerUp)):
                self.powerups.append(entity)
            elif(isinstance(entity,Enemy)):
                self.enemies.append(entity)

            entity.pos = pos #TODO think about positioning: pos is a value on within the tile, but has to be converted to an absolute value that makes sense for the game


    def can_connect(self, other_tile)->bool:
        pass
        

    