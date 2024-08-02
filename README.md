# 🏴‍☠️ Tesouro Pirata 🏴‍☠️
Tesouro Pirata é um jogo divertido onde os jogadores controlam piratas que coletam tesouros e os depositam em um baú da tripulação que é compartilhado. O objetivo é coletar o máximo de tesouros possível antes que o tempo acabe. O jogador com mais pontos vence!

## Funcionalidades
* Movimentação do Jogador: Controle ambos os piratas usando o mesmo teclado.
* Coleta de Tesouros: Pegue os tesouros espalhados pelo mapa.
* Depósito no Baú: Deposite os tesouros coletados no baú compartilhado.
* Sistema de Animação: Animações suaves para movimentos dos piratas.
* Surgimento Tesouros: Novos tesouros vão surgindo ao longo da partida em posições aleatórias.

## ⚙️ Mecânicas do Jogo
### Coleta de Tesouros
Cada jogador pode carregar até 3 tesouros na mochila. Para coletar um tesouro, basta se mover sobre ele. Os tesouros aparecem aleatoriamente pelo mapa e podem ser de três tipos:
- 🥉 Bronze: 1 ponto
- 🥈 Prata: 3 pontos
- 🥇 Ouro: 5 pontos

### Depósito no Baú
O baú compartilhado está no centro do mapa. Para depositar tesouros, mova-se até o baú e pressione a tecla de ação (F para Jogador 1, 0 para Jogador 2). Porém existe algumas coisas que o jogador precisa levar em conta:
- Se o baú estiver disponível, o jogador pode depositar os seus tesouros, caso ele tenha coletado algum, e ganhar os pontos. ✅
- Se o baú estiver em uso, o jogador precisa esperar até que ele esteja disponível. ⛔

### Região Crítica e Condição de Corrida
O baú de tesouros da tripulação é uma região crítica onde apenas um pirata pode acessar por vez. Para evitar condições de corrida, utilizei o padrão Strategy para implementar diferentes mecanismos de sincronização de processos. Os mecanismos de sincronização atualmente disponíveis são: Semaphore e Lock. Dependendo da configuração, o comportamento da sincronização varia:
* Semaphore: 
    Foi utilizado threading.Condition para implementar um semáforo que controla o acesso ao baú. Se um pirata tentar acessar o baú enquanto ele está em uso, ele precisa esperar até que o semáforo seja liberado. Seus movimentos ficam bloqueados até que sua vez chegue.
*Lock:
    Neste caso foi utilizado o threading.Lock para garantir que apenas um pirata possa acessar o baú por vez. Se o pirata não conseguir adquirir o lock, ele imprime uma mensagem informando que o baú está ocupado e ele é livre para se movimentar e tentar novamente em um outro momento.
Você pode alterar o comportamento de sincronização através do arquivo `consts/settings.py`, que seleciona a estratégia apropriada com base nas configurações fornecidas. Abaixo você pode visualizar a implementação dos mecanismo de sincronização utilizados nesse projeto até o momento. As classes estão disponíveis em `strategies/synchronizations/`.

```python
class Semaphore():
    def __init__(self, value = 1):
        self.value = value # Determina o número máximo de threads que podem acessar a seção crítica simultaneamente.
        self.condition = threading.Condition()
    
    def down(self):
        with self.condition: # Método para uma thread esperar para entrar na seção crítica.
            while self.value <= 0: self.condition.wait() # Se o valor for 0 ou menor, a thread espera.
            self.value -= 1 # Decrementa o valor e permite que a thread prossiga.
    
    def up(self):
        with self.condition:  # Método para uma thread sinalizar que está saindo da seção crítica
            self.value += 1  # Incrementa o valor e notifica uma das threads que estão esperando
            self.condition.notify()

class Lock():
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self, timeout=0.5):
        return self.lock.acquire(timeout=timeout) # O timeout é o tempo máximo em segundos para tentar adquirir o lock.

    def release(self):
        self.lock.release() # Libera o lock adquirido.
```
Cada Thread chama a mesma função dentro da classe Pirate, mas a função em si pode variar de acordo com a solução escolhida durante a execução do código. A ideia por trás dessa abordagem é facilitar a manutenção e a extensão do código a medida que novas implementações de solução para a condição de corrida são adicionadas. Consulte `models/Pirate.py` para mais detalhes.

