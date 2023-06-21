import random
import pygame
import time
from pygame.locals import *
from sys import exit
    
pygame.init()
pygame.font.init()

largura = 480
altura = 480
tamanho_quadrado = 60

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
ROXO = (255, 0, 255)
VERDE = (0, 255, 0)

tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont('arial', 20, True, True)

pygame.display.set_caption('Jogo de damas com IA')

tabuleiro = [
        [" ", "X", " ", "X", " ", "X", " ", "X"],
        ["X", " ", "X", " ", "X", " ", "X", " "],
        [" ", "X", " ", "X", " ", "X", " ", "X"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["O", " ", "O", " ", "O", " ", "O", " "],
        [" ", "O", " ", "O", " ", "O", " ", "O"],
        ["O", " ", "O", " ", "O", " ", "O", " "]
    ]

# Função para exibir o tabuleiro
def exibir_tabuleiro(tabuleiro):
    for linha in range(8):
        for coluna in range(8):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            pygame.draw.rect(tela, cor, (coluna * tamanho_quadrado, linha * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado))
            if tabuleiro[linha][coluna] == 'X':
                pygame.draw.circle(tela, CINZA, (coluna * tamanho_quadrado + tamanho_quadrado // 2, linha * tamanho_quadrado + tamanho_quadrado // 2), tamanho_quadrado // 2 - 5)
            elif tabuleiro[linha][coluna] == 'O':
                pygame.draw.circle(tela, VERMELHO, (coluna * tamanho_quadrado + tamanho_quadrado // 2, linha * tamanho_quadrado + tamanho_quadrado // 2), tamanho_quadrado // 2 - 5)
            elif tabuleiro[linha][coluna] == 'R':
                pygame.draw.circle(tela, AMARELO, (coluna * tamanho_quadrado + tamanho_quadrado // 2, linha * tamanho_quadrado + tamanho_quadrado // 2), tamanho_quadrado // 2 - 5)
            elif tabuleiro[linha][coluna] == 'D':
                pygame.draw.circle(tela, ROXO, (coluna * tamanho_quadrado + tamanho_quadrado // 2, linha * tamanho_quadrado + tamanho_quadrado // 2), tamanho_quadrado // 2 - 5)                

# Função para verificar se uma jogada é válida
def jogada_valida(tabuleiro, jogador, linha_origem, coluna_origem, linha_destino, coluna_destino):
    if linha_destino < 0 or linha_destino >= len(tabuleiro) or coluna_destino < 0 or coluna_destino >= len(tabuleiro[0]):
        return False
    peca = tabuleiro[linha_origem][coluna_origem]

    if peca != jogador and peca !="R":
        return False
    
    if linha_destino > linha_origem and peca != 'R':
        return False
        
    if tabuleiro[linha_destino][coluna_destino] == "O" and jogador == "O":
        return False
   
    if tabuleiro[linha_destino][coluna_destino] == "X" and jogador == "O":
        return False
           
    if abs(linha_destino - linha_origem) != abs(coluna_destino - coluna_origem):
        return False

    if abs(linha_destino - linha_origem) > 2 or abs(coluna_destino - coluna_origem) > 2:
        return False

    if abs(linha_destino - linha_origem) == 2 and abs(coluna_destino - coluna_origem) == 2:
        linha_captura = (linha_origem + linha_destino) // 2
        coluna_captura = (coluna_origem + coluna_destino) // 2

        if tabuleiro[linha_captura][coluna_captura] == " ":
            return False
    return True

# Função para realizar uma jogada
def realizar_jogada(tabuleiro, linha_origem, coluna_origem, linha_destino, coluna_destino):
    tabuleiro[linha_destino][coluna_destino] = tabuleiro[linha_origem][coluna_origem]
    tabuleiro[linha_origem][coluna_origem] = " "

    if abs(linha_destino - linha_origem) == 2 and abs(coluna_destino - coluna_origem) == 2:
        linha_captura = (linha_origem + linha_destino) // 2
        coluna_captura = (coluna_origem + coluna_destino) // 2
        tabuleiro[linha_captura][coluna_captura] = " "

# Função para obter as jogadas válidas para um jogador
def obter_jogadas_validas(tabuleiro, jogador):
    jogadas_validas = []
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            if tabuleiro[i][j] == jogador or tabuleiro[i][j] == "D":
                jogadas_validas.extend(obter_jogada_obrigatoria(tabuleiro, i, j))
    if len(jogadas_validas) == 0:
        for i in range(len(tabuleiro)):
            for j in range(len(tabuleiro[i])):            
                if tabuleiro[i][j] == jogador or tabuleiro[i][j] == "D":
                    jogadas_validas.extend(obter_jogadas_validas_peca_X(tabuleiro, i, j))    
    return jogadas_validas

# Função auxiliar para obter as jogadas válidas para uma peça "X"
def obter_jogadas_validas_peca_X(tabuleiro, linha, coluna):
    jogadas_validas = []
    if linha + 1 < len(tabuleiro):
        if coluna - 1 >= 0 and tabuleiro[linha + 1][coluna - 1] == " ":
            jogadas_validas.append((linha, coluna, linha + 1, coluna - 1))
        if coluna + 1 < len(tabuleiro[0]) and tabuleiro[linha + 1][coluna + 1] == " ":
            jogadas_validas.append((linha, coluna, linha + 1, coluna + 1))
    if linha - 1 < len(tabuleiro) and tabuleiro[linha][coluna] == "D":
        if coluna - 1 >= 0 and tabuleiro[linha - 1][coluna - 1] == " ":
            jogadas_validas.append((linha, coluna, linha - 1, coluna - 1))
        if coluna + 1 < len(tabuleiro[0]) and tabuleiro[linha - 1][coluna + 1] == " ":
            jogadas_validas.append((linha, coluna, linha - 1, coluna + 1))        
    return jogadas_validas

def obter_jogada_obrigatoria(tabuleiro, linha, coluna):
    jogadas_obrigatorias = []
    if linha + 2 < len(tabuleiro):
        if coluna - 2 >= 0 and tabuleiro[linha + 1][coluna - 1] == "O" and tabuleiro[linha + 2][coluna - 2] == " ":
            jogadas_obrigatorias.append((linha, coluna, linha + 2, coluna - 2))
        if coluna + 2 < len(tabuleiro[0]) and tabuleiro[linha + 1][coluna + 1] == "O" and tabuleiro[linha + 2][coluna + 2] == " ":
            jogadas_obrigatorias.append((linha, coluna, linha + 2, coluna + 2))
        if coluna - 2 >= 0 and tabuleiro[linha + 1][coluna - 1] == "R" and tabuleiro[linha + 2][coluna - 2] == " ":
            jogadas_obrigatorias.append((linha, coluna, linha + 2, coluna - 2))
        if coluna + 2 < len(tabuleiro[0]) and tabuleiro[linha + 1][coluna + 1] == "R" and tabuleiro[linha + 2][coluna + 2] == " ":
            jogadas_obrigatorias.append((linha, coluna, linha + 2, coluna + 2))            
    if linha - 2 < len(tabuleiro) and tabuleiro[linha][coluna] == "D":
        if coluna - 2 >= 0 and tabuleiro[linha - 1][coluna - 1] == "O" and tabuleiro[linha - 2][coluna - 2] == " ":
            jogadas_obrigatorias.append((linha, coluna, linha - 2, coluna - 2))
        if coluna + 2 < len(tabuleiro[0]) and tabuleiro[linha - 1][coluna + 1] == "O" and tabuleiro[linha - 2][coluna + 2] == " ":
            jogadas_obrigatorias.append((linha, coluna, linha - 2, coluna + 2))
        if coluna - 2 >= 0 and tabuleiro[linha - 1][coluna - 1] == "R" and tabuleiro[linha - 2][coluna - 2] == " ":
            jogadas_obrigatorias.append((linha, coluna, linha - 2, coluna - 2))
        if coluna + 2 < len(tabuleiro[0]) and tabuleiro[linha - 1][coluna + 1] == "R" and tabuleiro[linha - 2][coluna + 2] == " ":
            jogadas_obrigatorias.append((linha, coluna, linha - 2, coluna + 2))                 
    return jogadas_obrigatorias

def verif_dama_jog(tabuleiro, jogador, linha_destino, coluna_destino):
    if jogador == "O" and linha_destino == 0:
        tabuleiro[linha_destino][coluna_destino] = "R"

def verif_dama_ia(tabuleiro, jogador):       
    for j in range(len(tabuleiro[7])):
        if jogador == "X" and tabuleiro[7][j] == "X":
            tabuleiro[7][j] = "D"
             
# Função para verificar se o jogo acabou
def jogo_acabou(tabuleiro):
    peca_O = False
    peca_X = False
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[i])):
            if tabuleiro[i][j] == "O" or tabuleiro[i][j] == "R":
                peca_O = True
            elif tabuleiro[i][j] == "X" or tabuleiro[i][j] == "D":
                peca_X = True           
    return not peca_O or not peca_X

# Função principal do jogo
def jogar_damas():
    jogador_atual = "O"
    count = 0
    while not jogo_acabou(tabuleiro):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogo_acabou() == True
        relogio.tick(60)
        exibir_tabuleiro(tabuleiro)
        if jogador_atual == "O":
            texto = fonte.render("Vez do jogador (Vermelho)", 1, (AZUL))
            tela.blit(texto, (10,20))
            pygame.display.update()
            while not count == 1:         
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        jogo_acabou() == True
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:         
                        pos_mouse = pygame.mouse.get_pos()
                        coluna_origem = int(pos_mouse[0] // tamanho_quadrado)
                        linha_origem = int(pos_mouse[1] // tamanho_quadrado)
                        pygame.draw.rect(tela, VERDE, (coluna_origem * tamanho_quadrado, linha_origem * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado), 4)
                        pygame.display.update()
                        count = 1
            while count == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        jogo_acabou() == True
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:           
                        pos_mouse = pygame.mouse.get_pos()
                        coluna_destino = int(pos_mouse[0] // tamanho_quadrado)
                        linha_destino = int(pos_mouse[1] // tamanho_quadrado)
                        count = 0
            if jogada_valida(tabuleiro, jogador_atual, linha_origem, coluna_origem, linha_destino, coluna_destino):
                realizar_jogada(tabuleiro, linha_origem, coluna_origem, linha_destino, coluna_destino)
                verif_dama_jog(tabuleiro, jogador_atual, linha_destino, coluna_destino)
                jogador_atual = "X"
            else:
                texto = fonte.render("Jogada invalida, tente novamente", 1, (AZUL))
                tela.blit(texto, (10,60))
                pygame.display.update()
                time.sleep(2)
        else:
            texto = fonte.render("Vez do computador (Cinza)", 1, (AZUL))
            tela.blit(texto, (10,20))
            pygame.display.update()
            time.sleep(2)
            jogadas_validas = obter_jogadas_validas(tabuleiro, jogador_atual)
            if len(jogadas_validas) > 0:
                jogada = random.choice(jogadas_validas)
                realizar_jogada(tabuleiro, jogada[0], jogada[1], jogada[2], jogada[3])
            verif_dama_ia(tabuleiro, jogador_atual)
            jogador_atual = "O"  
        exibir_tabuleiro(tabuleiro)
        pygame.display.update() 
    texto = fonte.render("Fim de jogo!", 1, (AZUL))
    tela.blit(texto, (largura/2, altura/2))
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    quit()

# Iniciar o jogo
jogar_damas()
