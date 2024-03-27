import random
import pygame as pg
from powerup_manager import PowerUpManager, PowerUp
from enemy_manager import EnemyManager, Enemy

class Map:
    

    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.game_settings = game.game_settings
        self.background_surface = None
        self.player = None
        self.camera_group = None
        self.tile_images = self.load_tile_images()
        
        self.last_player_pos_x = 0
        self.last_player_pos_y = 0

        #Tiles
        self.visited_tiles_amount = 1
        self.visited_tiles = []
        self.tiles = []
        
        
        self.active_tile = None
        self.entrance_dict = {}

        self.powerup_mgr = PowerUpManager(game=self.game,tiles=self.tiles, player=self.player) #TODO the tile should be filled or updated at some point!!
        self.enemy_mgr = EnemyManager()


    def set_player(self,player):
        self.player = player

    def update(self):
        player_center = self.player.rect.center
        for tile in self.tiles:

                    

            offset = (tile.rect.x - self.player.rect.x, tile.rect.y - self.player.rect.y)
            collision = self.player.mask.overlap(tile.mask, offset)
            if collision: # if collision: set player back to last valid position
                
                self.player.rect.x = self.last_player_pos_x
                self.player.rect.y = self.last_player_pos_y
            else:
                #if no collision, the current pos is valid and therefore stored
                self.last_player_pos_x = self.player.rect.x
                self.last_player_pos_y = self.player.rect.y
        
            if tile.rect.collidepoint(player_center):
                if tile != self.active_tile:
                    self.active_tile = tile
                    if(not tile in self.visited_tiles):
                        self.visited_tiles.append(tile)
                break

        
        self.gen_new_tiles()

        #self.gen_new_tiles()


    def initialize_map(self):
        self.camera_group = self.game.camera_group
        self.gen_background()
        self.find_entrances()
        self.gen_initial_map() #create spawn area
        
        
        #TEST
        # for tile in self.tile_blueprints:
        #     print(tile.position)
        #     print(tile.entrances)


        #TODO: Start sth like a thread here to generate new Tiles all the time
        #TODO use gen_new_tiles() somewhere here
        

    def gen_background(self):
            # Erstelle eine Surface für den Hintergrund
        background_surface = pg.Surface(self.game_settings.map_size)

        # si
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
        #Note that each tile is 448x448

        #Also: Start with tile_9 for spawn (is nice and open)

        tile_image = self.load_tile_images()[9]
        entrances = self.entrance_dict["tile_9"]

        tile = MapTile(
                    game=self.game,
                    image=tile_image, 
                    position=(500,180),
                    possible_spawns=[], 
                    entrances=entrances, 
                    powerup_mgr=self.powerup_mgr, 
                    enemy_mgr=self.enemy_mgr,
                    camera_group = self.camera_group,
                    )
        self.tiles.append(tile)
        self.active_tile = tile
        print("Map Spawn created")

        
    def gen_new_tiles(self):
        keys = []
   
        keys = self.active_tile.get_empty_neighbors()
        
        
        if len(keys) > 0:
            print("generating new tiles for positions:" , keys)
            active_tile_pos = self.active_tile.rect.topleft #important for positioning
            
            for key in keys: #in keys is every key at which the active tile has no neighbur yet
                    
                    #find position as coordinates to place new tile at 
                    if(key=="top"):  
                        position = (active_tile_pos[0],active_tile_pos[1]-448) #place above means subtract 448 from tile's y coordinate
                    if(key=="bottom"): 
                        position = (active_tile_pos[0], active_tile_pos[1]+448) # 448 step down
                    if(key=="left"): 
                        position =  (active_tile_pos[0]-448 , active_tile_pos[1] )
                    if(key=="right"): 
                        position = (active_tile_pos[0]+448 , active_tile_pos[1])
                    
                    
                    tile_idx = 0
                    found_match = False


                    #Searching for a matching entrance combination
                    
                    #Trying tiles in a random order each time
                    indices = list(range(len(self.tile_images))) 
                    random.shuffle(indices) 

                    #First round (perfect match = everey entrance matches)
                    for idx in indices :
                        entrances_new_tile = self.entrance_dict[f"tile_{idx}"] 

                        if(self.active_tile.can_connect_perfectly(entrances_new_tile,side=key)):
                            tile_idx = idx
                            found_match=True

                    #Second round (at least one entrance matches)
                    if not found_match:
                        for idx in random.shuffle(range(len(self.tile_images))) :
                            entrances_new_tile = self.entrance_dict[f"tile_{idx}"] 

                            if(self.active_tile.can_connect(entrances_new_tile,side=key)):
                                tile_idx = idx
                                found_match = True
                    
                    if not found_match:
                        tile_idx = random.randint(0,len(self.tile_images))  
                        found_match = True


                    #At this point we know the idx in the images of the tile we want to attach
                        
                    tile = MapTile(
                        game=self.game,
                        image=self.tile_images[tile_idx],
                        position=position,
                        entrances= self.entrance_dict[f"tile_{tile_idx}"],
                        possible_spawns=[],
                        powerup_mgr= self.powerup_mgr,
                        enemy_mgr= self.enemy_mgr,
                        camera_group=self.camera_group
                    )
                    self.tiles.append(tile)
                    

                    self.update_neighbors(tile,side=key)
                    
                    
                    print("Map tile nummber ", len(self.tiles) , " created.")

    def update_neighbors(self, new_tile, side):
        # Aktualisiere das neue Tile als Nachbarn des aktiven Tiles
        self.active_tile.add_neighbor(new_tile, side)
        
        # Finde das gegenüberliegende Side, um das neue Tile korrekt zu aktualisieren
        opposite_side = self.get_opposite_side(side)
        new_tile.add_neighbor(self.active_tile, opposite_side)

        # Prüfe und aktualisiere umliegende Tiles für das neue Tile
        for check_side in ['top', 'bottom', 'left', 'right']:
            neighbor_pos = self.get_neighbor_position(new_tile.rect.topleft, check_side)
            neighbor_tile = self.find_tile_at_position(neighbor_pos)
            if neighbor_tile:
                new_tile.add_neighbor(neighbor_tile, check_side)
                neighbor_tile.add_neighbor(new_tile, self.get_opposite_side(check_side))

    def get_neighbor_position(self, position, side):
        # Berechne die Position des Nachbars basierend auf dem Side
        x, y = position
        if side == "top":
            return (x, y - 448)
        elif side == "bottom":
            return (x, y + 448)
        elif side == "left":
            return (x - 448, y)
        elif side == "right":
            return (x + 448, y)

    def find_tile_at_position(self, position):
        # Finde ein Tile basierend auf einer Position
        for tile in self.tiles:
            if tile.rect.topleft == position:
                return tile
        return None



    def get_opposite_side(self,side):
        if side=="top": return "bottom"
        if side=="bottom": return "top"
        if side=="left": return "right"
        if side=="right": return "left"


    def find_entrances(self):
        """ Locates and saves entrances for all possible map tile sprites"""
        tile_images = self.load_tile_images()

        for number, tile_image in enumerate(tile_images):
            entrances = self.check_entrances(tile_image)
            self.entrance_dict[f"tile_{number}"] = entrances
     
            
    def load_tile_images(self):
        tile_images = [pg.image.load(path) for path in self.game_settings.tile_image_paths.values()]
        return tile_images
    
    def is_transparent(self,pixel):
        """Check if pixel transparent"""
        return pixel.a == 0


    def check_entrances(self,image):
        # coordinates of possible entrances
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
        
        entrances = {
            "top" : [],
            "right" : [],
            "bottom" : [],
            "left" : [],
        }

        coordinate_key_iterator = iter(coordinates.keys())

        for key in entrances.keys(): 
            for _ in range(2): #2 possible entrances per side
                entrance = next(coordinate_key_iterator)
                x,y = coordinates[entrance]
                pixel = image.get_at((x, y))
                if self.is_transparent(pixel):
                    entrances[key].append(entrance)
        
        return entrances


