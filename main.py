import pygame
import pytmx



class Player:

    def __init__(self, x, y):
        from get_sprite import player_images
        self.images = player_images
        self.direction = "down"
        self.status = "awake"
        self.tmx_data = pytmx.load_pygame(
                    "assets/prototype.tmx"
                )
        self.rect = self.images[self.direction].get_rect(
            topleft=(x, y)
        )

        self.speed = 1
        self.is_collide = False

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if self.handle_collision(keys):

            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.rect.x -= self.speed
                self.direction = "left"

            elif keys[pygame.K_RIGHT] and self.rect.x < 160:
                self.rect.x += self.speed
                self.direction = "right"

            elif keys[pygame.K_UP] and self.rect.y > 0:
                self.rect.y -= self.speed
                self.direction = "up"

            elif keys[pygame.K_DOWN] and self.rect.y < 100:
                self.rect.y += self.speed
                self.direction = "down"

    def handle_collision(self, keys):
        player_rect = self.rect
        x = self.rect.x
        y = self.rect.y

        if keys[pygame.K_LEFT]:
            x -= self.speed
        elif keys[pygame.K_RIGHT]:
            x += self.speed
        elif keys[pygame.K_UP]:
            y -= self.speed
        elif keys[pygame.K_DOWN]:
            y += self.speed
        
        player_rect = pygame.Rect(
            x,
            y,
            player_rect.width,
            player_rect.height
        )

        for obj in self.tmx_data.get_layer_by_name("Object Layer 1"):
            collision_rect = pygame.Rect(
                                obj.x,
                                obj.y,
                                obj.width,
                                obj.height
                            )
            if obj.name in ["Chair", "Bin", "Door", "Table"]:
                if player_rect.colliderect(collision_rect):
                    return False
            if obj.name == "Bed":
                if player_rect.colliderect(collision_rect):
                    self.status = "sleeping"
                else:
                    self.status = "awake"
                
        return True
        
    def draw(self, screen):
        screen.blit(
            self.images[self.direction],
            self.rect
        )


class Game:

    def __init__(self):
        pygame.init()
        GAME_WIDTH = 176
        GAME_HEIGHT = 112
        SCALE = 4
        
        self.screen = pygame.display.set_mode(
            (GAME_WIDTH * SCALE, GAME_HEIGHT * SCALE)
        )

        self.game_surface = pygame.Surface(
            (GAME_WIDTH, GAME_HEIGHT)
        )

        pygame.display.set_caption("Five night at DIS")

        self.clock = pygame.time.Clock()

        # Load map
        self.tmx_data = pytmx.load_pygame(
            "assets/prototype.tmx"
        )

        # Create player from Tiled object
        player_x = 0
        player_y = 0

        for obj in self.tmx_data.get_layer_by_name("Object Layer 1"):

            if obj.name == "Player":
                player_x = obj.x
                player_y = obj.y
                break

        self.player = Player(player_x, player_y)

        self.running = True

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

    def update(self):

        self.player.handle_movement()

    def draw_map(self):

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):

                for x, y, image in layer.tiles():

                    self.game_surface.blit(
                        image,
                        (
                            x * self.tmx_data.tilewidth,
                            y * self.tmx_data.tileheight
                        )
                    )

    def draw(self):

        # Draw everything at 176x128
        self.game_surface.fill((0, 0, 0))

        self.draw_map()

        self.player.draw(self.game_surface)

        # Scale 112x176 -> 448x704
        scaled = pygame.transform.scale(
            self.game_surface,
            self.screen.get_size()
        )

        self.screen.blit(scaled, (0, 0))

        pygame.display.flip()

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(60)

        pygame.quit()


game = Game()
game.run()