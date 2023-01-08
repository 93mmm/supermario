class Button():
    def __init__(self, images, pos):
        self.images = images
        self.current_image = self.images[0]
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.images[0].get_rect(center=(self.x, self.y))

        self.position_check_x = range(self.rect.left, self.rect.right)
        self.position_check_y = range(self.rect.top, self.rect.bottom)

    def update(self, screen):
        screen.blit(self.current_image, self.rect)

    def check_for_input(self, position):
        if position[0] in self.position_check_x and position[1] in self.position_check_y:
            return True
        return False

    def change_image(self, position):
        if position[0] in self.position_check_x and position[1] in self.position_check_y:
            self.current_image = self.images[1]
        else:
            self.current_image = self.images[0]
