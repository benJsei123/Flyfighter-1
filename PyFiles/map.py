import random
import pygame as pg
from powerup_manager import PowerUpManager, PowerUp
from enemy_manager import EnemyManager, Enemy, TankyEnemy

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
        self.enemy_mgr = EnemyManager(game=self.game)

    

    def set_player(self,player):
        self.player = player

    def update(self):
    
        #Update active tile and visited tiles
        player_center = self.player.rect.center
        for tile in self.active_tile.get_neighbors():
            if tile.rect.collidepoint(player_center):
                if tile != self.active_tile:
                    self.active_tile = tile
                    if(not tile in self.visited_tiles):
                        self.visited_tiles.append(tile)
                break
            
            #let enemies arround player shoot (randomly)
            will_fire_proba = random.random()
            if will_fire_proba < self.game_settings.enemy_fire_proba_thresh:
                if len(tile.enemies)>0:
                    
                    enemy_to_fire = random.choice(tile.enemies)
                    if(enemy_to_fire.guns):
                        enemy_to_fire.fire()

        self.enemy_mgr.update() #reponsible for smart and fast enemy
        #TODO avoid enemies passing through tiles

        self.check_enemy_tile_collision()
        self.check_enemy_enemy_collision()
        self.check_player_tile_collision()
        self.check_bullet_tile_colllision()
        self.check_bullet_player_collision()
        self.check_bullet_enemy_collision()
        self.gen_new_tiles()

    def reset(self):
        # Entferne alle Tiles und damit verbundene Objekte wie Feinde und Power-ups.
        for tile in self.tiles:
            tile.kill()

        # Leere die Listen und Dictionaries, die Kartenobjekte und Zustände speichern.
        self.tiles.clear()
        self.visited_tiles.clear()
        self.entrance_dict.clear()

        # Setze Zähler und Zustandsvariablen zurück.
        self.visited_tiles_amount = 0
        self.active_tile = None
        self.last_player_pos_x = 0
        self.last_player_pos_y = 0

        # Setze Power-up und Enemy Manager zurück.
        #self.powerup_mgr.reset()
        #self.enemy_mgr.reset()

        # Neugenerieren der initialen Map und Setzen der Spielerposition zurück.
        self.initialize_map()
        self.set_player(self.game.player)


    def check_enemy_enemy_collision(self):
        cur_enemies = self.enemy_mgr.get_current_enemies()
        for enemy in cur_enemies:
            last_enemy_pos_x = enemy.last_enemy_pos_x
            last_enemy_pos_y = enemy.last_enemy_pos_y

            for other_enemy in cur_enemies:
                if other_enemy is enemy:
                    continue

                last_other_enemy_pos_x = other_enemy.last_enemy_pos_x
                last_other_enemy_pos_y = other_enemy.last_enemy_pos_y

                if enemy.rect.colliderect(other_enemy.rect):
                    #print('ENEMY  resetted position of ', type(enemy))
                    enemy.rect.x = last_enemy_pos_x
                    enemy.rect.y = last_enemy_pos_y
                    other_enemy.rect.x = last_other_enemy_pos_x
                    other_enemy.rect.y = last_other_enemy_pos_y

                    farther_away = None
                    if enemy.get_fire_direction().magnitude() > other_enemy.get_fire_direction().magnitude():
                        farther_away = enemy
                    else:
                        farther_away = other_enemy
                    farther_away.slow_down()

                else:
                    enemy.last_enemy_pos_x = enemy.rect.x
                    enemy.last_enemy_pos_y = enemy.rect.y


                    

                    #TODO slow down enemy that s farther away from player to not make enemies get stuck in each other


    def check_enemy_tile_collision(self):
        for enemy in self.enemy_mgr.get_current_enemies():
            last_enemy_pos_x = enemy.last_enemy_pos_x
            last_enemy_pos_y = enemy.last_enemy_pos_y

            for tile in self.tiles:
                offset = (tile.rect.x - enemy.rect.x, tile.rect.y - enemy.rect.y)
                collision = enemy.mask.overlap(tile.mask, offset)

                if collision:
                    print('resetted position of ', type(enemy))
                    enemy.last_enemy_pos_x = last_enemy_pos_x
                    enemy.last_enemy_pos_y = last_enemy_pos_y
                    enemy.rect.x = last_enemy_pos_x
                    enemy.rect.y = last_enemy_pos_y




    def check_bullet_enemy_collision(self):
        
        for enemy in self.enemy_mgr.get_current_enemies():
            collisions = pg.sprite.spritecollide(enemy,self.player.guns.bullet_group,dokill=True)
            for col in collisions:
                enemy.take_damage() # + kills enemy if no hp left
                

    def check_bullet_player_collision(self):
        for enemy in self.enemy_mgr.enemy_group:
            collisions = pg.sprite.spritecollide(self.player, enemy.guns.bullet_group, dokill=True)
        
            if collisions:
                self.player.player_stats.take_damage(self.game_settings.enemy_bullet_damage)
            #print(f'HP {self.player.player_stats.hp}')


    def check_bullet_tile_colllision(self):
                
        tiles_poss_collisions = [self.active_tile]
        tiles_poss_collisions.extend(list(self.active_tile.get_neighbors()))

        #BPlayer bullet tile collisions
        player_bullets = self.player.guns.bullet_group
        if(player_bullets):
            for bullet in player_bullets:
                for tile in tiles_poss_collisions:
                    offset = (tile.rect.x - bullet.rect.x, tile.rect.y - bullet.rect.y)
                    collision = bullet.mask.overlap(tile.mask, offset)

                    if collision: # if collision: delete bullet from game
                        bullet.kill()

        #Enemy bullet tile colllision
        for enemy in self.enemy_mgr.enemy_group:
            for bullet in enemy.guns.bullet_group:
                for tile in tiles_poss_collisions:
                    offset = (tile.rect.x - bullet.rect.x, tile.rect.y - bullet.rect.y)
                    collision = bullet.mask.overlap(tile.mask, offset)

                    if collision: # if collision: delete bullet from game
                        bullet.kill()

    def check_player_tile_collision(self):
        #avoid player flying through black pieces
        offset = (self.active_tile.rect.x - self.player.rect.x, self.active_tile.rect.y - self.player.rect.y)
        collision = self.player.mask.overlap(self.active_tile.mask, offset)
        
        if collision: # if collision: set player back to last valid position
            
            self.player.rect.x = self.last_player_pos_x
            self.player.rect.y = self.last_player_pos_y
        else:
            #if no collision, the current pos is valid and therefore stored
            self.last_player_pos_x = self.player.rect.x
            self.last_player_pos_y = self.player.rect.y


        

    def initialize_map(self):
        self.camera_group = self.game.camera_group
        self.gen_background()
        self.find_entrances()
        self.gen_initial_map() #create spawn area

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
                    entrances=entrances, 
                    powerup_mgr=self.powerup_mgr, 
                    enemy_mgr=self.enemy_mgr,
                    camera_group = self.camera_group,
                    )
        self.tiles.append(tile)
        self.active_tile = tile
        
        #print("Map Spawn created")

        
    def gen_new_tiles(self):
        keys = []
   
        keys = self.active_tile.get_empty_neighbors() #get all directions where tile adding necessary
        
        
        if len(keys) > 0:
            #print("generating new tiles for positions:" , keys)
            active_tile_pos = self.active_tile.rect.topleft #important for positioning of new tile
            
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
                    
                    
                    tile_idx = 0 #index to choose from tile set (will be set to random number in range 0-16)
                    found_match = False #required for levelwise testing if tile fits (first test for two matching entrances, then for one)


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
                        powerup_mgr= self.powerup_mgr,
                        enemy_mgr= self.enemy_mgr,
                        camera_group=self.camera_group
                    )
                    self.tiles.append(tile)
                    self.update_neighbors(tile,side=key)
                

                    
                    
                    #print("Map tile nummber ", len(self.tiles) , " created.")

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
        """ Used in Map.find_entrances() which sets up the entrance_dict of the Map class. 
        Map class uses entrance_dict to generate new tiles"""
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
    def __init__(self, game, image, position:tuple, entrances:list, powerup_mgr:PowerUpManager, enemy_mgr:EnemyManager, camera_group ) -> None:
        super().__init__(camera_group)
        self.game = game
        self.screen = game.screen
        
        self.game_settings = self.game.game_settings
        self.image = image

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
        
        #Enemies guard map tile entrances (spawn points for enemies)
        offset = 35 # defines how much towards center enemys are placed
        self.possible_spawn_positions = {
            "top_left": (120, 1+offset),
            "top_right": (330, 1+offset),
            "right_top": (447-offset, 100),
            "right_bottom": (447-offset, 330),
            "bottom_right": (330, 447-offset),
            "bottom_left": (120, 447-offset),
            "left_bottom": (1+offset, 330),
            "left_top": (1+offset, 100)
        }

        #Store where entities have been spawned
        
        
         #has to be tuples
        self.visited = False
        self.enemies_spawned = False

        self.mask =  pg.mask.from_surface(self.image)
        
        
        self.place_entities() # should place some random entities on tile, when instantiated
        

    def get_enemies(self):
        return self.enemies

    def get_neighbors(self):
        return [i for k, i in self.neighbor_tile_dict.items() if isinstance(i,MapTile)]

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
        for pos_name, pos in self.possible_spawn_positions.items():
            if pos_name in set([ entr for entr_list in Map.check_entrances(self=self.game.map,image=self.image).values() for entr in entr_list ]): 
                # this comprehension makes a single list from a list looking like this: 
                #[[topleft,topright],[right_right,right_left],[bottomright,bottomright],[lefttop,leftright],...]
                
                rand_num = random.random()
                if rand_num < self.game_settings.enemy_spawn_chance:
                    
                    absolute_position = (self.rect.topleft[0]+pos[0],self.rect.topleft[1]+pos[1])

                    entity = self.enemy_mgr.get_random_enemy(absolute_position) 
                    
                    #if(isinstance(entity, PowerUp)):
                    #    self.powerups.append(entity)
                    
                    self.enemies.append(entity)

        self.enemies_spawned = True
        


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

        
        

    