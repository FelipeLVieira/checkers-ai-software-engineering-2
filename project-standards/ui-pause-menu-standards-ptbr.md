# Padrão de implementação para o menu de pause

O menu de pause será implementado como uma classe simples. Ela cumpre os seguintes papéis:
- Desenhar o menu de pause, incluindo os textos atrelados, por cima da tela de jogo
- Desenhar os highlights sobre o botão aonde o mouse está posicionado

A captura de inputs dos botões e as ações a eles atreladas serão feitas pelo game loop, que é responsável por não realizar updates na classe de IA e sinalizar à classe de UI de jogo para não atualizar animações. O game loop também é responsável por não capturar inputs relacionados a cliques sobre peças.

O menu de pause tem as seguintes funções:
- Desenhar
- Atualizar: Recebe como argumento se o mouse está posicionado sobre algum dos botões, para poder posicionar o highlight sobre ele
