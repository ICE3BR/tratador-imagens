# pip install opencv-python (cv2)
import cv2  # RGB -> cv2 = BGR
import textwrap
import os
from pathlib import Path

def tratamento(arquivo, qtde_filtro, arquivo_local_save):
    img = cv2.imread(f"{arquivo}")  # Local da imagem

    if img is None:
        print(f"Erro: Não foi possível ler a imagem {arquivo}. Verifique o caminho e tente novamente.")
        return None

    if qtde_filtro % 2 == 0:
        qtde_filtro += 1  # Adiciona 1 para o filtro sempre ser ímpar

    # Tratamento da imagem aqui...
    print("Imagem em Tratamento... aguarde")
    img_pb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converte a imagem para preto e branco (cv2.COLOR_BGR2GRAY)

    img_invertida = cv2.bitwise_not(img_pb)
    img_blur = cv2.GaussianBlur(img_invertida, (qtde_filtro, qtde_filtro), 0)  # Aplica blur
    img_blur_invert = cv2.bitwise_not(img_blur)
    img_desenho = cv2.divide(img_pb, img_blur_invert, scale=256.0)  # Divide pb/blur_invert e multiplica por 256

    img_final = img_desenho
    print("Imagem finalizada, iniciando salvamento")

    # Salva a imagem tratada
    if not os.path.exists(arquivo_local_save): # Caso o diretório de save não seja especificado/exista, o padrão será pasta download
        os.makedirs(arquivo_local_save)

    base_name = os.path.splitext(os.path.basename(arquivo))[0]
    save_path = os.path.join(arquivo_local_save, f"{base_name}_tratada")

    # Adicionar número sequencial ao nome do arquivo para evitar sobrescrita
    counter = 1
    while os.path.exists(f"{save_path}_{counter}.png"):
        counter += 1

    final_save_path = f"{save_path}_{counter}.png"
    cv2.imwrite(final_save_path, img_final)  # Local para salvar a imagem
    print(f"Imagem tratada salva em: {final_save_path}")
    return img_final

def preview(img_final):
    img_show = cv2.resize(img_final, (590, 700))  # Redimensiona a interface para um tamanho (x,y)
    cv2.namedWindow("image_preview", cv2.WINDOW_NORMAL)  # Permite redimensionar a interface manualmente
    cv2.imshow("image_preview", img_show)  # Cria e exibe uma interface com a foto
    cv2.waitKey(0)  # 0 = ESC ou X | Quando fechar a imagem ele para o código
    cv2.destroyAllWindows()  # Quando parar, destrói todas as interfaces criadas

def menu_selecao_img():  # Menu Principal
    menu = """\n\t<====== Deseja selecionar apenas uma imagem ou uma pasta inteira? ======>
[1] - Imagem
[2] - Pasta
=>> """
    return input(textwrap.dedent(menu))

def menu_preview():  # Menu Principal
    menu = """\n\t<====== Deseja visualizar a imagem? ======>
(Não recomendo usar se fez tratamentos de pasta com várias imagens)
[Y] - Yes
[n] - No
=>> """
    return input(textwrap.dedent(menu))

def main():
    print("\t<=========== Tratador de imagens ==========>")
    print("Transforma as imagens em estilo desenho preto e branco")
    
    # Definir o diretório padrão de Downloads
    downloads_path = str(Path.home() / "Downloads")
    
    while True:
        menu_selecao = menu_selecao_img()
        if menu_selecao == "1":
            arquivo = input("Insira o caminho da imagem que deseja tratar (ex: minhas fotos/imagem.png):\n=>> ")  # Insira o caminho da imagem que deseja tratar
            qtde_filtro = int(input("Insira a quantidade de blur:\n=>> "))  # Insira a quantidade de pixels do filtro Gaussiano
            local_save = input(f"Insira a pasta para salvar (padrão: {downloads_path}):\n=>> ")  # Insira a pasta para salvar
            if not local_save:
                local_save = downloads_path  # Usar Downloads como padrão se o usuário não especificar
            img_final = tratamento(arquivo, qtde_filtro, local_save)
            if img_final is not None:
                break
        elif menu_selecao == "2":
            imagens_local_pasta = input("Informe o local completo da pasta:\n=>> ")  # Local da pasta com as imagens
            qtde_filtro = int(input("Insira a quantidade de blur:\n=>> "))  # Insira a quantidade de pixels do filtro Gaussiano
            local_save = input(f"Insira a pasta para salvar (padrão: {downloads_path}):\n=>> ")  # Insira a pasta para salvar
            if not local_save:
                local_save = downloads_path  # Usar Downloads como padrão se o usuário não especificar
            lista_arquivos = os.listdir(imagens_local_pasta)
            for arquivo_l in lista_arquivos:
                caminho_completo = os.path.join(imagens_local_pasta, arquivo_l)
                img_final = tratamento(caminho_completo, qtde_filtro, local_save)
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")
    
    while True: # Menu Para perguntar se deseja ter um preview de como ficou a imagem
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