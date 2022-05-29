from Objects import *
class UI:
    def paint_Map(self,screen,Map):
        for obj in Map.Objects:
            if type(obj) in [Mobs, Boss_Kozlov]:
                screen.blit(obj.animation.image, (obj.Point + Map.Freshman.Phys.d).tuple())
            elif type(obj)==Message:
                obj.draw_text(screen,Map)
            else:
                screen.blit(obj.image, (obj.Point + Map.Freshman.Phys.d).tuple())
        screen.blit(Map.Freshman.animation.image, (Map.Freshman.Point + Map.Freshman.Phys.d).tuple())

        pygame.draw.rect(pygame.display.set_mode([0, 0], pygame.FULLSCREEN), (0, 0, 0),(100, 100, Map.Freshman.maxhp, 20))
        pygame.draw.rect(pygame.display.set_mode([0, 0], pygame.FULLSCREEN), (0, 192, 0),(100, 100, Map.Freshman.hp, 20))

        f1 = pygame.font.Font(None, 36)
        text = f1.render(f"{Map.Freshman.hp} / {Map.Freshman.maxhp}", True,(0, 0, 0))
        screen.blit(text, (100 + Map.Freshman.maxhp + 20, 98))