import json
import pygame
import sys

def forca():
    pygame.init()

    # Set up the display
    size = (400, 400)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Jogo da Forca")

    # Load the Hangman images
    hangman_imgs = []
    for i in range(7):
        img = pygame.image.load(f"hangman{i}.png")
        hangman_imgs.append(img)

    # Set up the font
    font = pygame.font.SysFont(None, 48)

    # Set up the game variables
    word = "hangman"
    guessed_word = "_" * len(word)
    incorrect_guesses = 0

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the screen
        screen.fill((255, 255, 255))
        
        # Draw the Hangman figure
        screen.blit(hangman_imgs[incorrect_guesses], (0, 0))
        
        # Draw the word to be guessed
        text = font.render(guessed_word, True, (0, 0, 0))

        screen.blit(text, (size[0]//2 - text.get_width()//2, size[1]//2 + hangman_imgs[0].get_height() // 2))

        # Check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    # Check if the letter is in the word
                    if event.unicode in word:
                        for i, letter in enumerate(word):
                            if letter == event.unicode:
                                guessed_word = guessed_word[:i] + letter + guessed_word[i+1:]
                    else:
                        incorrect_guesses += 1

        # Check if the game is over
        if guessed_word == word:
            text = font.render("You win!", True, (0, 255, 0))
            screen.blit(text, (size[0]//2 - text.get_width()//2, size[1]//2 + 50))
            running = False
        elif incorrect_guesses == len(hangman_imgs)-1:
            text = font.render("You lose!", True, (255, 0, 0))
            screen.blit(text, (size[0]//2 - text.get_width()//2, size[1]//2 + 50))
            running = False

        # Update the display
        pygame.display.update()

    pygame.quit()

def galo():
    pygame.init()

    pygame.display.set_caption("Jogo do Galo")

    grid_width, grid_height = 3, 3
    square_size = 160

    screen_width = grid_width * square_size
    screen_height = grid_height * square_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # Define symbols
    symbol_size = int(square_size * 0.8)
    symbol_thickness = int(square_size * 0.1)

    cross = pygame.Surface((symbol_size, symbol_size), pygame.SRCALPHA)
    pygame.draw.line(cross, (255, 0, 0), (symbol_thickness, symbol_thickness), (symbol_size - symbol_thickness, symbol_size - symbol_thickness), symbol_thickness)
    pygame.draw.line(cross, (255, 0, 0), (symbol_thickness, symbol_size - symbol_thickness), (symbol_size - symbol_thickness, symbol_thickness), symbol_thickness)

    circle = pygame.Surface((symbol_size, symbol_size), pygame.SRCALPHA)
    pygame.draw.circle(circle, (0, 0, 255), (symbol_size // 2, symbol_size // 2), symbol_size // 2 - symbol_thickness // 2, symbol_thickness)

    # Initialize game variables
    board = [[None] * grid_width for _ in range(grid_height)]
    current_player = 0
    players = [cross, circle]

    running = True

    # Check for a winning configuration
    def check_win():
        # Check rows
        for row in range(grid_height):
            if all(board[row][col] == current_player for col in range(grid_width)):
                return 'row', ((row, 0), (row, grid_width - 1))

        # Check columns
        for col in range(grid_width):
            if all(board[row][col] == current_player for row in range(grid_height)):
                return 'col', ((0, col), (grid_height - 1, col))

        # Check diagonals
        if all(board[i][i] == current_player for i in range(grid_height)):
            return 'diag', ((0, 0), (grid_height - 1, grid_width - 1))

        if all(board[i][grid_width - 1 - i] == current_player for i in range(grid_height)):
            return 'rev_diag', ((0, grid_width - 1), (grid_height - 1, 0))

        return None, None
    
    win_coords = None

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = event.pos[1] // square_size, event.pos[0] // square_size
                if board[row][col] is None:
                    board[row][col] = current_player
                    win_type, win_coords = check_win()
                    if win_coords is not None:

                        # Create a new window to display the winning message
                        win_message = f"Player {current_player + 1} wins!"
                        print(win_message)
                        running = False
                    
                    current_player = (current_player + 1) % 2

        # Draw the grid
        for row in range(grid_height):
            for col in range(grid_width):
                square = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
                pygame.draw.rect(screen, (255, 255, 255), square)
                pygame.draw.rect(screen, (0, 0, 0), square, 3)

                # Draw symbols
                if board[row][col] is not None:
                    screen.blit(players[board[row][col]], square.move(square_size // 10, square_size // 10))

        # Draw the winning line
        if win_coords is not None:
            #line_color = (255, 0, 0) if win_coords == 'blue' else (0, 0, 255)
            line_color = 'yellow'
            if win_type == 'row':
                y = win_coords[0][0] * square_size + square_size // 2
                pygame.draw.line(screen, line_color, (0, y), (screen_width, y), 5)
            elif win_type == 'col':
                x = win_coords[0][1] * square_size + square_size // 2
                pygame.draw.line(screen, line_color, (x, 0), (x, screen_height), 5)
            elif win_type == 'diag':
                pygame.draw.line(screen, line_color, (0, 0), (screen_width, screen_height), 5)
            elif win_type == 'rev_diag':
                pygame.draw.line(screen, line_color, (0, screen_height), (screen_width, 0), 5)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

def damas():
    pygame.init()

    pygame.display.set_caption("Jogo das Damas")

    grid_width, grid_height = 8, 8
    square_size = 80
    piece_size = int(square_size * 0.9)

    # Define the colors
    light_color = (255, 206, 158)
    dark_color = (209, 139, 71)
    selected_color = (255, 255, 0)

    # Define the board
    board = [['', 'w', '', 'w', '', 'w', '', 'w'],
             ['w', '', 'w', '', 'w', '', 'w', ''],
             ['', 'w', '', 'w', '', 'w', '', 'w'],
             ['', '', '', '', '', '', '', ''],
             ['', '', '', '', '', '', '', ''],
             ['b', '', 'b', '', 'b', '', 'b', ''],
             ['', 'b', '', 'b', '', 'b', '', 'b'],
             ['b', '', 'b', '', 'b', '', 'b', '']]

    # Define the pieces
    pieces = []
    for row in range(grid_height):
        for col in range(grid_width):
            if board[row][col] == 'w':
                pieces.append({'x': col, 'y': row, 'color': (255, 255, 255)})
            elif board[row][col] == 'b':
                pieces.append({'x': col, 'y': row, 'color': (0, 0, 0)})

    screen_width = grid_width * square_size
    screen_height = grid_height * square_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    running = True

    # Define the selected piece
    piece_selected = False
    selected_piece = {}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // square_size
                row = mouse_y // square_size
                if not piece_selected:
                    # Select the piece if there is one at the mouse position
                    for piece in pieces:
                        if piece['x'] == col and piece['y'] == row:
                            piece_selected = True
                            selected_piece = piece
                            break
                else:
                    # Otherwise, move the selected piece to the mouse position
                    destination_piece = None
                    for piece in pieces:
                        if piece['x'] == col and piece['y'] == row:
                            destination_piece = piece
                            break
                    selected_piece['x'] = col
                    selected_piece['y'] = row
                    # Check if the selected piece overlaps a piece of the opposite color
                    for piece in pieces:
                        if piece != selected_piece and piece['x'] == col and piece['y'] == row:
                            pieces.remove(piece)
                            break
                    piece_selected = False

        screen.fill((255, 255, 255))

        # Update the position of the selected piece if it is selected
        if piece_selected:
            mouse_pos = pygame.mouse.get_pos()
            selected_piece['x'] = mouse_pos[0] // square_size
            selected_piece['y'] = mouse_pos[1] // square_size

        
        # Draw the checkerboard
        for row in range(grid_height):
            for col in range(grid_width):
                square_rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, light_color, square_rect)
                else:
                    pygame.draw.rect(screen, dark_color, square_rect)

        # Draw the pieces on the board
        for piece in pieces:
            piece_rect = pygame.Rect(piece['x'] * square_size, piece['y'] * square_size, piece_size, piece_size)
            pygame.draw.ellipse(screen, piece['color'], piece_rect)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

def conversor_js_py():

    print("\nACABOU DE ENTRAR NO CONVERSOR DE DADOS ENTRE JS E PY\n")

    options = {
        '1': 'Conversor de json para python',
        '2': 'Conversor de python para json'
    }

    for key, value in options.items():
        print(f"{key} - {value}")

    choice = input('\nEscolha o que pretende fazer: ') 

    if choice == '1':
        print("\nACABOU DE ENTRAR NO CONVERSOR DE JSON PARA PYTHON\n")

        x =  '{ "name":"Diogo", "age":23, "height":"193cm", "city":"Évora", "country":"Portugal" }'

        y = json.loads(x)
        
        print(y)
    elif choice == '2':
        print("\nACABOU DE ENTRAR NO CONVERSOR DE PYTHON PARA JSON\n")

        x = {
            "name": "Diogo",
            "age": 23,
            "height": "193cm",
            "city": "Évora",
            "country": "Portugal"
        }

        y = json.dumps(x)

        print(x)
    else:
        print("Erro na conversão.")

def list_options():

    print('\n ACABOU DE ENTRAR NO OPERADOR DE LISTAS\n')\

    lista = ["maçã","pera","ananás","kiwi","pêssego"]

    opções = {
        '1': 'Listar elementos',
        '2': 'Adicionar elementos',
        '3': 'Remover elementos',
        '4': 'Limpar lista'
    }

    for key, value in opções.items():
        print(f"{key} - {value}")

    choice = input('\nEscolha o que pretende fazer: ')

    if choice == '1':
        [print(x) for x in lista]
    elif choice == '2':
        fruta_inserir = input('\nNome do elemento a inserir na lista: ')
        if fruta_inserir not in lista:
            lista.append(fruta_inserir)
        else:
            print('Já pertence à lista')
        print('Após inserção de elemento {}'.format(lista))
    elif choice == '3':
        fruta_remover = input('\nNome do elemento a remover da lista: ')
        if fruta_remover in lista:
            lista.remove(fruta_remover)
        else:
            print('Não pertence à lista')
        print('Após remoção de elemento {}'.format(lista))
    elif choice == '4':
        if len(lista) != 0:
            lista.clear()
        else:
            print('A lista já está vazia')
        print(lista)
    else:
        print('Problemas com a lista')
        
def character_counter():
    print('\nACABOU DE ENTRAR NO CONTADOR DE OCORRÊNCIAS DE CARACTERES\n')

    x = input('Escreva aqui o seu caracter: ')
    text = input('Escreva aqui a sua frase/texto: ')

    if x in text:
        contador = text.count(x)
        print('O caracter ' '"' + x + '"' ' aparece ' + str(contador) + 'x' + ' na frase: ' + text)
    else:
        print('O caracter ' '"'+ x +'"'  ' não aparece qualquer vez na frase: ' + text)

def word_finder():

    print('\nACABOU DE ENTRAR NO WORD FINDER... \n')

    x = input('Escreva a palavra a procurar: ')
    text = input('Escreva aqui a sua frase/texto: ')

    if x in text:
        print('A palavra ' + x + ' está contida na frase: ' + text + '.')
    elif x not in text:
        print('A palavra ' + x + ' não está contida na frase: ' + text + '.')
    else:
        print('Indefinição na escolha da palavra/frase')

def word_comparator():

    print('\nACABOU DE ENTRAR NO COMPARADOR ORTOGRÁFICO... \n')

    x = input('Escreva a sua primeira palavra: ')
    y = input('Escreva a sua segunda palavra: ')

    if x == y:
        print('\nAs palavras são iguais!!!')
    elif x != y:
        print('\nAs palavras são diferentes!!!')
    else:
        print('\nIndefinição na comparação de palavras...')

def number_comparator():

    print('\nACABOU DE ENTRAR NO COMPARADOR NUMÉRICO... \n')

    x = float(input('Digite o valor de x: '))
    y = float(input('Digite o valor de y: '))

    if x > y:
        print('x é maior que y')
    elif x >= y:
        print('x é maior ou igual a y')
    elif x < y:
        print('x é menor que y')
    elif x <= y:
        print('x é menor ou igual a y')
    elif x != y:
        print('x é diferente de y')
    else:
        print('indefinição entre x e y')

def calculator():

    print('\nACABOU DE ENTRAR NA CALCULADORA... \n')

    operations = {
        '+': 'Adição',
        '-': 'Subtração',
        '*': 'Multiplicação',
        '/': 'Divisão',
        '%': 'Módulo',
        '**': 'Exponencial',
        '//': 'Divisão Inteira'
    }

    for key, value in operations.items():
        print(f"{key} - {value}")

    choice = input('\nEscolha uma opção: ')

    if choice == '+':
        x = float(input('Digite o valor de x: '))
        y = float(input('Digite o valor de y: '))
        print(f'Adição: {x} + {y} = {x+y}')
    elif choice == '-':
        x = float(input('Digite o valor de x: '))
        y = float(input('Digite o valor de y: '))
        print(f' Subtração: {x} - {y} = {x-y}')
    elif choice == '*':
        x = float(input('Digite o valor de x: '))
        y = float(input('Digite o valor de y: '))
        print(f' Multiplicação: {x} * {y} = {x*y}')
    elif choice == '/':
        x = float(input('Digite o valor de x: '))
        y = float(input('Digite o valor de y: '))
        print(f'Divisão: {x} / {y} = {x/y}')
    elif choice == '%':
        x = float(input('Digite o valor de x: '))
        y = float(input('Digite o valor de y: '))
        print(f'Módulo: {x} % {y} = {x%y}')
    elif choice == '**':
        x = float(input('Digite o valor de x: '))
        y = float(input('Digite o valor de y: '))
        print(f'Exponencial: {x} ** {y} = {x**y}')
    elif choice == '//':
        x = float(input('Digite o valor de x: '))
        y = float(input('Digite o valor de y: '))
        print(f'Divisão Inteira: {x} // {y} = {x//y}')
    else:
        print('Operação inválida. Escolha novamente')

def turn_on_program():
    print('\nA iniciar o programa...')
    print('\n')
    print('              \                     ')
    print('               \                    ')
    print('                \                   ')
    print('                 \                  ')
    print(' - - - - - - - - -+        INÍCIO   ')
    print('                 /                  ')
    print('                /                   ')
    print('               /                    ')
    print('              /                     ')

def show_menu():

    options = {
        '1': 'Teste',
        '2': 'Cruz',
        '3': 'Círculo',
        '4': 'Triângulo',
        '5': 'Quadrado',
        '6': 'Retângulo',
        '7': 'Calculadora',
        '8': 'Comparador Numérico',
        '9': 'Comparador Ortográfico',
        '10': 'Procurar palavras',
        '11': 'Contador de ocorrências de caracter',
        '12': 'Operações com listas',
        '13': 'Conversor de dados js - py',
        '14': 'Jogo das Damas',
        '15': 'Jogo do Galo',
        '16': 'Jogo da Forca',
        '17': 'Saída'
    }

    print('\n')
    print('+ - - - - - - - - - - - - - - - - - +')
    print('| \  -   \  -  \  -  /  -  /   -  / |')
    print('|  \   -  \  +- - - - -+  /   -  /  |')
    print('|- - - - - + |   MENU  | + - - - - -|')
    print('|  /   -  /  +- - - - -+  \   -  \  |')
    print('| /  -   /  -  /  -  \  -  \   -  \ |')
    print('+ - - - - - - - - - - - - - - - - - +')
    print('\n')

    for key, value in options.items():
        print('+----------------+')
        print('-> 'f"{key}: {value}")
        print('+----------------+')

def draw_cross():
    print('\n')
    print('\nA opção escolhida foi: CRUZ\n')
    print('        \               /          ')
    print('          \           /            ')
    print('            \       /              ')
    print('              \   /                ')
    print('                .                  ')
    print('              /   \                ')
    print('            /       \              ')
    print('          /           \            ')
    print('        /               \          ')

def draw_circle():
    print('\n')
    print('\nA opção escolhida foi: CÍRCULO\n')
    print('         +  - - - -  +             ')
    print('       /               \           ')
    print('      /                 \          ')
    print('     +                   +         ')
    print('     |                   |         ')
    print('     +                   +         ')
    print('      \                 /          ')
    print('       \               /           ')
    print('         +  - - - -  +             ')

def draw_triangle():
    print('\n')
    print('\nA opção escolhida foi: TRIÂNGULO\n')
    print('               +                  ')
    print('              / \                 ')
    print('             /   \                ')
    print('            /     \               ')
    print('           /       \              ')
    print('          /         \             ')
    print('         /           \            ')
    print('        /             \           ')
    print('       +- - - - - - - -+          ')

def draw_square():
    print('\n')
    print('\nA opção escolhida foi: QUADRADO\n')
    print('       +- - - - - - - - -+         ')
    print('       |                 |         ')
    print('       |                 |         ')
    print('       |                 |         ')
    print('       |                 |         ')
    print('       |                 |         ')
    print('       |                 |         ')
    print('       |                 |         ')
    print('       +- - - - - - - - -+         ')

def draw_rectangle():
    print('\n')
    print('\nA opção escolhida foi: RETÂNGULO\n')
    print('+- - - - - - - - - - - - - - - - -+ ')
    print('|                                 | ')
    print('|                                 | ')
    print('|                                 | ')
    print('|                                 | ')
    print('|                                 | ')
    print('|                                 | ')
    print('+- - - - - - - - - - - - - - - - -+' )

def turn_off_program():
    print('\n')
    print('                    /              ')
    print('                   /               ')
    print('                  /                ')
    print('                 /                 ')
    print('    SAÍDA       +- - - - - - - - - ')
    print('                 \                 ')
    print('                  \                ')
    print('                   \               ')
    print('                    \              ')
    print('\nA desligar o programa...\n')

def menu():

    turn_on_program()

    while True:
        show_menu()

        choice = input('\nEscolha uma opção: ')

        if choice == '1':
            print('\nEsta é uma opção de teste.')
        elif choice == '2':
            draw_cross()
        elif choice == '3':
            draw_circle()
        elif choice == '4':
            draw_triangle()
        elif choice == '5':
            draw_square()
        elif choice == '6':
            draw_rectangle()
        elif choice == '7':
            calculator()
        elif choice == '8':
            number_comparator()
        elif choice == '9':
            word_comparator()
        elif choice == '10':
            word_finder()
        elif choice == '11':
            character_counter()
        elif choice == '12':
            list_options()
        elif choice == '13':
            conversor_js_py()
        elif choice == '14':
            damas()
        elif choice == '15':
            galo()
        elif choice == '16':
            forca()
        elif choice == '17':
            turn_off_program()
            break
        else:
            print('\nEscolha inválida. Tente novamente.')

menu()