import os
import json
import shutil

if __name__ == "__main__":
    # PATH DE BASE
    path = os.getcwd()

    # print('{}'.format(path))

    # MUDANDO O ENDEREÇO PATH DO SISTEMA PARA PEGAR O ARQUIVO JSON
    try:
        os.chdir(path+"/VALIDACAO/Resultado")
        print("Directory changed to ", os.getcwd())
    except OSError:
        print("Can't change the current working Directory")

    # Ler o arquivo JSON da Validacao
    with open('XG_Validation1.json') as f:
        data = json.load(f)

    # carregando as predições da validação
    prediction = [int(x) for x in data["prediction"].strip('][').split(' ')]

    # Definindo os labels da pasta das imagens
    attributes = ["BLISSUS", "CIGARRINHA"]

    # MUDANDO O ENDEREÇO PATH DO SISTEMA PARA PEGAR O NOME DAS IMAGENS
    try:
        os.chdir(path+"/VALIDACAO")
        print("Directory changed to ", os.getcwd())
    except OSError:
        print("Can't change the current working Directory")

    for count, filename in enumerate(os.listdir('Image')):

        # MUDANDO O ENDEREÇO PATH DO SISTEMA PARA PEGAR O NOME DAS IMAGENS
        try:
            os.chdir(path+"/VALIDACAO/Image")
            print("Directory changed to ", os.getcwd())
        except OSError:
            print("Can't change the current working Directory")

        valor = prediction[count-1]
        dst = os.path.splitext(filename)[0]+"@" + attributes[valor] + ".jpg"
        src = filename
        dst = dst

        # rename() function will
        # rename all the files
        os.rename(src, dst)


    source_folder = os.getcwd()
    dest_folder = path + "/VALIDACAO/Classificate"

    arquivos = os.listdir(source_folder)

    for arquivo in arquivos:
        shutil.move(os.path.join(source_folder, arquivo), dest_folder)
