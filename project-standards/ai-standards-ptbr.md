# Padrões de projeto para a inteligência artificial

## Algoritmo Minimax com poda alpha-beta

A função leva como parâmetros:
- O tabuleiro atual
- A profundidade de busca que se deseja fazer (o quanto quer-se olhar no futuro)
- A cor das peças da IA
- Um "ponteiro de retorno" - uma lista vazia aonde será adicionado o movimento determinado pela IA; este não é retornado pelo fato da função rodar em uma thread separada.

A função Minimax é o algoritmo recursivo básico da IA que é usado para determinar qual jogada será feita. Como o algoritmo pode levar um tempo para executar, para impedir que o executável do jogo fique irresponsivo durante os cálculos da IA, ela é executada de forma assíncrona, numa thread separada.

Há quatro hiperparâmetros que podem ser ajustados para modificar a "inteligência" da IA:
- Profundidade
- Tabela de "teimosia" (stubbornnessTable) - para cada profundidade na árvore de chamadas, há uma chance de a IA "não perceber" um possível movimento. Essa tabela define essa chance para cada valor de profundidade - é necessário notar que a profundidade é endereçada de forma decrescente, sendo 0 a chamada mais profunda e (profundidade - 1) a chamada pai.
- Viés aleatório - a cada valor computado para um movimento, será adicionado um viés aleatório com essa magnitude. Isso tem tanto o propósito de aleatoriezar as escolhas de caminhos de mesmo valor, quanto de tornar a IA mais estocástica. Note que o viés se acumula dos ramos mais profundos até a base da árvore.
- Função de heurística - Uma função de heurística diferente altera a percepção da IA sobre um determinado estado de jogo.

Dentro do algoritmo, a função requer acesso a:
- Instanciar novos objetos Board a partir de objetos existentes
- Requerir os movimentos possíveis para todas as suas peças
- Executar movimentos no tabuleiro (no caso, em tabuleiros instanciados pela função a partir do tabuleiro passado como parâmetro)

## Heurística base desenvolvida

A heurística atualmente implementada na função heuristic é uma heurística que leva em conta tanto a diferença do número de peças da IA e do seu oponente, quanto a razão entre elas. Assim, a IA tende a se sentir mais "intimidada" por uma peça sua sendo comida conforme o jogo progride e o número de peças diminui.

## Classe "jogador IA"

A classe do jogador da IA é uma classe simples feita para lidar com a thread de minimax.

Ela tem as seguintes funções relevantes:
- Jogar: Recebe um tabuleiro e inicia a thread de minimax, se ela já não estiver rodando. Retorna um erro se estiver.
- Update: Deve ser chamada todo frame, após a jogada ser iniciada, até que retorne resultado. Recebe a diferença de tempo entre o update anterior e o atual; checa se a thread completou, e caso a thread já tenha completado, retorna o resultado se o "tempo mínimo de pensamento" já passou.

Os parâmetros desta classe são a cor das peças da IA, o tempo mínimo de pensamento em segundos, e opcionalmente os hiperparâmetros do Minimax.
