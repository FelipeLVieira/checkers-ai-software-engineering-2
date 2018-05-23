# Padrões de implementação para o game loop

## Vez do jogador
Durante a vez do jogador, o game loop deverá:
#### Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre uma peça, determinar a coordenada da peça no tabuleiro
- Se estiver sobre um botão, determinar qual é o botão

#### Capturar cliques do mouse
- Se o usuário clicar sobre uma peça, obter os possíveis movimentos dela para serem exibidos na tela
- Se o usuário clicar sobre um possível movimento, executar o movimento, sinalizá-lo à classe de gráficos para que seja exibida a animação, e aguardar o fim da animação
- Se o usuário clicar sobre um botão, executar a ação correspondente (pausar ou finalizar o jogo)

#### Atualizar a classe de gráficos


## Vez do oponente IA
No momento em que o turno da IA iniciar, o game loop deverá chamar a função de IA para computar a jogada, e aguardar que a IA faça sua jogada.

Durante a vez do oponente, o game loop deverá:
#### Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre uma peça, determinar a coordenada da peça no tabuleiro
- Se estiver sobre um botão, determinar qual é o botão

#### Capturar cliques do mouse
- Se o usuário clicar sobre um botão, executar a ação correspondente (pausar ou finalizar o jogo)

#### Atualizar a classe de gráficos

#### Atualizar o estado da classe de IA, aguardando que ela termine sua jogada
- Caso tenha terminado, fazer o movimento, sinalizá-lo à classe de gráficos para que seja exibida a animação, e aguardar o fim da animação


## Aguardando fim de animação
Durante esse estado, o game loop deverá:

#### Ouvir eventos
- Ouvir os eventos que correspondem a uma peça sumir da tela e responder chamando a função correspondente
- Ouvir o evento que corresponde ao fim da animação e ir para o turno do próximo jogador

#### Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre uma peça, determinar a coordenada da peça no tabuleiro
- Se estiver sobre um botão, determinar qual é o botão

#### Capturar cliques do mouse
- Se o usuário clicar sobre um botão, executar a ação correspondente (pausar ou finalizar o jogo)

#### Atualizar a classe de gráficos


## Jogo pausado
Enquanto o jogo, o game loop deverá:

#### Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre um botão do menu de pause (e apenas do menu de pause), determinar qual é o botão

#### Capturar cliques do mouse
- Se o usuário clicar sobre um botão, executar a ação correspondente (continuar, reiniciar ou finalizar o jogo)

#### Atualizar a classe de gráficos

## Fim do jogo
No momento em que o jogo terminar, o game loop deverá sinalizar isso à classe gráfica, dizendo quem ganhou o jogo para ela mostrar a mensagem correspondente.

Após o jogo ter terminado, o game loop deverá:

#### Capturar a posição do mouse e determinar sobre qual item ele está
- Se estiver sobre um botão, seja da barra lateral ou do menu pop-up que aparece na tela, determinar qual é o botão. O botão de pause não contará.

#### Capturar cliques do mouse
- Se o usuário clicar sobre um botão, executar a ação correspondente (reiniciar ou finalizar o jogo)

#### Atualizar a classe de gráficos
