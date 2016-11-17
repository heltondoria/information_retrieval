# Information Retrieval
Projeto de indexação e busca construído como parte do trabalho semestral do Bloco D da Pós-graduação Mit em BigData da Infnet

## Fase 1 - Criar uma lista invertiva em Python usando a biblioteca NLTK:
[Métodos de Busca - Aula 2.pdf](https://github.com/raulsenaferreira/Talks-and-Presentations/blob/master/Infnet/information_retrieval/M%C3%A9todos%20de%20busca%20-%20Aula%202.pdf)

- [x] Pegar 3 textos da imagem seguinte (pág. 18) e inicializar cada um em um arquivo diferente
- [x] Extrair o texto desses arquivos para dentro do python (3 variáveis ou array)
- [x] Aplica o tratamento aprendido na aula 1 e praticado na aula 2 para criação dos termos e remoção de stopwords
- [x] Criar a lista de ocorrências de termos dentro dos modelos de uma lista invertida e salvar o arquivo.
- [x] Usar a figura seguinte (pág. 18) como gabarito.

## Fase 2 - Criar um indexador utilizando pesos (tf-idf):
[Métodos de Busca - Aula 3.pdf](https://github.com/raulsenaferreira/Talks-and-Presentations/blob/master/Infnet/information_retrieval/M%C3%A9todos%20de%20busca%20-%20Aula%203.pdf)

- [x] Ler arqivo que contém a lista invertida (produzido na fase 1)
- [x] Criar um método de cálculo do tf-idf e atribuir o pesos aos termos da lista invertida lida do arquivo 
    - Consultar aula anterior para ver como é o cálculo do TF-IDF e como esse valor é atribuído na lista invertida
- [x] Salvar o resultado final em arquivo
- [x] O resultado pode ser salvo da mesma forma como foi salvo no exercício anterior, por exemplo:
    - termo;[doc1: 2.98, doc2: 1.74]


## Novas recursos que eu gostaria de incluir, fora do escopo do trabalho:
* [x] Tornar o uso do stemmer e do lemmatizer mutuamente exclusivos 
    > Removido posteriormente por que percebi que eram estratégias concorrentes e não necessariamente complementares. Além disso, um
    lemmatizador necessita de outras fases de normalização que incluam a classificação sintática dos tokens. Removido posteriormente por
    que percebi que eram estratégias concorrentes e não necessariamente complementares. Além disso, um lemmatizador
    necessita de outras fases de normalização que incluam a classificação sintática dos tokens.
* [ ] Criar testes unitários para todos os métodos para ter uma maior confiabilidade na qualidade do código (pendente)
* [x] Só usar o stemmer default caso o usuário não forneça um stemmer ou um lemmatizer 
    > Modificado posteriormente com a eliminação da possibilidade de
    > fornecer um lemmatizador. Porém modificado posteriormente com a
    > eliminação da possibilidade de fornecer um lemmatizador.
* [ ] Acrescentar busca por similaridade (prioridade)
* [x] Criar um hash como identificador único dos arquivos para que o índice seja o mesmo, independente da ordem de carregamento dos documentos
* [ ] Criar métodos (ou uma nova classe) para extrair métricas do índice (desejável)
* [x] Criar um método de carga de documentos que aceite um crawler como parâmetro, que será responsável por navegar em uma estrura de pastas
   carregando arquivos (desejável)
* [ ] Ampliar o suporte a crawlers, adicionando um crawler web (desejável)
* [x] Separar o tratamento de limpeza dos documentos, permitindo que outros tipos de arquivos, como páginas HTML, também possam ser
  indexados (desejável)
* [x] Aperfeiçoar meu código Python usando o pylint como orientador.
* [ ] Remodelar o código de acordo com o método S.O.L.I.D. (Robert C. Martin) (Em andamento)
* [x] Adicionar rankeamento de resultados de consultas
