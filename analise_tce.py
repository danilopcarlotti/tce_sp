import re, sys, os
from mNB_classification_text import mNB_classification_text

def topicos(FILE_PATH):
	topicos = []
	comeco_topico = False
	topico = ''
	for line in open(FILE_PATH, 'r'):
		if re.search(r'^\d\.\d{1,2}\.', line):
			topicos.append(topico)
			topico = line
		else:
			topico += line
	topicos.append(topico)
	return topicos[1:]

def titulo_topico(topico):
	titulo = re.search(r'^\d\.\d{1,2}\.(.*?)\n',topico)
	if titulo:
		return titulo.group(1).replace(':','').replace('-','').strip()
	return None

def jurisprudencia_partes(topico, so_textos = False, texto_classe = False, numero_classe = False):
	jurisprudencia = re.split(r'\n\d{6}\.\d{3}\.\d{2}\-\d', topico)
	if so_textos:
		return jurisprudencia[1:]
	
	titulo = titulo_topico(topico)
	
	if texto_classe:
		texto_classe_jurisprudencia = []
		for j in range(1,len(jurisprudencia)):
			texto_classe_jurisprudencia.append((jurisprudencia[j],titulo))
		return texto_classe_jurisprudencia
	
	if numero_classe:
		numero_processos = re.findall(r'\n\d{6}\.\d{3}\.\d{2}\-\d',topico)
		numero_classe_processo = []
		for j in range(len(numero_processos)):
			numero_classe_processo.append((numero_processos[j].strip(),titulo))
		return numero_classe_processo

def texto_num_decisoes(FILE_PATH):
	textos_num = []
	contador = 0
	for file in os.listdir(FILE_PATH):
		texto = '\n'
		if re.search(r'\.txt',file):
			for line in open(FILE_PATH+'/'+file,'r'):
				texto += line
		numero = re.search(r'\d{6,8}[\.\-\s]\d{3}[\.\-\s]\d{2}[\.\-\s]\d',file)
		if not numero:
			numero = re.search(r'\d{6,8}[\.\-\s]\d{3}[\.\-\s]\d{2}[\.\-\s]\d',texto)
		if numero:
			numero = numero.group(0)
			if len(numero) > 15:
				numero = numero[2:]
			textos_num.append((numero,texto))
		else:
			contador += 1
	return textos_num

def main(FILE_PATH):
	pass
	# PRIMEIRA PARTE: ANÁLISE DA CAPACIDADE DOS TRECHOS SEREM CLASSIFICADOS
	# classes = []
	# dados = []
	# tops = topicos(FILE_PATH)
	# for t in tops:
	# 	for parte in jurisprudencia_partes(t, texto_classe = True):
	# 		if parte[1] not in classes:
	# 			classes.append(parte[1])
	# 		# somente os trechos com parte da jurisprudência citada
	# 		if len(parte[0]) > 300:
	# 			dados.append(parte)
	# print('Foram encontradas '+str(len(classes))+' classes diferentes')
	# for classe in classes:
	# 	classificador = mNB_classification_text(dados, target_class=classe)
	# 	print('Para a classe '+classe+' houve uma precisao de '+str((classificador.validate_score(mean=True))))
	# 	print('Para esta classe foram encontrados '+str(classificador.dataframe['class'].value_counts())+' exemplos\n')

	# SEGUNDA PARTE: ANÁLISE DA CAPACIDADE DE SE CLASSIFICAR TEXTOS A PARTIR DE EXEMPLOS E DECISÕES
	# classes = []
	# dados = []
	# numeros_classe_processo = []
	# tops = topicos(FILE_PATH)
	# for t in tops:
	# 	for parte in jurisprudencia_partes(t, numero_classe = True):
	# 		if parte[1] not in classes:
	# 			classes.append(parte[1])
	# 		numeros_classe_processo.append(parte)
	# dados_textos_num = texto_num_decisoes('/home/danilo/Documents/TCE/votos')
	# for numero, classe in numeros_classe_processo:
	# 	for numero_t, texto in dados_textos_num:
	# 		if numero.strip() == numero_t.strip():
	# 			dados.append((texto, classe))
	# print('Foram encontradas '+str(len(classes))+' classes diferentes\n')
	# for classe in classes:
	# 	classificador = mNB_classification_text(dados, target_class=classe)
	# 	print('Para a classe '+classe+' houve uma precisao de '+str((classificador.validate_score(mean=True))))
	# 	print('Para esta classe foram encontrados '+str(classificador.dataframe['class'].value_counts())+' exemplos\n')


if __name__ == '__main__':
	FILE_PATH = '/home/danilo/Documents/TCE/exemplos_tce.txt'
	main(FILE_PATH)