# information_retrieval
Projeto de indexação e busca construído como parte do trabalho semestral do Bloco D da Pós-graduação Mit em BigData da Infnet


#Novas features a planejadas:
* Tornar o uso do stemmer e do lemmatizer mutuamente exclusivos(prioridade)
* Criar testes unitários para todos os métodos para ter uma maior confiabilidade na qualidade do código (prioridade)
* Só usar o stemmer default caso o usuário não forneça um stemmer ou um lemmatizer (prioridade)
* Passar a receber o stemmer e o lemmatizer como parâmetros do método de carga de documentos para permitir váriações no tratamento de diferentes cargas de arquivos (prioridade)
* Acrescentar busca por similaridade (prioridade)
* Criar um hash como identificador único dos arquivos para que o índice seja o mesmo, independente da ordem de carregamento dos documentos (desejável)
* Criar métodos (ou uma nova classe) para extrair métricas do índice (desejável)
* Criar um método de carga de documentos que aceite um crawler como parâmetro, que será responsável por navegar em uma estrura de pastas carregando arquivos (desejável)
* Ampliar o suporte a crawlers, adicionando um crawler web (desejável)
* Separar o tratamento de limpeza dos documentos, permitindo que outros tipos de arquivos, como páginas HTML, também possam ser indexados (desejável)


