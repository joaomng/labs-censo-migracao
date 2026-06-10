import pandas as pd
import re
#import unicodedata


def so_alfanum(frase):
  '''Função pensada para os nomes de laboratórios de acordo com o leiaute
  de migração do censo.
  Transforma a string recebida em uma string só com caracteres alfa-numéricos e espaços;
  mas troca os caracteres acentuados pelos mesmos caracteres sem acento, por exemplo:
  á -> a, ç -> c'''

  #caracteres com acento: áãâàéèêíìîóòõôúùûüçñ


  frase= frase.replace("á", "a")
  frase= frase.replace("ã", "a")
  frase= frase.replace("â", "a")
  frase= frase.replace("à", "a")

  frase= frase.replace("é", "e")
  frase= frase.replace("è", "e")
  frase= frase.replace("ê", "e")

  frase= frase.replace("í", "i")
  frase= frase.replace("ì", "i")
  frase= frase.replace("î", "i")

  frase= frase.replace("ó", "o")
  frase= frase.replace("ò", "o")
  frase= frase.replace("õ", "o")
  frase= frase.replace("ô", "o")

  frase= frase.replace("ú", "u")
  frase= frase.replace("ù", "u")
  frase= frase.replace("û", "u")
  frase= frase.replace("ü", "u")

  frase= frase.replace("ç", "c")

  frase= frase.replace("ñ", "n")



  frase2 = re.sub(r'[^a-zA-Z0-9\s]', '', frase) #demais caracteres serão apagados


  return frase2



