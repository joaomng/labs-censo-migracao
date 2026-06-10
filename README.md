# labs-censo-migracao
Repositório com os scripts em python para produzir arquivos de migração de laboratórios para o Censo da Educação Superior

O script gera um arquivo .txt para ser submetido à funcionalidade de migração de laboratórios no site do censo da educação superior <br/>
https://censosuperior.inep.gov.br/censosuperior

## IMPORTANTE:
Só funciona com planilhas que estejam formatadas conforme a planilha de exemplo (note as fórmulas utilizadas na aba "Migracao")

## Dependências:

- pandas <br/>

   pip install pandas 

## Como utilizar:

Executar notebook .ipynb, ou:

<b> 1. Instalar python: </b> <br/>
    No windows, pesquisar "python" na barra de pesquisa e instalar conforme a página da microsoft store que será aberta. <br/>

<b> 2. Instalar dependências </b> <br/>
    No windows, pesquisar "cmd" na barra de pesquisa. Apertando Enter será aberto o prompt de comando. <br/>
    No prompt, digitar: 
      
      pip install pandas

<b> 3. Executar o programa </b> <br/>
  3.1. Fazer o download deste repositório; <br/>
  3.2. Extrair o repositório; <br/>
  3.3. Abrir o cmd e ir para a pasta do repositório. O comando "cd" abre uma pasta, por exemplo, o comando: <br/>
  
       cd Documentos 
  
  abre a pasta Documentos. O comando <br/> 
  
       cd Documentos\Pasta_1 
       
  abre a pasta Pasta_1, que está dentro da pasta documentos <br/>
  
  <b> 3.4. Digitar o seguinte comando </b> <br/>
  
        python migracao_labs.py 

  O programa iniciará a execução.

  <b> 3.5. Siga as instruções na tela </b> <br/>
  Será solicitado o nome da planilha e da aba da planilha, é preciso digitá-los corretamente, incluindo maiúsculas e minúsculas. <br/>
  
        

## Obs:
O notebook .ipynb neste repositório possibilita uma execução interativa dos scripts de migração, permitindo entre outras coisas executar sem utilizar a função input()


