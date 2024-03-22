import random
import pygame as pg
from powerup_manager import PowerUpManager, PowerUp
from enemy_manager import EnemyManager, Enemy

class Map:
    tile_image_paths = [] #holds paths to tile images

    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.player = game.player
        self.game_settings = game.game_settings
        self.background_surface = None
        

        #Tiles
        self.tile_bluprints = self.create_tile_blueprints() #holds MapTile objects
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
        #TODO: Start sth like a thread here to generate new Tiles all the time
        #TODO use gen_new_tiles() somewhere here
        

    def gen_background(self):
            # Erstelle eine Surface für den Hintergrund
        background_surface = pg.Surface(self.game_settings.map_size)

        # Generiere das Hintergrundmuster wie zuvor
        tile_size = self.game_settings.map_tile_size
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

    
    def create_tile_blueprints(self)->list:
        """ Creates a bunch of blueprints of tiles to be used by gen_new_tiles and gen_initial_map"""
        tiles = []
        for tile_image_path in Map.tile_image_paths:
            position = (0,0)
            entrances = {
                "top": [],
                "bottom": [],
                "left": [],
                "right": []
            }
    	    #TODO find a way to fill the entrance dict depending on the image of tile (CSV that holds info about each blueprint? Image recognisiton with pixel check for black/white?)

            tiles.append(MapTile(tile_image_path, position, entrances, self.powerup_mgr, self.enemy_mgr))
            

class MapTile:
    def __init__(self, image_path:str, position:tuple, entrances:dict,possible_spawns:list, powerup_mgr:PowerUpManager, enemy_mgr:EnemyManager ) -> None:
        
        self.image = pg.image.load(image_path)
        self.position = position
        self.entrances = entrances #holds possible connections to other tiles
        self.powerups = [] #filled as soon place_entities called
        self.enemies = [] #filled as soon place_entities called

        self.powerup_mgr = powerup_mgr
        self.enemy_mgr = enemy_mgr
        self.possible_spawn_positions = possible_spawns #holds tuples with possible spawn locations for enemies or PUs

        self.visited = False
        self.enemies_spawned = False

        self.place_entities() # should place some random entities on tile, when instantiated

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
        

    