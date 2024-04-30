import pygame

pygame.init()

# Créer les boutons
class Button:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

x_start_button = 100  # Remplacez par la position X désirée
y_start_button = 100  # Remplacez par la position Y désirée
x_exit_button = 100   # Remplacez par la position X désirée
y_exit_button = 200   # Remplacez par la position Y désirée

# Chemins d'accès aux images
exit_img_path = "Projet_NSI_2/graphics/menu/exit_button.png"
start_img_path = "Projet_NSI_2/graphics/menu/start_button.png"

# Créer les instances de boutons
start_button = Button(start_img_path, x_start_button, y_start_button)
exit_button = Button(exit_img_path, x_exit_button, y_exit_button)
