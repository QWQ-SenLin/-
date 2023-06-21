import pygame

pygame.init()
huase_pos = {
    "meihua" : (270 , 178 , 20 , 24) ,
    "fangkuai" : (246 , 178 , 20 , 24),
    "hongxin" : (294 , 178 , 20 , 24) ,
    "heitao" : (318 , 178 , 20 , 24)
}
image = pygame.image.load('image/image.png')
cards_number = ['A' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '10' , 'J' , 'Q' , 'K']
card_group = pygame.sprite.Group()

def Text(size , font , pos , color):   #打印文字
    Font = pygame.font.SysFont('华文新魏' , size)
    surface = Font.render(font , 1 , color)  #打印内容，是否抗锯齿，文字颜色，背景颜色
    rect = surface.get_rect()
    rect.center = pos   #位置
    return (surface , rect)

class Card(pygame.sprite.Sprite):
    def __init__(self , number , huase) -> None:
        super().__init__()
        self.number = number
        self.huase = huase
        self.flag = True #是否翻面，F正
        self.image = pygame.Surface((110 , 150) , pygame.SRCALPHA , 32).convert_alpha()
        self.image_F = pygame.Surface((110 , 150) , pygame.SRCALPHA , 32).convert_alpha()
        self.init_number()
        self.init_huase()
        self.rect = self.image.get_rect()
        self.pos = [0 , 0]
        # card_group.add(self)

    def __str__(self):
        return cards_number[self.number]

    def __int__(self):
        return self.number

    def init_number(self):
        self.image_F.blit(image , (0 , 0) , (22 , 10 , 100 , 140))
        self.image.blit(image , (0 , 0) , (158 , 12 , 100 , 140))
        self.color = (255 , 0 , 0) if self.huase == 'hongxin' or self.huase == 'fangkuai' else (55 , 55 , 55)
        self.image.blit(*Text(25 , cards_number[self.number] , (15 , 20) , self.color))
        tmp = Text(25 , cards_number[self.number] , (85 , 115) , self.color)
        self.image.blit(pygame.transform.rotate(tmp[0] , 180) , tmp[1])

    def init_huase(self):             
        huase_surface = pygame.Surface((20 , 24) , pygame.SRCALPHA).convert_alpha()
        huase_surface.blit(image , (0 , 0) , huase_pos[self.huase])
        self.image.blit(huase_surface , (5 , 30))
        self.image.blit(pygame.transform.rotate(huase_surface , 180) , (75 , 80))

    def show(self , screen):
        self.rect.topleft = self.pos
        screen.blit(self.image if not self.flag else self.image_F , self.rect)