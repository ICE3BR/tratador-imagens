#pip install opencv-python (cv2)
import cv2 #RGB -> cv2 = BGR
import textwrap
import os

def tratamento(arquivo, qtde_filtro, arquivo_local_save):
    img = cv2.imread(f"{arquivo}") # Local da imagem

    # Tratamento da imagem aqui...
    img_pb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converte a imagem para preto e branco (cv2.COLOR_BGR2GRAY) [na net: mais opções em Color conversions OpenCV]

    img_invertida = cv2.bitwise_not(img_pb)
    img_blur = cv2.GaussianBlur(img_invertida, (qtde_filtro, qtde_filtro), 0) # Coloca blur porem só aceita numeros positivos (qtde_filtro) impares
    img_blur_invert = cv2.bitwise_not(img_blur)
    img_desenho = cv2.divide(img_pb, img_blur_invert, scale=256.0) # Divide pb/blur_invert e multiplica por 256 para a escala de cor não ficar 0|1

    img_final = img_desenho
    cv2.imwrite(arquivo_local_save, img_final) # Local para salvar a imagem
    return img_final

def preview(img_final):
    img_show = cv2.resize(img_final, (590, 700)) # Redimensioa a interface para um tamanho (x,y)
    cv2.namedWindow("image_preview", cv2.WINDOW_NORMAL) # Permite Redimensionar a interface manualmente
    cv2.imshow("image_preview", img_show) # Cria e Exibe uma interface com a foto
    cv2.waitKey(0) # 0 = ESC ou X | Quando fechar a imagem ele para o código
    cv2.destroyAllWindows() # Quando parar destroi todas as interfaces criadas

def menu_selecao_img(): # Menu Principal
    menu = """\n\t<====== Deseja selecionar apenas uma imagem ou uma pasta inteira ? ======>
[1] - Imagem
[2] - Pasta
=>> """
    return input(textwrap.dedent(menu))

def menu_preview(): # Menu Principal
    menu = """\n\t<====== Deseja Visualizar a imagem ? ======>
[Y] - Yes
[n] - No
=>> """
    return input(textwrap.dedent(menu))

def main():
    print("\t<=========== Tratador de imagens ==========>")
    print("Transforma as imagens em estilo desenho preto e branco")
    
    while True:
        menu_selecao = menu_selecao_img()
        #local_save = ("C:\Users\user\Downloads") # acho que n vai funionar para qualquer usuário que executar pois o user muda né ?
        if menu_selecao == "1":
            arquivo = input("Insira o caminho da imagem que deseja tratar (ex: minhas fotos/imagem.png):\n=>> ") # Insira o caminho da imagem que deseja tratar
            qtde_filtro = int(input("Insira a quantidade de blur (Aceita apenas numeros positivos e impares):\n=>> ")) # Insira a quantidade de pixels do filtro Gaussiano
            local_save = input("Insira a pasta para salvar (ex: C:\Users\user\Downloads):\n=>> ") # Insira a pasta para salvar
            img_final = tratamento(arquivo, qtde_filtro, local_save)
            if img_final is not None:
                break
        elif menu_selecao == "2": # @@@ Provavelmente com um erro ainda nesta parte @@@
            imagens_local_pasta = input("Informe o local completo da pasta:\n=>> ") # Local da pasta com as imagens
            qtde_filtro = int(input("Insira a quantidade de blur (Aceita apenas numeros positivos e impares):\n=>> ")) # Insira a quantidade de pixels do filtro Gaussiano
            local_save = input("Insira a pasta para salvar (ex: C:\Users\user\Downloads):\n=>> ") # Insira a pasta para salvar
            lista_arquivos = os.listdir(f"{imagens_local_pasta}") ### @@@ Provavelmente a parte de salvar não está funcionando aqui: @@@
            for arquivo_l in lista_arquivos:
                img_final = tratamento(arquivo_l, qtde_filtro, local_save)
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")
    
    while True:
        opcao = menu_preview()
        if opcao == "Y":
            if img_final is not None:
                preview(img_final)
            break
        elif opcao == "n":
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

main()

# Preciso adicionar uma opção que informa a localização que o usuário deseja salvar as imagens - FEITO
# (e colocar o padrão em downloas (talvez com uma pasta criada junto))