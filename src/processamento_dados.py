import json
import csv

class Dados:
    def __init__(self, path, tipo_dados):
        self.path = path
        self.tipo_dados = tipo_dados
        self.dados = self.leitura_dados()
        self.nome_colunas = self.get_columns()
        self.qtd_linhas = self.size_data()        

    # Leitura dos dados json
    def leitura_json(self):
        with open(self.path, 'r') as file:
            dados_json = json.load(file)
        return dados_json

    # Leitura dos dados csv
    def leitura_csv(self):
        dados_csv = []
        with open(self.path, 'r') as file:
            leitura = csv.DictReader(file, delimiter=',')
            for coluna in leitura:
                dados_csv.append(coluna)
        return dados_csv

    # Analise do tipo de dado para executar a leitura
    def leitura_dados(self):
        dados = []
        if self.tipo_dados == 'csv':
            dados = self.leitura_csv()
        elif self.tipo_dados == 'json':
            dados = self.leitura_json()
        elif self.tipo_dados == 'list':
            dados = self.path
            self.path = 'lista em memoria'

        return dados  

    # Pega o nome das colunas
    def get_colunas(self):
        return list(self.dados[-1].keys())

    # Renomeia as colunas usando um dicionário de mapeamento de nomes
    def renomeando_colunas(self, key_mapping):
        new_dados = []

        for old_dict in self.dados:
            dict_temp = {}
            for old_key, value in old_dict.items():
                dict_temp[key_mapping[old_key]] = value
            new_dados.append(dict_temp)

        self.dados = new_dados
        self.nome_colunas = self.get_columns()

    # Retorna a quantidade de registros nos dados
    def size_data(self):
        return len(self.dados)

    # Juntando os dados
    def join(dadosA, dadosB):
        combined_list = []
        combined_list.extend(dadosA.dados)
        combined_list.extend(dadosB.dados)
        return Dados(combined_list, 'list')

    # Transforma os dados em uma tabela 
    def transformando_dados_tabela(self):
        dados_combinados_tabela = [self.nome_colunas]
        for row in self.dados:
            linha = []
            for coluna in self.nome_colunas:
                linha.append(row.get(coluna, 'Sem registro'))
            dados_combinados_tabela.append(linha)
        return dados_combinados_tabela

    # Salva os dados em formato CSV
    def salvando_dados(self, path):
        dados_combinados_tabela = self.transformando_dados_tabela()
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(dados_combinados_tabela)
