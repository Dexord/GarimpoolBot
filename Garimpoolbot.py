import time
import requests
import json

url_api = "https://garimpool.com.br/api/blocks"
bot_token = '1767333275:AAFGyhRhHQnhQc2fGdV_09fdDm6Ffk8NZ4c'
bot_chatID = '130872481'
#bot_chatID =  "-1001462267074" #grupo garimpool
matured_inicial = 252

def telegram_bot_sendtext(bot_message):      
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def telegram_bot_sendtext_silenciada(bot_message):      
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message + "&disable_notification=True"
    response = requests.get(send_text)
    return response.json()

def envia_novo_bloco(ultimo_bloco): 
  link_ethscan = "https://etherscan.io/block/" + str(ultimo_bloco["height"])
  recompensa = int(ultimo_bloco["reward"])/1000000000000000000-1
  
  contador = json.loads(requests.get("https://garimpool.com.br/api/stats").text)
  contador = contador['nodes'][0]['height']

  mensagem = "*É " +str(contador) + " PÁPÁPÁ !!*\n" + "*Novo bloco maturado!!!!*\n\n" +"Recompensa do Bloco => " + str(recompensa) + "\nAltura do Bloco:" + str(altura_max) + "\nHash do bloco => " + "[" + ultimo_bloco["hash"] +"](" + link_ethscan + ")\n"

  query1 = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + mensagem
  try:
    requests.get(query1)
  except:
    print("Erro no envio da mensagem.")
  return

def envia_novo_uncle(ultimo_bloco): 
  link_ethscan = "https://etherscan.io/uncle/" + ultimo_bloco["hash"]
  recompensa = int(ultimo_bloco["reward"])/1000000000000000000-1
  mensagem = "*Novo bloco maturado!!!!*\n\n" + "Mas é uncle, tem recompensa menor!\n" +"\nRecompensa do Bloco => " + str(recompensa) + "\nHash do bloco => " + [ultimo_bloco["hash"]](link_ethscan) + "\n"
  
  query1 = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + mensagem
  try:
    requests.get(query1)
  except:
    print("Erro no envio da mensagem.")
  return


def envia_novo_bloco1(ultimo_bloco): 
  if bool(ultimo_bloco["uncle"]): #eh uncle
    altura_uncle = int(ultimo_bloco["uncleHeight"])
    link_ethscan = "https://etherscan.io/uncle/" + ultimo_bloco["hash"]
    recompensa = int(ultimo_bloco["reward"])/1000000000000000000-1
    mensagem = "*Novo bloco maturado!!!!*\n\n" + "Mas é uncle, tem recompensa menor!\n" +"\nRecompensa do Bloco => " + str(recompensa) + "\nHash do bloco => " + [ultimo_bloco["hash"]](link_ethscan) + "\n"
  else: #é normal
    altura_max = int(ultimo_bloco["height"])
    link_ethscan = "https://etherscan.io/block/" + str(ultimo_bloco["height"])
    recompensa = int(ultimo_bloco["reward"])/1000000000000000000-1
    
    contador = json.loads(requests.get("https://garimpool.com.br/api/stats").text)
    contador = contador['nodes'][0]['height']

    mensagem = "*É " +str(contador) + " PÁPÁPÁ !!*\n" + "*Novo bloco maturado!!!!*\n\n" +"Recompensa do Bloco => " + str(recompensa) + "\nAltura do Bloco:" + str(altura_max) + "\nHash do bloco => " + "[" + ultimo_bloco["hash"] +"](" + link_ethscan + ")\n"
  
  #mensagem = "Novo *bloco* encontrado!\n" + "Altura do bloco => " + str(dados_bloco["Altura"]) +"\nRecompensa do Bloco => " + str(dados_bloco["Recompensa"]) + "\nVariância => " + str(dados_bloco["Variancia"])
  query1 = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + mensagem
  try:
    requests.get(query1)
  except:
    print("Erro no envio da mensagem.")

  return

def CalcIncrVar():
  try:
    stats = json.loads(requests.get("https://garimpool.com.br/api/stats").text)
  except:
    return var_atual
  tempo_bloco = 13
  tempo_verific = 15*10
  hr_rede = 576*(10**12)
  hr_pool = float(stats["hashrate"])
  print("Hashrate da Pool: "+ str(hr_pool/1000000000) + " GH/s")

  tempo_quebra_atual = int((hr_rede/hr_pool)*tempo_bloco)
  print("Tempo atual pra quebrar: " + str(tempo_quebra_atual) + " segs. Em horas:" + str(tempo_quebra_atual/(60*60)))
  incremento_var = tempo_verific/tempo_quebra_atual
  return incremento_var



def checa_novo_bloco():
  resposta = requests.get(url_api)
  try:
    resposta = json.loads(resposta.text)
  except:
    print("Servidor da API offline!")
    return 0
  ultimo_bloco = resposta["matured"][0]
  if int(ultimo_bloco["height"]) > altura_max:# or int(ultimo_bloco["uncleHeight"]) > altura_uncle:
    return ultimo_bloco
  else: 
    #print("Sem novos blocos")
    return 0

variancia = 66
contador_variance = 10

while 1:
  bloco = checa_novo_bloco()
  if bloco != 0:

    if bool(bloco["uncle"]): #eh uncle
      altura_uncle = int(bloco["uncleHeight"])
      envia_novo_uncle(bloco)
    else:
      altura_max = int(bloco["height"])
      envia_novo_bloco(bloco)
  #else:
    #telegram_bot_sendtext_silenciada("nada novo sob o sol")
  bloco = 0
  contador_variance+=1
  if contador_variance >= 10:    
    try:
      incremento = CalcIncrVar()
    except:
      incremento = inc_ant
    variancia = variancia + incremento*100
    print("Variancia do round: " + str(variancia) + "%")
    inc_ant=incremento
    contador_variance = 0
  time.sleep(15)
