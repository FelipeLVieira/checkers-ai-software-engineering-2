# Padrões para a interface lógica das classes de UI in-game

## Classe para controlar o desenho do tabuleiro na tela

Esta classe é responsável por:

- A cada frame redesenhar o tabuleiro e os highlights, e caso o jogo não esteja pausado (isso deve ser passado como parâmetro), atualizar animações e highlights.
- Quando um movimento for realizado, disparar a animação correspondente
- Se uma peça for comida, marcá-la para remoção no trigger e disparar a animação com o trigger para removê-la da tela
- Ao receber o trigger para remover uma peça da tela, removê-la de fato (isso terá sua própria função, o GameLoop é responsável por chamar ela quando receber o evento correspondente)

### Função de update principal
Esta função recebe os seguintes parâmetros:
- Lista de possíveis movimentos a serem mostrados, se houverem
- Coordenada do tabuleiro sobre a qual o mouse está, se estiver (para o highlight de hover)
- Peça que está selecionada, se houver (para highlighting)
- Botão sobre o qual o mouse está posicionado
- Se o jogo está pausado ou não
- Se é a vez do jogador ou não

Ela chama a classe de timing do pygame, atualiza os elementos necessários, desenha a tela de jogo, e retorna o valor do timeDelta, que deve ser capturado para uso na função de IA que precisa dele para timing.

### Highlights
Há alguns tipos de highlights que a classe deve lidar:
- Highlighting de hover - quando o mouse está sobre uma peça ou um nó de um possível caminho, aquele elemento deve ser desenhado com um highlight.
- Highlighting de possíveis caminhos - quando uma peça é selecionada, os possíveis caminhos devem ser mostrados utilizando a animação de pop-in do highlight de movimento. Cada vez que um possível caminho é adicionado, a animação e as coordenadas correspondentes são armazenadas em uma lista, e os elementos lá dentro são atualizados e desenhados todo frame.

### Animação de movimento de peças
Quando ocorre um movimento, a classe deverá receber:
- O tabuleiro resultante
- As coordenadas do movimento
- Aonde as peças são comidas (coordenadas), caso houver

A classe irá então construir um caminho de movimento, incluindo os triggers para a remoção visual das peças, e disparar a animação (adicionando-a em uma lista). O tabuleiro recebido pela função é armazenado, e o tabuleiro interno da classe só é atualizado ao fim da animação.

O game loop não deverá permitir que o usuário ou a IA joguem enquanto a animação está em progresso.

O game loop deverá capturar os eventos pygame.USEREVENT referentes aos triggers que são disparados e executar as funções correspondentes para que haja atualização na tela.

### Turnos
A classe deverá exibir, como registrado no mockup, o número do turno atual no scoreboard.

Ela também deverá exibir qual jogador está jogando no momento; isso será feito exibindo o texto "Aguarde..." no lugar do número do turno enquanto a IA estiver jogando.

### Nomes dos jogadores
O nome do jogador é definido no momento em que a classe é inicializada. Enquanto a tela de título não é implementada, será usado o valor padrão "Jogador" na inicialização.
