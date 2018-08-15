from mNB_classification_text import mNB_classification_text
import pickle, difflib, pandas as pd

class padronizacao_itens():
	
	def __init__(self, dicionario_itens={}):
		self.dicionario_itens = dicionario_itens

	def classificador_itens_dicionario(self, dicionario_itens, nome_dicionario):
		dados = []
		for k, v in dicionario_itens.items():
			for i in v:
				dados.append((k,i))
		sck = mNB_classification_text(dados)
		pickle.dump(sck, open('classificador_%s.pickle' % (nome_dicionario,),'wb'))

	def dicionario_classes_itens_criar(self, arq_desc_itens):
		df = pd.read_csv(arq_desc_itens, error_bad_lines=False)
		for index_, row in df.iterrows():
			classe_item = row['Descrição Classe Item'].strip()
			desc_item = row['Descrição Item'].strip()
			if classe_item in self.dicionario_itens:
				if desc_item not in self.dicionario_itens[classe_item]:
					self.dicionario_itens[classe_item].append(desc_item)
			else:
				self.dicionario_itens[classe_item] = [desc_item]
		pickle.dump(self.dicionario_itens, open("dicionario_classe_itens.pickle", "wb" ) )

	def dicionario_desc_itens_diff(self, dicionario_itens):
		dicionario_itens_diff = {}
		for k in dicionario_itens:
			encontrei_representante = False
			for k_rep in dicionario_itens_diff:
				if self.ratio_strings(k, k_rep) >= 0.5:
					dicionario_itens_diff[k_rep].append(k)
					encontrei_representante = True
					break
			if not encontrei_representante:
				dicionario_itens_diff[k] = []
		pickle.dump(dicionario_itens_diff, open('dicionario_itens_diff.pickle','wb'))

	def dicionario_itens_criar(self, arq_desc_itens):
		df = pd.read_csv(arq_desc_itens, error_bad_lines=False)
		for index_, row in df.iterrows():
			desc_item = row['Descrição Item'].strip()
			codigo_item = int(row['Código Item'])
			if desc_item in self.dicionario_itens:
				if codigo_item not in self.dicionario_itens[desc_item]:
					self.dicionario_itens[desc_item].append(codigo_item)
			else:
				self.dicionario_itens[desc_item] = [codigo_item]
		pickle.dump(self.dicionario_itens, open("dicionario_itens.pickle", "wb" ) )

	def dicionario_grupos_itens_criar(self, arq_desc_itens):
		df = pd.read_csv(arq_desc_itens, error_bad_lines=False)
		for index_, row in df.iterrows():
			grupo_item = row['Descrição Grupo Item'].strip()
			desc_item = row['Descrição Item'].strip()
			if grupo_item in self.dicionario_itens:
				if desc_item not in self.dicionario_itens[grupo_item]:
					self.dicionario_itens[grupo_item].append(desc_item)
			else:
				self.dicionario_itens[grupo_item] = [desc_item]
		pickle.dump(self.dicionario_itens, open("dicionario_grupos_itens.pickle", "wb" ) )

	def ratio_strings(self, string1, string2):	
		diff = difflib.SequenceMatcher(lambda x: x==" ", string1, string2)
		return diff.ratio()


def main():
	p = padronizacao_itens()
	# dic = pickle.load(open('/home/danilo/Documents/tce_sp/dicionario_itens.pickle','rb'))
	# p.dicionario_desc_itens_diff(dic)
	# p.dicionario_classes_itens_criar('/home/danilo/Downloads/BASE 2009 - 2017 SEM QTDE FORNECEDORES PARTICIPANTES.csv')
	# p.dicionario_grupos_itens_criar('/home/danilo/Downloads/BASE 2009 - 2017 SEM QTDE FORNECEDORES PARTICIPANTES.csv')
	# p.dicionario_itens_criar('/home/danilo/Downloads/BASE 2009 - 2017 SEM QTDE FORNECEDORES PARTICIPANTES.csv')
	dic_classes = pickle.load(open('/home/danilo/Documents/tce_sp/dicionario_classe_itens.pickle','rb'))
	p.classificador_itens_dicionario(dic_classes,'classes_itens')
	dic_grupos = pickle.load(open('/home/danilo/Documents/tce_sp/dicionario_grupos_itens.pickle','rb'))
	p.classificador_itens_dicionario(dic_grupos,'grupos_itens')

if __name__ == '__main__':
	main()