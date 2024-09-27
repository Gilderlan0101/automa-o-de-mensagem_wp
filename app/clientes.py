import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pyautogui

class MensagemManha:
    def __init__(self):
        pass

    def noticia(self):
        header = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://www.giroemibirataia.com.br/'
        response = requests.get(url, headers=header)

        if response.status_code == 200:
            response.encoding = 'utf-8'  # Define a codificação como UTF-8
            soup = BeautifulSoup(response.text, 'html.parser')
           
            # Buscando os títulos, resumos e links das notícias
            posts = soup.find_all('div', class_='post')
            noticias = []  # Lista para armazenar títulos, resumos e links

            for post in posts:
                # Título
                titulo = post.find('h2', class_='post-title entry-title')
                if titulo:
                    titulo_text = titulo.get_text(separator=' ', strip=True)

                    # Link
                    link = titulo.find('a')['href']  # Obtém o link do título
                
                # Resumo
                resumo = post.find('div', class_='resumo').find('span')
                if resumo:
                    resumo_text = resumo.get_text(strip=True)
                    
                    # Adiciona o título, resumo e link à lista
                    noticias.append((titulo_text, resumo_text, link))

            # Verificar se as notícias já foram enviadas
            novas_noticias = self.verificar_noticias(noticias)
            return novas_noticias  # Retorna a lista de notícias novas
        else:
            print(f"Falha ao acessar o site: {response.status_code}")
            return []

    def verificar_noticias(self, noticias):
        try:
            with open('noticia.txt', 'r') as file:
                noticias_enviadas = file.read().splitlines()  # Lê notícias já enviadas
        except FileNotFoundError:
            noticias_enviadas = []

        novas_noticias = []
        for titulo, resumo, link in noticias:
            noticia_completa = f"Título: {titulo}\nResumo: {resumo}\nLink: {link}"
            if noticia_completa not in noticias_enviadas:
                novas_noticias.append((titulo, resumo, link))  # Adiciona novas notícias
                with open('noticia.txt', 'a') as file:
                    file.write(noticia_completa + '\n')  # Adiciona ao arquivo de enviadas

        return novas_noticias

class HorasMensagem:
    def enviar_whatsapp(self, noticias):
        """Usa pyautogui para simular envio de mensagens no WhatsApp Web"""
        for titulo, resumo, link in noticias:
            mensagem = f"Título: {titulo}\nResumo: {resumo}\nLink: {link}"
            print(f"Enviando mensagem:\n{mensagem}\n")

            # Simula a digitação e envio da mensagem no WhatsApp com intervalo de 0.1 segundos entre caracteres
            pyautogui.write(mensagem.split('\n')[0], interval=0.2)  # Escreve o título mais devagar
            pyautogui.press('enter')  # Envia o título
            pyautogui.hotkey('shift', 'enter')  # Muda para nova linha
            pyautogui.write(mensagem.split('\n')[1], interval=0.2)  # Escreve o resumo mais devagar
            pyautogui.press('enter')  # Envia o resumo
            pyautogui.hotkey('shift', 'enter')  # Muda para nova linha
            pyautogui.write(mensagem.split('\n')[2], interval=0.1)  # Escreve o link mais devagar
            pyautogui.press('enter')  # Envia o link
            time.sleep(600)  # Pequena pausa antes de enviar a próxima mensagem

def agendar_envio():
    """Verifica o horário e envia mensagens conforme programado."""
    mensagem_manha = MensagemManha()
    horas_mensagem = HorasMensagem()
    
    while True:
        hora_atual = datetime.now()
        horas_formatada = hora_atual.strftime('%H:%M')
        print(f"Hora atual: {horas_formatada}")  # Debug: Imprime a hora atual
        
        # Define os horários de envio
        if horas_formatada in ['09:14', '12:00', '18:00', '22:00']:
            print("Hora de enviar mensagens!")  # Debug: Indica que é hora de enviar
            noticias = mensagem_manha.noticia()  # Obtém as notícias
            if noticias:  # Se houver notícias novas
                horas_mensagem.enviar_whatsapp(noticias)  # Envia as notícias
            time.sleep(60)  # Espera um minuto antes de verificar novamente
        else:
            time.sleep(3)  # Espera 3 segundos antes de verificar o horário novamente

# Iniciar agendamento
agendar_envio()
