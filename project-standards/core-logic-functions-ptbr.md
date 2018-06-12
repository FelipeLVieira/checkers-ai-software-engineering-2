# Algoritmos utilizados no núcleo de lógica do jogo

## Lógica do método getLegalMoves


Recupera todos os movimentos possíveis do jogador através do método "getAllLegalMoves".
São cacheados todos os movimentos gerados.
Em seguida, são filtrados os melhores movimentos para a peça selecionada através do método
"getBestMoves", aplicando também a "Lei da Maioria".
São retornados os movimentos filtrados para o GameLoop, bem como permanecem cacheados para uso posterior.

## Lógica do método getAllLegalMoves

Varre o tabuleiro pegando todos os movimentos possíveis de todas as peças do turno atual do jogador no tabuleiro

## Lógica do método getLegalMovesByPiece

É feito um loop em todo o tabuleiro procurando as peças do turno do jogador atual e aplicado
a função "theoreticalLegalMoves".
Em seguida é aplicada a função "moveRank" para rankear os melhores movimentos daquela lista gerada.
São retornados todos os movimentos de uma peça e concatenados nos movimentos das outras peças

## Lógica do método theoreticalLegalMoves

Checa todos os movimentos válidos com e sem capturas, chamando a função "possibleCaptures" para
verificar recursivamente as possíveis capturas.
Caso a peça seja uma dama, chama o método "theoreticalKingLegalMoves".

## Lógica do método theoreticalKingLegalMoves

Retorna todas as jogadas válidas de uma peça de dama.