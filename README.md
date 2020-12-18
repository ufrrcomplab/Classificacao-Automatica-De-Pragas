# Classificacao-Automatica-De-Pragas
Classificacao-Automatica-De-Pragas

# Imagens 
Aceitas são de formato JPG
Adicionei um na pasta Teste Alguns Imagens

# Commandos
Para Desligar, Construir e Montar o Docker
docker-compose down && docker-compose build && docker-compose up -d

Executado no Container para Debugar
docker logs --tail 20 --follow --timestamps classificacao-automatica-de-pragas_app_1

# O que é feito
Foi colocado no container o modelo preditivo já Treinada, os Scripts e as Pastas
depois o Upload da Imagem no directório /VALIDACAO/IMAGE
Foi feita a extração das caracteristicas com o arquivo *create data*
Logo a predição como o arquivo *make_prediction* que gerou alguns Resultado colocado na pasta Resultado
Foi renormado o filename da imagem inicial no Formato de filename+@+< a Classificação >
com a função set_prediction. com essa mesma função é removido a imagens da pasta Image [pasta de Upload ]
para a pasta de Classificate. (/VALIDACAO/Classificate)
Assim no arquivo App é usado uma string regex para pegar a classificação do filename da imagem classificada 
que esta localizada na pasta Classificate.
Essa classificação é retornado como resposta da APP
