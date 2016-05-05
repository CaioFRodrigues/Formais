"""Terminais					# A secao de simbolos terminais eh a primeira do arquivo.
{ runs, barks, eats, espresso, coffee, machine, cat, the, a }	# Tudo o que estiver apos o sustenido (#)  sera considerado comentario. 
Variaveis				    	
{ N, V, NP, DT, VP, S }			  	
Inicial					
{ S }							# Os simbolos terminais sao qualquer sequencia de caracteres 
Regras						# (nao reservados) entre chaves. Os elementos do conjunto sao separados por virgula.
{ S > NP , VP }   				# A secao de simbolos terminais inicia com a palavra-chave "Terminais".
{ NP > DT , N }  				# Eh altamente recomendavel que simbolos terminais iniciem por caracteres minusculos.
{ N > N , N }  
{ N > coffee }  
{ N > machine }   				# Simbolos nao podem conter os caracteres "{", "}", "#" ou ">", por serem reservados
{ N > cat } ;				  	# A secao de variaveis inicia por "Variaveis", e eh a segunda do arquivo
{ N > espresso } ; 				# Note que a sintaxe eh case-sensitive, isto eh, maiusculas e minusculas sao 
{ VP > V , NP } ;				# diferenciadas. Nao usar acentos para que o uso em outras plataformas nao 	
{ VP > runs } ;					# corrompa o arquivo. O simbolo inicial possui uma secao propria, iniciada pela palavra
{ VP > barks } ;				   	# "Inicial". Essa secao possui apenas uma linha com o simbolo inicial entre chaves.
{ VP > eats } ;					# A ultima secao vem encabecada pela palavra-chave "Regras"
{ NP > DT , N } ;				# Nas regras de producao, coloca-se o simbolo da esquerda antes
{ V > runs } ;					# do simbolo de ">", que representa a derivacao.
{ V > barks } ;				  	# Os simbolos da direita sao separados por "," e espacos,
{ V > eats } ;				  	# a fim de definir-se a fronteira entre dois simbolos.
{ DT > a } ;				  	# As regras de producao devem seguir as restricoes de uma GLC.
{ DT > the } ;				  	# Linhas em branco entre as secoes e entre os itens nao serao toleradas.
"""
import re
#class Terminais:

#class Variaveis:

#class Inicial:

#sclass Regras:

class Parser:
    f=open('gramatica-exemplo.txt','r')
    readString = f.readline()
   
    match = re.search('^Terminais',readString) 
    if match:
         readString = f.readline()
         p = re.compile("\{\s*(.+)\s*\}")
         matchObj = p.search(readString)
         #print "searchObj.group(0) : ", matchObj.group(0)
         #print "searchObj.group(1) : ", matchObj.group(1)
         terminais = re.split(",\s", matchObj.group(1))
         print terminais
         
    readString = f.readline() 
    match = re.search('^Variaveis',readString) 
    if match:
         readString = f.readline()
         p = re.compile("\{\s*(.+)\s*\}")
         matchObj = p.search(readString)
         #print "searchObj.group(0) : ", matchObj.group(0)
         #print "searchObj.group(1) : ", matchObj.group(1)
         variaveis = re.split(",\s", matchObj.group(1))
         print variaveis
         
    readString = f.readline() 
    match = re.search('^Inicial',readString) 
    if match:
         readString = f.readline()
         p = re.compile("\{\s*(.+)\s*\}")
         matchObj = p.search(readString)
         #print "searchObj.group(0) : ", matchObj.group(0)
         #print "searchObj.group(1) : ", matchObj.group(1)
         inicial = re.split(",\s", matchObj.group(1))
         print inicial
         
    readString = f.readline() 
    match = re.search('^Regras',readString) 
    if match:
         readString = f.readline()
         p = re.compile("\{\s*(.+)\s*> \s*(.+)\}")
         matchObj = p.search(readString)
         #print "searchObj.group(0) : ", matchObj.group(0)
         #print "searchObj.group(1) : ", matchObj.group(1)
         regras = re.split(",\s", matchObj.group(1))
         print regras
    