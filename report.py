from datetime import datetime

def make_report(data, result, change, indicator_name, country_name):

    if change is None:
        change_text = "Неможливо розрахувати"
    else:
        change_text = f"{change:.2f}%"

    table = data.to_html(index=False, border=1)

    report = f"""
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>Звіт з аналізу даних</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 35px;
                color: #222;
            }}
            h1, h2 {{
                color: #245b87;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                padding: 8px;
                border: 1px solid #ccc;
                text-align: left;
            }}
            th {{
                background: #eaf2f8;
            }}
        </style>
    </head>
    <body>
        <h1>Звіт з аналізу економічних даних</h1>
        <p>Дата створення: {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>

        <h2>Параметри аналізу</h2>
        <p>Країна: {country_name}</p>
        <p>Показник: {indicator_name}</p>

        <h2>Результати</h2>
        <p>Середнє значення: {result["Середнє"]:,.2f}</p>
        <p>Максимальне значення: {result["Максимум"]:,.2f}</p>
        <p>Мінімальне значення: {result["Мінімум"]:,.2f}</p>
        <p>Останнє значення: {result["Останнє значення"]:,.2f}</p>
        <p>Зміна за період: {change_text}</p>

        <h2>Таблиця даних</h2>
        {table}

    </body>
    </html>
    """

    return report.encode("utf-8")
