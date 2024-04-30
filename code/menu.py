import pygame

# Créer une fonction d'initialisation des boutons
def init_buttons():
    pygame.init()  # Initialisation de Pygame ici

    # Créer les boutons
    class Button:
        def __init__(self, image_path, x, y):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    x_resume_button = 100  # Remplacez par la position X désirée
    y_resume_button = 100  # Remplacez par la position Y désirée
    x_exit_button = 100   # Remplacez par la position X désirée
    y_exit_button = 200   # Remplacez par la position Y désirée

    # Chemins d'accès aux images
    exit_img_path = "../graphics/menu/exit_button.png"
    resume_img_path = "../graphics/menu/start_button.png"

    # Créer et retourner les instances de boutons
    resume_button = Button(resume_img_path, x_resume_button, y_resume_button)
    exit_button = Button(exit_img_path, x_exit_button, y_exit_button)
    return resume_button, exit_button