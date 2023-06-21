import pygame
from threading import Thread
import card , random , time

def init():
    global screen , cards , map_cards , card_bg
    global x0 , y0 , sepx , sepy , card_size , width , height
    pygame.init()

    card_size = (100 , 140)
    x0 , y0 , sepx , sepy = 50 , 50 , 20 , 30
    width = x0 * 2 + card_size[0] * 10 + sepx  * 9
    height = 900
    screen = pygame.display.set_mode((width , height))

    cards = [card.Card(i % 13 , "heitao") for i in range(104)]
    card_bg = pygame.image.load('image/card_bg.png')
    random.shuffle(cards)

    map_cards = [None for i in range(10)]
    for i in range(4):
        map_cards[i] = cards[:6]
        del cards[:6]
    for i in range(4 , 10):
        map_cards[i] = cards[:5]
        del cards[:5]

    for i in range(50):
        cards[i].pos = [width - x0 - card_size[0] - i // 10 * 10 , height - y0 - card_size[1]]

class Main():
    def __init__(self) -> None:
        self.game_over = False
        self.run = True
        self.mouse_down_flag = False
        self.mouse_drag = False
        self.mouse_from_index = []
        self.move_cards = []
        self.ok_cards = []
        self.update_thread = Thread(target = self.update)
        self.update_thread.start()
        self.main()

    def main(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    index = self.get_index(mouse_pos)
                    if index[0] != -1:
                        self.mouse_down_flag = True
                    if width - x0 - card_size[0] - 50 <= mouse_pos[0] <= width - x0:
                        if height - y0 - card_size[1] <= mouse_pos[1] <= height - y0:
                            self.add_card_to_map()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_up()
            self.mouse_down()
            self.judge_card()
                         
    def update(self):
        while self.run:
            screen.fill((14 , 132 , 54))
            tmp = []
            for i in range(10):
                screen.blit(card_bg , (x0 + i * (card_size[0] + sepx) , y0))
                for j in range(len(map_cards[i])):
                    if map_cards[i][j] not in self.move_cards:
                        to_pos = (x0 + i * (card_size[0] + sepx) , j * sepy + y0)
                        map_cards[i][j].pos[0] += (to_pos[0] - map_cards[i][j].pos[0]) / 20
                        map_cards[i][j].pos[1] += (to_pos[1] - map_cards[i][j].pos[1]) / 20
                        if abs(map_cards[i][j].pos[0] - to_pos[0]) > 0.1 and abs(map_cards[i][j].pos[1] - to_pos[1]) > 0.1:
                            tmp.append(map_cards[i][j])
                        else:
                            map_cards[i][j].show(screen)
                if map_cards[i]:
                    map_cards[i][-1].flag = False
            for i in tmp:
                i.show(screen)
            for i in self.move_cards:
                i.show(screen)
            for i in range(len(self.ok_cards)):
                for j in range(12 , -1 , -1):
                    to_pos = (x0 + i * (card_size[0] + sepx) , height - y0 - card_size[1] - j * 4)
                    self.ok_cards[i][j].pos[0] += (to_pos[0] - self.ok_cards[i][j].pos[0]) / 20
                    self.ok_cards[i][j].pos[1] += (to_pos[1] - self.ok_cards[i][j].pos[1]) / 20
                    self.ok_cards[i][j].show(screen)
            for i in range(len(cards) - 1 , -1 , -1):
                cards[i].show(screen)
            if self.game_over:
                screen.blit(*card.Text(150 , "恭喜你过关啦啦啦" , (width // 2 , height // 2) , (255 , 215 , 0)))
            pygame.display.flip()

    def get_index(self , pos):
        if pos[0] < x0 or pos[0] > width - x0 or pos[1] < y0:
            return (-1 , 114514)
        i = (pos[0] - x0) // (sepx + card_size[0])
        j = (pos[1] - y0) // sepy
        if i * (card_size[0] + sepx) + x0 + card_size[0] < pos[0]:
            return (-1 , 114514)
        if j < len(map_cards[i]):
            return (i , j)
        if pos[1] <= (len(map_cards[i]) - 1) * sepy + y0 + card_size[1]:
            return (i , len(map_cards[i]) - 1)
        return (-1 , 114514)

    def mouse_down(self):
        if not self.mouse_down_flag:
            return None
        mouse_pos = pygame.mouse.get_pos()
        index = self.get_index(mouse_pos)
        if not self.mouse_drag:
            if not self.can_move(*index):
                return None
            self.mouse_drag = True
            self.mouse_from_index = index
            for i in self.move_cards:
                i.move_x = i.pos[0] - mouse_pos[0]
                i.move_y = i.pos[1] - mouse_pos[1]
        else:
            for i in self.move_cards:
                i.pos[0] = i.move_x + mouse_pos[0]
                i.pos[1] = i.move_y + mouse_pos[1]

    def mouse_up(self):
        if not self.move_cards:
            return None
        global map_cards
        self.mouse_down_flag = False
        self.mouse_drag = False
        mouse_pos = pygame.mouse.get_pos()
        index = self.get_index(mouse_pos)
        if self.can_to(*index):
            map_cards[index[0]] += self.move_cards
            i , j = self.mouse_from_index
            del map_cards[i][j:]
        self.move_cards.clear()

    def can_move(self , i , j):
        if i == -1 or j == -1:
            return False
        if map_cards[i][j].flag:
            return False
        self.move_cards = map_cards[i][j:]
        for i in range(1 , len(self.move_cards)):
            if self.move_cards[i - 1].number - self.move_cards[i].number != 1 or self.move_cards[i - 1].huase != self.move_cards[i].huase:
                self.move_cards.clear()
                return False
        return True

    def can_to(self , i , j):
        if i == -1:
            return False
        if not map_cards[i]:
            return True
        if map_cards[i][-1].number - self.move_cards[0].number == 1:
            return True
        return False

    def judge_card(self):
        if not any(map_cards):
            self.game_over = True
            return None
        for i in range(10):
            l = len(map_cards[i])
            if l < 13:
                continue
            if list(range(12 , -1 , -1)) == list(map(int , map_cards[i][-13:])):
                self.ok_cards.append(map_cards[i][-13:])
                del map_cards[i][-13:]
    
    def add_card_to_map(self):
        if not cards:
            return None
        if [] in map_cards:
            return None
        for i in range(10):
            top = cards.pop(0)
            map_cards[i].append(top)

init()
main = Main()