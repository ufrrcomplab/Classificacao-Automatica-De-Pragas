# Classificacao-Automatica-De-Pragas
<p>Classificacao-Automatica-De-Inseto <em> Cigarrinha e Blissus Pulchellus </em> </p>

# Imagens 
<p>Aceitas são de formato JPG; </p>
<p>Adicionei um na pasta Teste Alguns Imagens; </p>

# Commandos
<p>Para Desligar, Construir e Montar o Docker ; </p>
<p> <em> docker-compose down && docker-compose build && docker-compose up -d </em> </p>

<p>Executado no Container para Debugar </p>
<p> <em>docker logs --tail 20 --follow --timestamps classificacao-automatica-de-pragas_app_1</em> </p>

# O que é feito
<p>Foi colocado no container o modelo preditivo já Treinada, os Scripts e as Pastas. </p>

<p>Depois o Upload da Imagem no directório <em>/VALIDACAO/IMAGE</em> . </p>

<p>Foi feita a extração das caracteristicas com o arquivo *create data* . </p>

<p>Logo a predição como o arquivo *make_prediction* que gerou alguns Resultado colocado na pasta Resultado. </p>

<p>Foi renormado o filename da imagem inicial no formato de <em>filename + @ + < Classificação ></em>
com a função set_prediction. Com essa mesma função é removido a imagens da pasta Image [pasta de Upload ]
para a pasta de Classificate. <em> /VALIDACAO/Classificate </em>. </p>

<p>Assim no arquivo App é usado uma string regex para pegar a classificação do filename da imagem classificada 
que esta localizada na pasta <em>Classificate</em>. </p>
<p>Essa classificação é retornado como resposta da APP </p>
