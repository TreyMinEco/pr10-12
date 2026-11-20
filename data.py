import requests
import pandas as pd

class WorldBankData:

    def get_data(self, country, indicator, start_year, end_year):

        url = (
            f"https://api.worldbank.org/v2/country/{country}/indicator/"
            f"{indicator}"
        )

        params = {
            "format": "json",
            "date": f"{start_year}:{end_year}",
            "per_page": 1000
        }

        try:
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            result = response.json()

            if not isinstance(result, list) or len(result) < 2:
                return pd.DataFrame()

            if result[1] is None:
                return pd.DataFrame()

            rows = []

            for item in result[1]:
                if item["value"] is not None:
                    rows.append({
                        "Країна": item["country"]["value"],
                        "Код країни": item["countryiso3code"],
                        "Рік": int(item["date"]),
                        "Значення": item["value"]
                    })

            data = pd.DataFrame(rows)

            if data.empty:
                return data

            data = data.sort_values("Рік").reset_index(drop=True)
            return data

        except requests.exceptions.RequestException as error:
            print("Помилка підключення до API:", error)
            return pd.DataFrame()

        except (ValueError, KeyError, TypeError) as error:
            print("Помилка обробки даних:", error)
            return pd.DataFrame()

    def get_many_countries(self, countries, indicator, start_year, end_year):

        all_data = []

        for country in countries:
            data = self.get_data(country, indicator, start_year, end_year)

            if not data.empty:
                all_data.append(data)

        if len(all_data) == 0:
            return pd.DataFrame()

        return pd.concat(all_data, ignore_index=True)

    def check_data(self, data):
        return not data.empty
