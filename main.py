import fake_useragent
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from database import c, db, clear_database

url = 'https://www.rsb.ru/press-center/news/2024/'
url_main= 'https://www.rsb.ru'
name_bank ='Банк Русский Стандарт'
# Создание fake useragent, чтобы избегать ошибки <Response [403]>
random_user_agent = fake_useragent.UserAgent().random
header = {'user-agent': random_user_agent}

# Получение ответа от сайта
response = requests.get(url, headers=header)

# Проверка на успешный ответ
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Получаем все блоки новостей
    news_items = soup.find_all('div', class_='info-block__date-item')

    # Определяем дату 30 дней назад
    thirty_days_ago = datetime.now() - timedelta(days=30)
    clear_database()
    for item in news_items:
        data = item.find('time').text.strip()
        news_date = datetime.strptime(data, '%d.%m.%Y')  # Предполагаем, что дата в формате 'дд.мм.гггг'
        
        # Проверяем, если новость за последние 30 дней
        if news_date >= thirty_days_ago:
            # Получаем заголовок новости и ссылку
            title_link = item.find('a', class_='info-block__date-item-link').text.strip()
            href = item.find('a', class_='info-block__date-item-link')['href']  # Извлечение href
            #формирование ссылки на саму новость
            href_real = url_main + href
            #Получение из нее текста
            response_text = requests.get(href_real, headers=header)
            soup_text = BeautifulSoup(response_text.text, 'html.parser')
            text_news = soup_text.find('div', class_ = 'detail_text press_detail_text').text.strip()
            text_news = re.sub(r'\s+', ' ', text_news)
            c.execute("INSERT INTO rsb(bank, title, news, data) VALUES (?, ?, ?, ?)", (name_bank, title_link, text_news, data,))
            db.commit()       
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")
db.close() 