```python

    class Pirate(ISpritesAnimatorGenerator):
    
    def __init__(self, id, position, pngSprites, jsonSheet=Path("assets/pirate/pirateSpritesSheet.json"), size=stts.playerSize, state='idle', frame=0):
    # Outras inicializações...
    self.depositStrategy = SynchMechanismFactory().createDeposityStrategy()

    # Restante do código...

    def _depositTreasure(self, SharedChest): self.depositStrategy.deposit(self, SharedChest)

    def action(self, SharedChest, keyState):
        playerRect, chestRect = self.getRect(), SharedChest.getRect()
        if playerRect.colliderect(chestRect):
            if keyState[self.control.action] and not self.cannotMove:
                self.cannotMove = True
                threading.Thread(target=self._depositTreasure, args=(SharedChest, )).start()
```
A fábrica é a classe que vai definir qual função será chamada para depositar os tesouros e qual o mecanismo de sincronização foi adotado, permitindo adquirir ou liberar a região crítica. Veja o código completo em `factories/SynchMechanismFactory.py`.
```python
class SynchMechanismFactory:

    def __init__(self, mechanism=stts.synchMenchanism.lower()): self.mechanism = mechanism

    def createSynchMechanism(self):
        if self.mechanism == "semaphore":  return Semaphore()
        elif self.mechanism == "lock": return Lock()
        else: raise ValueError(f"Mecanismo de sincronização de processos inválido: {self.mechanism}")

    def createDeposityStrategy(self) ->  IDepositStrategy:
        if self.mechanism == "semaphore":  return SemaphoreDeposit()
        elif self.mechanism == "lock": return LockDeposit()
        else: raise ValueError(f"Mecanismo de sincronização de processos inválido: {self.mechanism}")
```

## ⌨️ Controles
* Jogador 1:
    - Movimento: W, A, S, D
    - Ação: F
* Jogador 2:
    - Movimento: Setas do teclado
    - Ação: Tecla 0 (numérica)

## 📸 Screenshots
<p align="center">
  <img src="assets/screenshots/screenshot-02.png" alt="Screenshot 1" width="800">
  <img src="assets/screenshots/screenshot-01.png" alt="Screenshot 2" width="800">
  <img src="assets/screenshots/screenshot-03.gif" alt="Screenshot 3" width="800">
  <img src="assets/screenshots/screenshot-04.png" alt="Screenshot 4" width="800">
</p>

## 🚀 Como rodar Tesouro Pirata na sua máquina.
Siga estas etapas para configurar e executar o projeto localmente.

### Pré-requisitos
- Python 3.8+
- Pygame

## Instalação
1. Instale a biblioteca pygame, para mais informações consulte o [Pypi do Pygame](https://pypi.org/project/pygame/).
```sh
pip install pygame
```

2. Clone e navegue até diretório do repositório.
```sh
git clone https://github.com/DavidOSilva/TesouroPirata
cd TesouroPirata
```

3. Executando o Jogo. O jogo será iniciado e a janela do Pygame será aberta.
```sh
python main.py
```

## 🎛️ Alterar configurações do Jogo.
Como já foi mencionado, você pode acessar o arquivo `consts/settings.py` e fazer algumas alterações, como: tempo da partida, número de tesouros gerados, tempo de geração dos tesouros, velocidade do jogador, capacidade da mochila, tamanho da tela etc.
```python
class Settings:
    def __init__(self):
        self.width = 1000
        self.height = int(self.width*0.5575)
        self.gameDuration = 60 * 1000
        self.margin = 20
        self.synchMenchanism = "lock"

        self.playerSpeed = 7
        self.playerSize = [52, 75]
        self.playerBackpackCapacity = 3
        self.playerAnimationFrameRate = 10

        self.treasureSize = [30, 34]
        self.treasureValues = [1, 3, 5]
        self.treasureProbas = [0.5, 0.35, 0.15]
        self.treasureNumMax = 15
        self.treasureSpawnInterval = 4 * 1000 
        self.treasureSpawnAmount = 2

        self.sharedChestSize = [54, 54]
        self.sharedChestPosition = self.width // 2 - self.sharedChestSize[0] // 2, self.height // 2 - self.sharedChestSize[1] // 2
        self.depositDuration = 1.2 * 1000
```

## 🗂️ Estrutura do Projeto
* `main.py`: Arquivo principal para iniciar o jogo.
* `models/`: Contém as classes principais do jogo, como Pirate, SharedChest e Treasure.
* `interfaces/`: Contém as interfaces usadas no projeto.
* `consts/`: Contém constantes e configurações do jogo.
* `assets/`: Contém imagens e outros recursos do jogo.
* `factories/`: Contém as fábricas que criam instâncias de estratégias e mecanismos de sincronização.
* `strategies/`: Contém as implementações das estratégias de depósito.
* `synchronizations/`: Contém as funções que serão chamadas pela Thread dependendo de qual abordagem foi escolhida.

## 📜 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

## 📬 Contato
David Oliveira Silva - @DavidOSilva - davidoliveirasilvaa@gmail.com

Link do Projeto: https://github.com/DavidOSilva/TesouroPirata