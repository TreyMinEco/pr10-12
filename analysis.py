import pandas as pd

class DataAnalysis:
    def analyze_data(self, data):
        if data.empty:
            return None
        
        values = data["Значення"]
        result = {
            "Середнє": values.mean(),
            "Максимум": values.max(),
            "Мінімум": values.min(),
            "Останнє значення": values.iloc[-1]
        }

        return result

    def calculate_change(self, data):
        if data.empty or len(data) < 2:
            return None

        first = data["Значення"].iloc[0]
        last = data["Значення"].iloc[-1]

        if first == 0:
            return None

        change = (last - first) / abs(first) * 100
        return change

    def compare_countries(self, data):
        if data.empty:
            return pd.DataFrame()

        result = data.sort_values("Рік").groupby("Країна", as_index=False).tail(1)
        result = result[["Країна", "Рік", "Значення"]]
        result = result.sort_values("Значення", ascending=False)

        return result.reset_index(drop=True)
