from models.Pirate import *
from models.Chronometer import *
from factories.TreasureFactory import *
from pathlib import Path

class Game():

    def __init__(self, width=stts.width, height=stts.height):
        self.running = True
        self.stopEvent = threading.Event()
        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode((width, height))
        self.menuBackground = self._setMenuBackground()
        self.lastTreasureSpawnTime = pygame.time.get_ticks()

    @staticmethod
    def _setMenuBackground(imagePath=Path("assets/background/menu.png"), width=stts.width, height=stts.height):
        sprite = pygame.image.load(imagePath)
        return pygame.transform.scale(sprite, (width, height))

    def showMenu(self):
        self.win.blit(self.menuBackground, (0, 0))
        pygame.display.update()

    def reset(self):
        self.running = True

    def run(self):

        self.lastTreasureSpawnTime = pygame.time.get_ticks() # Ultimo instante que um novo tesouro foi gerado.

        print(f"\nA solução para sincronização de processos usada nessa partida é: {stts.synchMenchanism.capitalize()} ⚙️💻")
        if stts.isTest: print("O jogo foi iniciado no modo de teste, a tecla de ação para ambos os piratas é o ESPAÇO ⚠️🕹️")

        #Instanciando jogadores.
        p1 = Pirate(1,
                    [stts.margin, stts.height//2 - stts.playerSize[1]//2],
                    Path("assets/pirate/pirateRedSprites.png"))
        p2 = Pirate(2,
                    [stts.width - stts.playerSize[0] - stts.margin, stts.height//2 - stts.playerSize[1]//2],
                    Path("assets/pirate/pirateBlueSprites.png"))
        
        #Instancindo baú de tesouros compartilhados.
        treasureChest = SharedChest()

        #Instanciando cada um dos tesouros.
        exclusionZones = [p1.getRect(), p2.getRect(), treasureChest.getRect()]
        treasures = TreasureFactory(exclusionZones).createTreasures()
        exclusionZones.extend(treasure.getRect() for treasure in treasures) # Adiciona os novos tesouros nas zonas de exclusão.

        #Contagem iniciada.
        startTime = pygame.time.get_ticks()

        while self.running:
            dt = self.clock.tick(30)  # 30 FPS
            keyState = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            #Movimentação dos jogadores.
            keys = pygame.key.get_pressed()
            p1.move(keys)
            p2.move(keys)

            # Coletando os tesouros.
            collectedP1 = p1.collect(treasures)
            collectedP2 = p2.collect(treasures)
            
            # Remover tesouros coletados da zona de exclusão.
            for treasure in collectedP1 + collectedP2: exclusionZones.remove(treasure.getRect())

            #Depositar tesouros no baú.
            p1.action(treasureChest, keyState)
            p2.action(treasureChest, keyState)

            # Gerar um novo tesouro dentro de um certo intervalo.
            currentTime = pygame.time.get_ticks()
            if currentTime - self.lastTreasureSpawnTime >= stts.treasureSpawnInterval:
                newTreasures = TreasureFactory(exclusionZones).createTreasures(stts.treasureSpawnAmount)
                treasures.extend(newTreasures)
                exclusionZones.extend(treasure.getRect() for treasure in newTreasures)
                self.lastTreasureSpawnTime = currentTime

            #Desenhando elementos na tela.
            self.win.fill(colors.sand) 
            for treasure in treasures: treasure._draw(self.win)
            drawables = [(treasureChest, treasureChest.getRect().y + treasureChest.getRect().height)] #Vamos ordenar para desenhar com sobreposições.
            drawables.append((p1, p1.getRect().y + p1.getRect().height))
            drawables.append((p2, p2.getRect().y + p2.getRect().height))
            drawables.sort(key=lambda item: item[1]) # Ordenando elementos por posição y + height.
            for drawable, _ in drawables: drawable._draw(self.win) # Desenhando elementos na ordem correta.

            #Calculando tempo restante e desenhando na tela.
            remainingTime = (stts.gameDuration - (pygame.time.get_ticks() - startTime)) // 1000
            timer = Chronometer(remainingTime, "Tempo Restante:", [stts.width - 0.28*stts.width, stts.height - 0.0583*stts.height])
            timer._draw(self.win)

            pygame.display.update()

            if pygame.time.get_ticks() - startTime > stts.gameDuration:
                treasureChest.gameOver.set()
                self.running = False
                print("Fim de jogo! ⌛❌")
                print(f"Tempo de espera total gasto: {round(treasureChest.totalWaitTime, 2)}s ⏲️")
                treasureChest.showScoreboard()
                treasureChest.determineWinner()
        
