from features.Game import *
pygame.init() # Inicialização

def main():
    
    pygame.display.set_caption("Tesouro Pirata")
    game = Game()

    # Estado do jogo
    menu = True
    while True:
        if menu:
            game.showMenu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu = False
                        game.reset() 
        else:
            game.run()
            menu = True

if __name__ == "__main__":
    main()


