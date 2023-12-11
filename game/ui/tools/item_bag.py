import pygame
import numpy as np
from ..tools.common import load_image
from .common import abstract_onclick_comp
from .text import Text
from .floating_tip import Floating_tip


class Item_bag(abstract_onclick_comp):
    ## 传入start_pos是因为item_bag返回的是局部的surface而不是在整个window上画，此时在onclick时需要知道是否点击在范围中了
    def __init__(self, size, item_bag=np.zeros(12, int), start_pos=(0, 0)):
        self.board_size = 200
        self.hover_time = 15
        self.start_pos = (start_pos[0], start_pos[1])
        self.rect = pygame.Rect(self.board_size, self.board_size, size[0], size[1])
        self.width = self.rect.w
        self.height = self.rect.h
        self.item_bag = item_bag
        self.item_to_png = {
            1: 'game\\ui\\assets\\images\\random.png',
            2: 'game\\ui\\assets\\images\\copy_32.png',
            3: 'game\\ui\\assets\\images\\copy_128.png',
            4: 'game\\ui\\assets\\images\\frozen_time.png',
            5: 'game\\ui\\assets\\images\\bigger_num.png',
            6: 'game\\ui\\assets\\images\\symmetry.png', 
            7: 'game\\ui\\assets\\images\\get_more_score.png', 
            8: 'game\\ui\\assets\\images\\double.png',
            9: 'game\\ui\\assets\\images\\smaller_num.png',
            10: 'game\\ui\\assets\\images\\merge_update.png',
            11: 'game\\ui\\assets\\images\\random_remove.png',
            12: 'game\\ui\\assets\\images\\max_remove.png',  # 我还是不到啊
        }
        self.item_to_tip = {
            1: 'shuffle',
            2: 'copy a num <=32',
            3: 'copy a num <=128',
            4: 'move twice',
            5: 'the num to generate increases',
            6: 'get score according to the symmetry',  # 我不到啊
            7: 'get score according to one blanck(3)',  # 我不到啊
            8: 'double one blanck',
            9: 'the num to generate decreases',
            10: 'get score according to merging time(3)',
            11: 'eliminate one blanck',
            12: 'eliminate the bigest blanck',  # 我还是不到啊
        }
        self.window = pygame.Surface(
            (self.width + 2 * self.board_size, self.height + 2 * self.board_size)
        ).convert_alpha()
        self.window.fill((0, 0, 0, 0))

        self.floating_time = 0
        self.last_mouse_pos = (0, 0)
        self.tip = Text((-1000, -1000), '')

        self.update(self.item_bag)
        self.last_onclick = -1

        png_width = self.width // 4
        png_height = self.height // 3
        self.image_cache_dict = {
            k: load_image(v, (png_width, png_height), alpha_convert=True)
            for k, v in self.item_to_png.items()
        }
        

    def get_text(self):
        return self.last_onclick

    def draw(self):
        item_pos = 0
        png_width = self.width // 4
        png_height = self.height // 3
        self.window.fill((0, 0, 0, 0))

        for item in self.item_bag:
            if item in self.item_to_png.keys():
                item_png = self.image_cache_dict[item]  # 分为4*3共12个道具
                self.window.blit(
                    item_png,
                    (
                        self.rect.x + png_width * (item_pos % 4),
                        self.rect.y + png_height * (item_pos // 4),
                    ),
                )
                item_pos += 1
        if self.floating_time >= self.hover_time:
            self.tip.show(self.window)

    def show(self, window):
        self.draw()
        window.blit(
            self.get_surface(),
            (self.start_pos[0] - self.board_size, self.start_pos[1] - self.board_size),
        )

    def update(self, item_bag):
        self.item_bag = item_bag
        self.draw()

    # 如果不在范围中返回false,否则返回对应的道具编号或-1
    def onclick(self, mouse_pos):
        mouse_pos = (mouse_pos[0] - self.start_pos[0], mouse_pos[1] - self.start_pos[1])
        if 0 < mouse_pos[0] < self.width and 0 < mouse_pos[1] < self.height:
            item_num = (mouse_pos[0] * 4 // self.width) + 4 * (
                mouse_pos[1] * 3 // self.height
            )
            self.last_onclick = (
                self.item_bag[item_num] if self.item_bag[item_num] != 0 else False
            )
            return self.last_onclick
        else:
            return False

    def floating_on(self, mouse_pos):
        mouse_pos = (mouse_pos[0] - self.start_pos[0], mouse_pos[1] - self.start_pos[1])
        if 0 < mouse_pos[0] < self.width and 0 < mouse_pos[1] < self.height:
            if self.floating_time == self.hover_time:
                item_num = (mouse_pos[0] * 4 // self.width) + 4 * (
                    mouse_pos[1] * 3 // self.height
                )
                self.last_onclick = (
                    self.item_bag[item_num] if self.item_bag[item_num] != 0 else False
                )
                if self.last_onclick:
                    self.tip = Text(
                        (
                            mouse_pos[0] + self.board_size,
                            mouse_pos[1] + self.board_size,
                        ),
                        self.item_to_tip[self.last_onclick],
                        font_color=(150, 150, 150),
                        font_size=40,
                    )
                    self.draw()
            if self.last_mouse_pos == mouse_pos:
                self.floating_time += 1
                print(self.floating_time)
                if self.floating_time >= self.hover_time:
                    return True
            else:
                self.floating_time = 0
                self.draw()
            self.last_mouse_pos = mouse_pos
            return False

    def get_surface(self):
        return self.window

    def pack_data(self):
        return self.item_bag.tolist()

    def check_data(self, data):
        if not (isinstance(data, list) and len(data) == 12):
            return False
        for i in data:
            if not (isinstance(i, int) and i in self.item_to_png.keys()):
                return False
        return True

    def load_data(self, data):
        if not self.check_data(data):
            return False
        self.item_bag = np.array(data)
        return True
