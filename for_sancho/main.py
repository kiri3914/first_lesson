import requests
import logging

# Настройка логирования с подробными объяснениями
# Логи сохраняются в файл, вывод в терминал отключен
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/logs.txt',  # Имя файла для сохранения логов
    filemode='w',  # 'w' - перезапись файла, 'a' - добавление в конец
    encoding='utf-8'  # Кодировка для корректного отображения русских символов
)

def explain_request(url, params=None, headers=None):
    """
    Простой сервис для объяснения HTTP запросов и ответов через логи.
    
    Args:
        url: URL для запроса
        params: Параметры запроса (для GET запросов)
        headers: Заголовки запроса
    """
    logging.info("=" * 60)
    logging.info("НАЧАЛО HTTP ЗАПРОСА")
    logging.info("=" * 60)
    
    # Логирование информации о запросе
    logging.info(f"📤 Отправляем GET запрос на: {url}")
    
    if headers:
        logging.info(f"📋 Заголовки запроса: {headers}")
    
    if params:
        logging.info(f"🔍 Параметры запроса (query string): {params}")
        logging.info("💡 ВАЖНО: Для GET запросов используем 'params', а не 'data'")
        logging.info("💡 'params' добавляет параметры в URL (?key=value)")
        logging.info("💡 'data' используется для POST запросов (тело запроса)")
    
    try:
        # Выполняем запрос
        logging.info("⏳ Выполняем запрос...")
        response = requests.get(url, headers=headers, params=params)
        
        logging.info("=" * 60)
        logging.info("ПОЛУЧЕН ОТВЕТ ОТ СЕРВЕРА")
        logging.info("=" * 60)
        
        # Основная информация об ответе
        logging.info(f"✅ Статус код ответа: {response.status_code}")
        
        # Объяснение статус кодов
        if response.status_code == 200:
            logging.info("💡 Статус 200: Запрос успешно выполнен (OK)")
        elif response.status_code == 400:
            logging.info("⚠️  Статус 400: Неверный запрос (Bad Request)")
            logging.info("💡 Возможные причины: неправильные параметры, формат данных")
        elif response.status_code == 404:
            logging.info("⚠️  Статус 404: Страница не найдена (Not Found)")
        elif 300 <= response.status_code < 400:
            logging.info("💡 Статус 3xx: Перенаправление (Redirect)")
        elif response.status_code >= 500:
            logging.info("❌ Статус 5xx: Ошибка сервера (Server Error)")
        
        # URL ответа (может отличаться из-за редиректов)
        logging.info(f"🌐 Финальный URL: {response.url}")
        if response.url != url:
            logging.info("💡 URL изменился из-за редиректа")
        
        # История редиректов
        if response.history:
            logging.info(f"🔄 История редиректов: {len(response.history)} перенаправлений")
            for i, hist_response in enumerate(response.history, 1):
                logging.info(f"   {i}. {hist_response.status_code} -> {hist_response.url}")
        else:
            logging.info("🔄 Редиректов не было")
        
        # Заголовки ответа
        logging.info(f"📋 Заголовки ответа: {dict(response.headers)}")
        
        # Тип контента
        content_type = response.headers.get('Content-Type', 'не указан')
        logging.info(f"📄 Тип контента: {content_type}")
        
        # Проверка типа контента перед парсингом JSON
        if 'application/json' in content_type:
            logging.info("💡 Ответ в формате JSON - можно парсить")
            try:
                json_data = response.json()
                logging.info(f"📦 JSON данные: {json_data}")
            except ValueError as e:
                logging.error(f"❌ Ошибка парсинга JSON: {e}")
        else:
            logging.info("💡 Ответ НЕ в формате JSON (вероятно HTML/текст)")
            logging.info("💡 Не пытаемся парсить как JSON, чтобы избежать ошибки")
            logging.info(f"📝 Текст ответа (первые 500 символов): {response.text[:500]}")
        
        # Дополнительная информация
        logging.info(f"⏱️  Время выполнения запроса: {response.elapsed}")
        logging.info(f"🔤 Кодировка ответа: {response.encoding}")
        logging.info(f"🍪 Cookies: {response.cookies}")
        logging.info(f"🔄 Это редирект: {response.is_redirect}")
        logging.info(f"🔄 Это постоянный редирект: {response.is_permanent_redirect}")
        
        # Проверка успешности запроса
        response.raise_for_status()  # Вызовет исключение для статусов 4xx и 5xx
        logging.info("✅ Запрос выполнен успешно!")
        
    except requests.exceptions.HTTPError as e:
        logging.error(f"❌ HTTP ошибка: {e}")
        logging.error(f"💡 Статус код: {response.status_code}")
        logging.error(f"💡 Ответ сервера: {response.text[:500]}")
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Ошибка запроса: {e}")
    except Exception as e:
        logging.error(f"❌ Неожиданная ошибка: {e}")
    
    logging.info("=" * 60)
    logging.info("КОНЕЦ ОБРАБОТКИ ЗАПРОСА")
    logging.info("=" * 60)


# Пример 1: Запрос к API, который возвращает JSON
logging.info("\n" + "="*60)
logging.info("ПРИМЕР 1: Запрос к API с JSON ответом")
logging.info("="*60)
explain_request("https://dog.ceo/api/breeds/image/random")

# Пример 2: Запрос к Google с параметрами (исправленная версия)
logging.info("\n" + "="*60)
logging.info("ПРИМЕР 2: Запрос к Google с параметрами поиска")
logging.info("="*60)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
params = {
    "q": "python"
}
explain_request("https://www.google.com/search", params=params, headers=headers)