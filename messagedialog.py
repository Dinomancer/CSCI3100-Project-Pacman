import pygame

class MessageDialog:
    def __init__(self, message, screen):
        self.screen = screen
        self.message = message
        self.font = pygame.font.Font(None, 32)

    def show(self):
        dialog_rect = pygame.Rect(400, 200, 480, 320)
        dialog_surface = pygame.Surface((480, 320))
        dialog_surface.fill((50, 50, 50))
        pygame.draw.rect(dialog_surface, (200, 200, 200), pygame.Rect(10, 10, 460, 300), 5)
        text = self.font.render(self.message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(240, 160))
        dialog_surface.blit(text, text_rect)

        self.screen.blit(dialog_surface, dialog_rect)
        pygame.display.update(dialog_rect)

        # Wait for 1 second
        timer = pygame.time.get_ticks() + 1000  # Set timer for 1 second
        while pygame.time.get_ticks() < timer:
            pass

        # Erase dialog
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        # Return control back to main program
        return
"""
class MessageDialog:
    def __init__(self, screen, text, font_size=24, position=None, bg_color=(0, 0, 0), text_color=(255, 255, 255)):
        self.screen = screen
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color = text_color

        if position is None:
            self.position = (screen.get_width() // 2, screen.get_height() // 2)
        else:
            self.position = position

        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def draw(self):
        text_rect = self.text_surface.get_rect()
        text_rect.center = self.position
        self.screen.fill(self.bg_color)
        self.screen.blit(self.text_surface, text_rect)
        pygame.display.flip()

    def show(self):
        self.draw()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    # sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return
"""