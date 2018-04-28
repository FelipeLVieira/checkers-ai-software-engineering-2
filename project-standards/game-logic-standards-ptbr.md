# Padrões de projeto para implementação das regras do jogo

## Abstração do jogador

Para o núcleo de lógica do jogo, **não interessa** quem é que está jogando. Ele apenas age como um mediador para o jogo, recebendo requisições e respondendo a elas.

O jogador interage com o núcleo da seguinte forma:

1. O jogador é notificado, através de um evento do Pygame, que é sua vez de jogar, imediatamente solicitando a última jogada realizada pelo outro jogador e a lista de possíveis jogadas para todas as peças
2. O jogador realiza sua jogada
3. Se a jogada for válida, o jogador recebe a confirmação de que sua jogada foi validada e fica aguardando o outro jogador efetuar sua jogada; se a sua jogada tiver sido inválida, ele retorna ao passo 2

## Função para retornar as possíveis movimentações para todas as peças

Para verificar as possíveis jogadas para uma peça, é necessário que a função verifique as possíveis jogadas para todas as peças, pois pode haver uma peça para a qual há a possibilidade de capturar mais peças do que uma certa peça para a qual se deseja saber as possíveis jogadas. Logo, não faz sentido muito sentido uma função para solicitar as movimentações para apenas uma peça - o jogador pode fazer o trabalho de escolher qual peça irá movimentar.

Isso não significa que todas as jogadas serão mostradas ao mesmo tempo - a interface não precisa mostrar tudo ao mesmo tempo o tempo todo; por hora será implementado para que a interface mostre apenas as possibilidades para uma peça clicada pelo jogador, e depois será decidido como a interface irá lidar com isso.

- A função recebe o objeto do "jogador" para saber quais peças deve verificar
- A função computa, para todas as peças, todas as possíveis jogadas, e adiciona em uma lista as jogadas válidas
- Caso haja possibilidade de se capturar peças, a função só deixa na lista as jogadas com o maior número de peças capturadas
- A função armazena a lista de possíveis jogadas internamente para utilizá-la para validar a jogada no momento que o jogador solicitar
- A função retorna a lista de possibilidades ao jogador.

## Função para validar e realizar uma jogada

- A função recebe o objeto "jogador", o tabuleiro atual (pode estar dentro da própria classe), e a jogada que se deseja realizar
- A função verifica se a jogada está dentre a lista de possíveis movimentações (essa lista tem que ter sido definida antes, se não tiver, a função levanta uma exceção do tipo RuntimeError)

Caso a jogada seja possível:
- A lista de possíveis movimentações é limpa
- A jogada é realizada no tabuleiro
- O jogo verifica se há uma condição de vitória ou empate; se sim, os jogadores recebem a notificação disso.
- Caso contrário, o outro jogador é notificado de que é sua vez de jogar;
- A função retorna um resultado positivo.

Caso a jogada não seja possível, a função retorna um resultado negativo.

## Função para verificar se há uma condição de vitória

- A função verifica se algum dos jogadores está sem peças; se estiver, há uma condição de derrota para este jogador e uma condição de vitória para o outro jogador; a função dispara então um evento notificando essa condição.
- Caso contrário, a função aplica as regras do jogo de damas para saber se houve empate, e dispara um evento notificando os jogadores caso isso se proceder.
- Caso contrário, a função retorna o controle para que o jogo prossiga.
