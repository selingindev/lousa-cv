import cv2  # OpenCV - para captura de video e manipulacao de imagens
from cvzone.HandTrackingModule import HandDetector  # cvzone - fornece utilitario de rastreamento de maos

# abre a camera
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # OpenCV - captura o video da camera

# define a resolucao da camera
video.set(3, 1280)  # OpenCV - define a largura do video
video.set(4, 720)   # OpenCV - define a altura do video

# cria o objeto detector de mao
detector = HandDetector()  # cvzone - cria um detector de maos para detectar e rastrear as maos

# lista para armazenar as coordenadas dos pontos desenhados
desenho = []

while True:
    # le o quadro da camera
    check, img = video.read()  # OpenCV - le o quadro da camera
    
    # detecta as maos na imagem usando o detector do cvzone (que depende do MediaPipe)
    resultado = detector.findHands(img, draw=True)  # cvzone - detecta maos e desenha na imagem
    
    hand = resultado[0]  # Obtem a primeira mao detectada (se houver)

    if hand:
        # pega a lista de coordenadas das articulacoes
        lmlist = hand[0]['lmList']  # cvzone - acessa as coordenadas dos pontos de referencia das maos
        # verifica quais dedos estao levantados
        dedos = detector.fingersUp(hand[0])  # cvzone - verifica quais dedos estao levantados
        dedosLev = dedos.count(1)  # conta quantos dedos estao levantados

        # se um dedo estiver levantado, desenha um ponto
        if dedosLev == 1:
            x, y = lmlist[8][0], lmlist[8][1]  # Pega as coordenadas do dedo indicador
            cv2.circle(img, (x, y), 15, (0, 0, 255), cv2.FILLED)  # OpenCV - desenha um circulo no indicador
            desenho.append((x, y))  # Adiciona a posicao a lista de pontos desenhados
        # se nao for 1 ou 3 dedos levantados, reseta a lista de pontos
        elif dedosLev != 1 and dedosLev != 3:
            desenho.append((0, 0))  # Adiciona (0,0) para ignorar desenho
        # se 3 dedos estiverem levantados, limpa o desenho
        elif dedosLev == 3:
            desenho = []  # Limpa o desenho

        # desenha as linhas ligando os pontos
        for id, ponto in enumerate(desenho):
            x, y = ponto[0], ponto[1]
            cv2.circle(img, (x, y), 10, (0, 0, 255), cv2.FILLED)  # OpenCV - desenha circulos em cada ponto
            if id >= 1:
                ax, ay = desenho[id - 1][0], desenho[id - 1][1]
                if x != 0 and ax != 0:
                    cv2.line(img, (x, y), (ax, ay), (0, 0, 255), 20)  # OpenCV - desenha linhas entre os pontos

    # inverte a imagem horizontalmente
    imgFlip = cv2.flip(img, 1)  # OpenCV - inverte a imagem para simular um espelho
    # exibe a imagem na tela
    cv2.imshow('Img', imgFlip)  # OpenCV - exibe a imagem na tela
    # sai do loop se a tecla ESC for pressionada
    if cv2.waitKey(1) == 27:  # OpenCV - aguarda pressionamento de tecla
        break