def migracao(nome_origem,nome_destino, aba_origem="Migracao"):

  '''Supondo que a planilha já está com tudo certo...
  A função lê a aba_origem da planilha excel nome_origem e
  escreve no txt nome_destino os dados para a migração, já na formatação
  correta '''

  xls = pd.ExcelFile(nome_origem)
  df1 = pd.read_excel(xls, aba_origem, header=0)

  n_linhas,  n_col = df1.shape

  print("linhas: "+str(n_linhas)+", colunas: "+str(n_col))

  #nome_destino = "caxias_migracao.txt"

  #######Criando o arquivo de migração supondo que já está tudo certo na planilha!####################


  #OBS: As planilhas (25/03/2026) estão na ordem: cabeçalho - registro 10, ID da IES(586),  reg_lab' (sempre 11), nome,
  #cod_lab, ativo, descricao, palavras_chave, informatica, exatas_e_da_terra, biologicas, engenharias, saude, agrarias,
  #sociais_aplicadas, humanas, linguistica_letras_e_artes, itinerante, outros_alunos_usaram, ensino, pesquisa, extensao,
  #acesso_agendamento, manutencao, gerenciamento_riscos, gerenciamento_residuos, esta_em_local_de_oferta,
  #codigo_local_oferta, #codigo_UF, codigo_municipio,
  #reg_curso, cursos
  #MESMA ORDEM DO LAYOUT!

  #O campo UF não deve ser informado quando o campo
  # 'O laboratório está localizado em algum local de oferta da IES?' for informado como '1-Sim'|

  #O campo município não deve ser informado quando o campo
  # 'O laboratório está localizado em algum local de oferta da IES?' for informado como '1-Sim'

  arq_dest = open(nome_destino, "w+")

  arq_dest.write("10|586\r\n") #registro de laboratorio| ID da UFRJ
  #o \r\n é pra windows


  campos = dict() #vai ser tudo string!!
  campos_lista = []
  cursos = []

  nomes_iguais = dict() #As chaves são os nomes dos labs e os valores são
                        #quantos labs tem o mesmo nome


  for i in range(n_linhas):

    cursos = []
    campos_lista = []

    linha = df1.iloc[i]

    tam_linha = len(linha)
    #print("colunas na linha "+str(i)+": "+str(tam_linha))
    campos["reg_lab"] = "11"
    campos_lista.append("11")

    nome = str(linha.iloc[3])

    cleaned_string = re.sub(r'[^a-zA-Z0-9áãâàéèêíìîóòõôúùûüçñÁÃÂÀÉÈÊÍÌÎÓÒÕÚÙÛÜÇÑ\s,.-]', '', nome)
    #leaned_string = so_alfanum(nome)


    aux = cleaned_string.replace("\r", " ")
    nome_final = aux.replace("\n", " ")

    if(nome_final in nomes_iguais.keys()):
      nomes_iguais[nome_final] += 1

      qtd = nomes_iguais[nome_final]

      nome_final = nome_final+" "+str(qtd)


    else:
      nomes_iguais[nome_final] = 0

    nome_final = nome_final.replace("\xa0", "\x20") #espaço "errado" por espaço certo

    while(nome_final.startswith("-") or nome_final.startswith(" ")):
      nome_final=nome_final[1:]

    campos["nome"] = nome_final
    campos_lista.append(nome_final)

    campos["cod_lab"] = str(linha.iloc[4])
    campos_lista.append(str(linha.iloc[4]))
    print(campos["cod_lab"])

    campos["ativo"] = str(int(float(linha.iloc[5]))) #pra não ficar 1.0
    campos_lista.append(str(int(float(linha.iloc[5]))) )

    descricao = (str(linha.iloc[6]))[:2000]
    cleaned_string = (re.sub(r'[^a-zA-Z0-9áãâàéèêíìîóòõôúùûçñÁÃÂÀÉÈÊÍÌÎÓÒÕÚÙÛÜÇÑ\s,.-]', '', descricao)).replace("ü", "u")
    #cleaned_string = re.sub(r'[^a-zA-Z0-9\s,.]', '', descricao)

    aux = cleaned_string.replace("\r", "")
    descricao_inter = aux.replace("\n", "\x20")
    descricao_final = descricao_inter.replace("\xa0", "\x20") #espaço "errado" por espaço certo

    while(descricao_final.startswith("-") or descricao_final.startswith(" ")):
      descricao_final=descricao_final[1:]

    campos["descricao"] = descricao_final
    campos_lista.append(descricao_final)

    palavras_chave = (str(linha.iloc[7]))[:100]
    keywords2 = re.sub("[;]", ",", palavras_chave)

    cleaned_string = re.sub(r'[^a-zA-Z0-9áãâàéèêíìîóòõôúùûüçñÁÃÂÀÉÈÊÍÌÎÓÒÕÚÙÛÜÇÑ\s,.]', '', keywords2)
    #cleaned_string = re.sub(r'[^a-zA-Z0-9\s,.]', '', keywords2)

    aux = cleaned_string.replace("\r", "")
    keywords_final = aux.replace("\n", "")

    campos["palavras_chave"] = keywords_final
    campos_lista.append(keywords_final)

    campos["informatica"] = str(linha.iloc[8])
    campos_lista.append(str(linha.iloc[8]))



    campos["exatas_e_da_terra"] = str(linha.iloc[9])
    campos_lista.append(str(linha.iloc[9]))

    campos["biologicas"] = str(linha.iloc[10])
    campos_lista.append(str(linha.iloc[10]))

    campos["engenharias"] = str(linha.iloc[11])
    campos_lista.append(str(linha.iloc[11]))

    campos["saude"] = str(linha.iloc[12])
    campos_lista.append(str(linha.iloc[12]))

    campos["agrarias"] = str(linha.iloc[13])
    campos_lista.append(str(linha.iloc[13]))

    campos["sociais_aplicadas"] = str(linha.iloc[14])
    campos_lista.append(str(linha.iloc[14]))

    campos["humanas"] = str(linha.iloc[15])
    campos_lista.append(str(linha.iloc[15]))

    campos["linguistica_letras_e_artes"] = str(linha.iloc[16])
    campos_lista.append(str(linha.iloc[16]))


    campos["itinerante"] = str(linha.iloc[17])
    campos_lista.append(str(linha.iloc[17]))

    campos["outros_alunos_usaram"] = str(linha.iloc[18])
    campos_lista.append(str(linha.iloc[18]))


    campos["ensino"] = str(linha.iloc[19])
    campos_lista.append(str(linha.iloc[19]))

    campos["pesquisa"] = str(linha.iloc[20])
    campos_lista.append(str(linha.iloc[20]))


    campos["extensao"] = str(linha.iloc[21])
    campos_lista.append(str(linha.iloc[21]))


    campos["acesso_agendamento"] = str(linha.iloc[22])
    campos_lista.append(str(linha.iloc[22]))

    campos["manutencao"] = str(linha.iloc[23])
    campos_lista.append(str(linha.iloc[23]))

    campos["gerenciamento_riscos"] = str(linha.iloc[24])
    campos_lista.append(str(linha.iloc[24]))

    campos["gerenciamento_residuos"] = str(linha.iloc[25])
    campos_lista.append(str(linha.iloc[25]))


    campos["esta_em_local_de_oferta"] = str(linha.iloc[26])
    campos_lista.append(str(linha.iloc[26]))

    campos["codigo_local_oferta"] = str(linha.iloc[27])
    campos_lista.append(linha.iloc[27])

    campos["codigo_UF"] = str(linha.iloc[28])
    if(campos["esta_em_local_de_oferta"] == "1"):
      campos_lista.append("")
      campos["codigo_UF"] = ""
    else:
      campos_lista.append(str(linha.iloc[28]))


    #print(str(linha.iloc[28]))

    campos["codigo_municipio"] = str(linha.iloc[29])
    if(campos["esta_em_local_de_oferta"] == "1"):
      campos_lista.append("")
      campos["codigo_municipio"] = ""
    else:
      campos_lista.append(str(linha.iloc[29]))



    campos["reg_curso"] = str(linha.iloc[30])
    #campos_lista.append(str(linha.iloc[30])) #isso é um "12",
    #que tem que estar na linha seguinte

    cursos.append(str(int(float(linha.iloc[31])))) #o primeiro curso
    #precisa fazer isso pra evitar o "14368.0"
    print("primeiro curso inserido")

    #obs:esse negocio de tamanho da linha não funcionou
    #mas a verificação feita impede de colocar um curso vazio
    print("inserindo demais cursos")
    for j in range(tam_linha-32): #cursos além do primeiro informado


      curso = str(linha.iloc[32+j])
      if((curso != "") and(curso !="nan")):
        print("inserindo curso")
        cursos.append(str(int(float(curso))))



    #print("\n\n", campos)

    #agora é só escrever a linha do lab e as dos cursos correspondentes
    linha_lab = ""
    #print("\n\n")

    indice = 0
    idx_esta_local_oferta = 24 #indice da informação "está em local de oferta" em campos_lista
    for campo in campos_lista: #pegando do "11" até o código do municipio

      if(indice==idx_esta_local_oferta):
        if(campos["itinerante"] == "1"): #não é pra preencher local de oferta
          print("\n\n LAB "+campos["cod_lab"]+ " é itinerante!")
          linha_lab+= "|"
          indice +=1
          continue


      linha_lab+= str(campo) +"|"
      indice+=1

    arq_dest.write( (linha_lab[:len(linha_lab) -1])+"\r\n") #sem o ultimo "|"

    #falta só os cursos
    for curso in cursos:
      arq_dest.write("12|"+curso+"\r\n")





  arq_dest.close()

  print("Arquivo de migração "+nome_destino+ " pronto")





if __name__ == "__main__":
  nome_arquivo = input("Insira o nome da planilha para Migração. Exemplo: Instituto_de_Historia.xlsx\n")
  aba_origem = input("Insira o nome da aba na planilha com as informações para migração. Exemplo: Migracao\n")
  nome_destino = input("Insira o nome do arquivo final da migração. Exemplo: migracao_IH.txt\n")


  migracao(nome_arquivo, nome_destino, aba_origem)

