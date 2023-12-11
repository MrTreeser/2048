import os
from abc import ABC, abstractmethod

import pygame


class abstract_onclick_comp(ABC):
    @abstractmethod
    def onclick(self, mouse_pos):
        pass

    @abstractmethod
    def get_text(self):
        pass


class abstract_show_comp(ABC):
    @abstractmethod
    def show(self, mouse_pos):
        pass

    @abstractmethod
    def get_text(self):
        pass


def get_font(font, font_size=20):
    if isinstance(font, pygame.font.Font):
        return font
    if font is None or font in pygame.font.get_fonts():
        font = pygame.font.SysFont(font, font_size)
    elif isinstance(font, str) and os.path.exists(font):
        font = pygame.font.Font(font, font_size)
    else:
        print(f'font \'{font}\' cannot be parsed.')
        font = pygame.font.SysFont(None, font_size)
    return font


def load_image(img_uri, size, alpha_convert=False):
    if not os.path.exists(img_uri):
        raise FileNotFoundError(f'img {img_uri} not exists')
    image = pygame.image.load(img_uri)
    image = pygame.transform.scale(image, size)
    if not alpha_convert:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image


def fill_rect(surface: pygame.Surface, rect, color, border_radius):
    if isinstance(rect, tuple):
        rect = pygame.Rect(0, 0, *rect)
    surface.convert_alpha()
    surface.fill(pygame.Color(0, 0, 0, 0), rect=rect)
    pygame.draw.circle(
        surface,
        color,
        (border_radius, border_radius),
        border_radius,
        draw_top_left=True,
    )
    pygame.draw.circle(
        surface,
        color,
        (rect.width - border_radius, border_radius),
        border_radius,
        draw_top_right=True,
    )
    pygame.draw.circle(
        surface,
        color,
        (border_radius, rect.height - border_radius),
        border_radius,
        draw_bottom_left=True,
    )
    pygame.draw.circle(
        surface,
        color,
        (
            rect.width - border_radius,
            rect.height - border_radius,
        ),
        border_radius,
        draw_bottom_right=True,
    )
    surface.fill(
        color,
        pygame.Rect(
            border_radius,
            0,
            rect.width - 2 * border_radius,
            rect.height,
        ),
    )
    surface.fill(
        color,
        pygame.Rect(
            0,
            border_radius,
            rect.width,
            rect.height - 2 * border_radius,
        ),
    )


def center2rect(center, size):
    return pygame.Rect(
        center[0] - size[0] // 2,
        center[1] - size[1] // 2,
        *size,
    )


def rect2center(rect):
    return (rect.x + rect.w // 2, rect.y + rect.h // 2)