class MapTile(pg.sprite.Sprite):
    def __init__(self, game, image, position:tuple, entrances:list,possible_spawns:list, powerup_mgr:PowerUpManager, enemy_mgr:EnemyManager, camera_group ) -> None:
        super().__init__(camera_group)
        self.game = game
        self.screen = game.screen
        
        self.game_settings = self.game.game_settings
        self.image = image

        self.mask =  pg.mask.from_surface(self.image)


        self.neighbor_tile_dict = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False
        }

        self.rect = self.image.get_rect(topleft=position)
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

    def get_empty_neighbors(self):
        empty_neighbors = []
        for key,item in self.neighbor_tile_dict.items(): #key top,bottom,left,right. items allNone by de
            if item == False: #if there is no neigbor yet / false
                empty_neighbors.append(key)
        
        return empty_neighbors

    def add_to_cameragroup(self):
        super().__init__(self.camera_group)

    def place_entities(self):
        """ Places powerups and enemies randomly on possible spawn locations"""
        for pos in self.possible_spawn_positions:
            entity = random.choice(self.powerup_mgr.get_random_powerup(), self.enemy_mgr.get_random_enemy())

            if(isinstance(entity, PowerUp)):
                self.powerups.append(entity)
            elif(isinstance(entity,Enemy)):
                self.enemies.append(entity)

            entity.pos = pos #TODO think about positioning: pos is a value on within the tile, but has to be converted to an absolute value that makes sense for the game


    def add_neighbor(self, tile, side):
        self.neighbor_tile_dict[side] = tile

    def can_connect_perfectly(self, entrances, side="top")->bool:
        """
        reuturns true/false, checking if 2 entrances of desired connection work
        Params:

            side: can have values "top", "bottom", "left", "right"
        """

        if side=="top":
            if(set(self.entrances["top"])== set(entrances["top"])):  return True
            else: return False

        if side=="bottom":
            if(set(self.entrances["bottom"])== set(entrances["bottom"])): return True
            else: return False
            
        if side=="left":
            if(set(self.entrances["left"])== set(entrances["left"])): return True
            else: return False
            
        if side=="right":
            if(set(self.entrances["right"])== set(entrances["right"])): return True
            else: return False


        #self.entrances stores all entrances of this tile

        
    
    
    def can_connect(self, entrances:dict, side="top")->bool:
        """
        Checks for a connection to other tile that may be imperfect (1 entrance cut off)
        
        Params:

            side: can have values "top", "bottom", "left", "right"
        """
        
        #Double Check
        if(self.can_connect_perfectly(self,entrances,side)): return True

        #check cut quantities
        if side=="top":
            if(set(self.entrances["top"]) & set(entrances["top"])):  return True
            else: return False

        if side=="bottom":
            if(set(self.entrances["bottom"]) & set(entrances["bottom"])): return True
            else: return False
            
        if side=="left":
            if(set(self.entrances["left"]) & set(entrances["left"])): return True
            else: return False
            
        if side=="right":
            if(set(self.entrances["right"]) & set(entrances["right"])): return True
            else: return False

        
        

    