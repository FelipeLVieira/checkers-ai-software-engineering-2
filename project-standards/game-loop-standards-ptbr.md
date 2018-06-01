# Padrões de implementação para o game loop

A instância do game loop recebe os seguintes parâmetros quando é inicializada:

- Objeto GraphicsBackend - sobre o qual ela deverá instanciar o objeto Graphics para mostrar a tela de jogo
- Nível de dificuldade - um número inteiro de 0 a 4, utilizado pra escolher os parâmetros da IA, que deverão estar em uma lista ou dicionário, indexados para cada nível de dificuldade.
- Nome do jogador - passado à classe Graphics para ser mostrado na tela

No momento que o objeto do GameLoop é inicializado, ele deverá:
- Instanciar um objeto Board
- Instanciar um objeto Graphics, passando como parâmetros o Board e o nome do jogador
- Instanciar um objeto AIPlayer, passando como parâmetros os atributos de dificuldade para o nível de dificuldade escolhido

O game loop em si só começará a ser executado no momento em que a classe Title chamar a função principal do GameLoop, e ele terminará (retornará) quando o usuário encerrar um jogo, tendo ele terminado ou não.

## Vez do jogador
Durante a vez do jogador, o game loop deverá:
#### - Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre uma peça, determinar a coordenada da peça no tabuleiro
- Se estiver sobre um botão, determinar qual é o botão

#### - Capturar cliques do mouse
- Se o usuário clicar sobre uma peça, obter os possíveis movimentos dela para serem exibidos na tela.

> Se não houverem possíveis movimentos para aquela peça, obter da Board a lista de quais peças têm possíveis movimentos e passar para a classe de Gráficos executando a função correspondente (`showPiecesWithLegalMoves`).

- Se o usuário clicar sobre um possível movimento: 

> 1. Executar o movimento
> 2. Receber a resposta da função de movimentação, para que ela diga se a jogada está completa ou não
> 3. Sinalizar o movimento à classe de gráficos para que seja exibida a animação
> 4. Aguardar o fim da animação para então pedir que o jogador complete o movimento, se ele estiver incompleto... ou passar a vez à IA se ele estiver completo.

- Se o usuário clicar sobre um botão, executar a ação correspondente (pausar ou finalizar o jogo)

#### - Atualizar a classe de gráficos


## Vez do oponente IA
No momento em que o turno da IA iniciar, o game loop deverá chamar a função de IA para computar a jogada, e aguardar que a IA faça sua jogada.

Durante a vez do oponente, o game loop deverá:
#### - Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre uma peça, determinar a coordenada da peça no tabuleiro
- Se estiver sobre um botão, determinar qual é o botão

#### - Capturar cliques do mouse
- Se o usuário clicar sobre um botão, executar a ação correspondente (pausar ou finalizar o jogo)

#### - Atualizar a classe de gráficos

#### - Atualizar o estado da classe de IA, aguardando que ela termine sua jogada
- Caso tenha terminado, fazer o movimento, sinalizá-lo à classe de gráficos para que seja exibida a animação, e aguardar o fim da animação


## Aguardando fim de animação
Durante esse estado, o game loop deverá:

#### - Ouvir eventos
- Ouvir os eventos que correspondem a uma peça sumir da tela e responder chamando a função correspondente
- Ouvir o evento que corresponde ao fim da animação e verificar se a jogada está completa; se estiver, ir para a vez do outro jogador, e se não, pedir que o jogador complete o movimento mostrando os possíveis movimentos

#### - Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre uma peça, determinar a coordenada da peça no tabuleiro
- Se estiver sobre um botão, determinar qual é o botão

#### - Capturar cliques do mouse
- Se o usuário clicar sobre um botão, executar a ação correspondente (pausar ou finalizar o jogo)

#### - Atualizar a classe de gráficos


## Jogo pausado
Enquanto o jogo, o game loop deverá:

#### - Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre um botão do menu de pause (e apenas do menu de pause), determinar qual é o botão

#### - Capturar cliques do mouse
- Se o usuário clicar sobre um botão, executar a ação correspondente (continuar, reiniciar ou finalizar o jogo)

#### - Atualizar a classe de gráficos

## Fim do jogo
No momento em que o jogo terminar, o game loop deverá sinalizar isso à classe gráfica, dizendo quem ganhou o jogo para ela mostrar a mensagem correspondente.

Após o jogo ter terminado, o game loop deverá:

#### - Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre um botão, seja da barra lateral ou do menu pop-up que aparece na tela, determinar qual é o botão. O botão de pause não contará.

#### - Capturar cliques do mouse
- Se o usuário clicar sobre um botão, executar a ação correspondente (reiniciar ou finalizar o jogo)

#### - Atualizar a classe de gráficos
