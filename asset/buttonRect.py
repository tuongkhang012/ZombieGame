import pygame


class Button:

    def __init__(self, text, x, y, width, height, margin_x, margin_y, color, textcolor,
                 font, hovercolor=None, presscolor=None):
        """
        Create a Button object

        :param text: Text for the button
        :param x: x-coordinate for the button
        :param y: y-coordinate for the button
        :param width: the width of the button
        :param height: the height of the button
        :param margin_x: the margin_x for the text
        :param margin_y: the margin_y for the text
        :param color: the color of the button
        :param textcolor: the color of the text
        :param font: the font used
        """
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.textcolor = textcolor

        if not hovercolor:
            self.hovercolor = self.textcolor
        else:
            self.hovercolor = hovercolor

        if not presscolor:
            self.presscolor = self.textcolor
        else:
            self.presscolor = presscolor

        self.marginx = margin_x
        self.marginy = margin_y
        self.clicked = False

    def draw(self, surface):
        """
        Draw the button while return a bool to detect click

        :param surface: the display to draw the button on
        :return: a boolean for click
        """
        pygame.draw.rect(surface, self.color, self.rect)

        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            surface.blit(self.font.render(self.text, False, self.hovercolor),
                         (self.rect.x + self.marginx, self.rect.y + self.marginy))
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                surface.blit(self.font.render(self.text, False, self.presscolor),
                             (self.rect.x + self.marginx, self.rect.y + self.marginy))
                self.clicked = True
                action = True
        else:
            surface.blit(self.font.render(self.text, False, self.textcolor),
                         (self.rect.x + self.marginx, self.rect.y + self.marginy))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
