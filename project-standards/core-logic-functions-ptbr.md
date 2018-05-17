# Algoritmos utilizados no núcleo de lógica do jogo

## Lógica do método getLegalMoves

Método que varre o tabuleiro procurando pelas peças do turno do jogador e chamando
o método **getLegalMovesByPiece** para juntar todas as possíveis jogadas de todas as peças
em um só vetor

Em seguida, devem ser podados os movimentos que mais pulam peças, a fim de aplicar a
"Lei da Maioria" do jogo.

O vetor então com todos os possíveis melhores movimentos é retornado ao **GameLoop.py**

## Lógica do método getLegalMovesByPiece

Inicia chamando o método **getRegularMovesByPiece**, solicitando os movimentos simples da peça, 
sendo ela peça normal ou dama, caso houverem.

Em seguida, é chamado o método **getJumpsByPiece**, onde são passados os movimentos simples para
detectar se existem pulos (no caso de dama) e se existem peças para serem puladas ao redor da peça
(normal ou dama).

Por fim, os movimentos detectados para a peça são retornados

## Lógica do método getJumpsByPiece

- O método inicia o algoritmo verificando se a peça pode pular para as quatro direções.
- Para cada direção que a peça puder pular, é duplicado o movimento inicial (copy.deepcopy(move)),
são adicionadas as duas coordenadas de pulo (a coordenada da peça que será pulada 
e a coordenada após a peça pular) e o movimento então é colocado na fila (moveQueue)
- De posse dos movimentos potenciais em pular mais, é iniciado um while que irá funcionar
enquanto houverem movimentos a serem expandidos na fila. Os movimentos que não puderem
ser expandidos são adicionados na lista de retorno para o **getLegalMovesByPiece**

## getRegularMovesByPiece

- Verifica se a peça pode movimentar para frente um quadrado quando for peça normal
- Verifica até onde a peça pode caminhar sem ser interrompida, no caso de dama

## getBestMoves

- Verifica quais são os melhores movimentos para uma peça com base no retorno do **getLegalMoves**, caso houver