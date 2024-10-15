import time
import re
from pdfminer.high_level import extract_text

meses = {
    "janeiro": "01",
    "fevereiro": "02",
    "março": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12"
}

def extraiPdf(caminho):

    textoPdf = extract_text(caminho)

    textoPdf = re.sub(r'\s+', ' ', textoPdf)

    resultados = {}

    encontrou = re.search(r'Processo(?:\s*[nºo°]*\.?\s*| No\.)?\s*[:\-]?\s*([\d\.\-\/]+)', textoPdf, re.IGNORECASE)
    # \s - Significa espaços vazios
    # * - ocorrência o valor antecessor zero ou mais vezes
    # [nºoº] - Colchetes p/ indicar busca, com o valor podendo variar entre "n", "º" ou "o"
    # * ao final - Ocorrência zero ou mais vezes
    # \. - A "\" significa que o "." é literal, uma vez que apenas . é um comando do RegEx
    # \s* - Significa espaços vazios, zero ou mais vezes
    # | - Pipe signifca ou
    # No\. - Busca o "No" seguido de "." literal
    # )? - ao final significa que os valores dentro de "()" é opcional
    # \s* - Espaços vazios, zero ou mais vezes

    # \d - Digitos (0,9)
    # \. - Ponto literal
    # \- - Hífen literal, uma vez que apenas hífen é um comando, assim como apenas "."
    # \/ - Barra literal, uma vez que apenas barra é um comando, assim como apenas "."
    # ]+ - Ao final refaz o padrão de números novamente, no caso o resto do número do Processo.

    if encontrou:
        numero_processo = encontrou.group(1).strip()
        resultados["Número do Processo"] = numero_processo
    else:
        resultados["Número do Processo"] = "Não encontrado"

    encontrou = re.search(r'(?:Código da Vara|Vara)[\s:]*([\d]+)', textoPdf, re.IGNORECASE)
    resultados["Código da Vara"] = encontrou.group(1) if encontrou else "Não encontrado"

    encontrou = re.search(r'(?:Código da Ação|Ação)[\s:]*([\d]+)', textoPdf, re.IGNORECASE)
    resultados["Código da Ação"] = encontrou.group(1) if encontrou else "Não encontrado"

    encontrou = re.search(r'Beneficiário(?:a)?[:]?[\s]*([^\n]+?)(?:Autor|Réu|Registro Geral)', textoPdf, re.IGNORECASE)
    if encontrou:
        nome_beneficiario = encontrou.group(1).strip()
        resultados["Nome do Beneficiário"] = nome_beneficiario
    else:
        resultados["Nome do Beneficiário"] = "Não encontrado"

    encontrou = re.search(r'(?:Registro Geral de Indicação|RGI)[:]?[\s]*([\d\s]+)', textoPdf, re.IGNORECASE)
    if encontrou:
        rgi = encontrou.group(1).strip()
        rgi = rgi.replace(" ", "")
        resultados["Registro Geral de Indicação"] = rgi
	if(len(rgi) != 23):
		resultados["Registro Geral de Indicação"] = "Quantidade caracteres inválido."
    else:
        resultados["Registro Geral de Indicação"] = "Não encontrado"

    encontrou = re.search(r'Data da nomeação[:]?[\s]*([\d]{2}/[\d]{2}/[\d]{4})', textoPdf, re.IGNORECASE)
    resultados["Data da Nomeação"] = encontrou.group(1).replace("/","") if encontrou else "Não encontrado"

    encontrou = re.search(r'Data da sentença[:]?[\s]*([\d]{2}/[\d]{2}/[\d]{4})', textoPdf, re.IGNORECASE)
    resultados["Data da Sentença"] = encontrou.group(1).replace("/","") if encontrou else "Não encontrado"

    encontrou = re.search(r'Data do trânsito em julgado[:]?[\s]*([\d]{2}/[\d]{2}/[\d]{4})', textoPdf, re.IGNORECASE)
    resultados["Data do Trânsito em Julgado"] = encontrou.group(1).replace("/","") if encontrou else "Não encontrado"

    encontrou = re.search(r'(\d{2}) de (\w+) de (\d{4})', textoPdf, re.IGNORECASE)
    if encontrou:
        dia = encontrou.group(1)
        mesExtenso = encontrou.group(2).lower()
        ano = encontrou.group(3)
        if mesExtenso in meses:
            mes = meses[mesExtenso]
        else:
            mes = "Mês inválido"

        if mes != "Mês inválido":
            dataFormatada = f"{dia}{mes}{ano}"
            resultados["Data de Emissão"] = dataFormatada
        else:
            resultados["Data de Emissão"] = "Mês inválido"
    else:
        resultados["Data de Emissão"] = "Não encontrado"


    return resultados


"""while True:
    participacaoParte = int(input("Autor ou Réu [1,2]: "))
    atosPraticados = int(input("1- Todos os atos do processo \n2- Atuação parcial \n4- Recurso \n10 - 2º Júri \n16 - Produção Antecipada de Provas – Art. 366, CPP. \nEscolha: "))
    resultadoAcao = int(input("\n\nResultado da Ação:\n1 - Procedente\n2 - Parcialmente Procedente\n3 - Improcedente\n4 - Sem Julgamento\n5 - Acordo\n6 - Desistência\n7 - Outro\nEscolha: "))
    if participacaoParte in [1, 2] and atosPraticados in range(1, 17) and resultadoAcao in range(1, 8):
        break
    else:
        print("Entrada inválida, por favor tente novamente.")"""

caminho = 'teste.pdf'

dados = extraiPdf(caminho)
for key, value in dados.items():
    print(f"{key}: {value}")
