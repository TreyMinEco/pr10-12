import streamlit as st
import pandas as pd

from data import WorldBankData
from analysis import DataAnalysis
from charts import make_line_chart, make_bar_chart
from report import make_report


st.set_page_config(page_title="World Bank Dashboard", layout="wide")

countries = {
    "Україна": "UKR",
    "Польща": "POL",
    "Німеччина": "DEU",
    "Франція": "FRA",
    "США": "USA",
    "Японія": "JPN",
    "Китай": "CHN",
    "Італія": "ITA",
    "Іспанія": "ESP",
    "Канада": "CAN"
}

indicators = {
    "ВВП (дол. США)": "NY.GDP.MKTP.CD",
    "ВВП на душу населення": "NY.GDP.PCAP.CD",
    "Населення": "SP.POP.TOTL",
    "Інфляція (%)": "FP.CPI.TOTL.ZG",
    "Безробіття (%)": "SL.UEM.TOTL.ZS"
}

st.title("Аналіз економічного розвитку країн світу")

st.sidebar.header("Налаштування")
country_name = st.sidebar.selectbox("Оберіть країну", list(countries.keys()))
indicator_name = st.sidebar.selectbox("Оберіть показник", list(indicators.keys()))
years = st.sidebar.slider("Період аналізу", min_value=1990, max_value=2025, value=(2000, 2024))
compare_names = st.sidebar.multiselect("Країни для порівняння", list(countries.keys()), default=["Україна", "Польща", "Німеччина"])

start_year, end_year = years
country_code = countries[country_name]
indicator_code = indicators[indicator_name]

world_bank = WorldBankData()
analyzer = DataAnalysis()

with st.spinner("Завантаження даних"):
    data = world_bank.get_data(country_code, indicator_code, start_year, end_year)

if not world_bank.check_data(data):
    st.warning("Дані не знайдено")
else:
    st.subheader(f"{indicator_name}: {country_name}")

    result = analyzer.analyze_data(data)
    change = analyzer.calculate_change(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Середнє значення", f"{result['Середнє']:,.2f}")
    col2.metric("Максимум", f"{result['Максимум']:,.2f}")
    col3.metric("Мінімум", f"{result['Мінімум']:,.2f}")

    if change is not None:
        st.metric("Зміна за обраний період", f"{change:.2f}%")
    else:
        st.info("Зміну показника неможливо розрахувати для цього періоду.")

    st.subheader("Динаміка показника")
    line_chart = make_line_chart(data, indicator_name)
    st.plotly_chart(line_chart, use_container_width=True)
    st.subheader("Таблиця даних")
    st.dataframe(data, use_container_width=True, hide_index=True)
    st.subheader("Порівняння країн")

    if compare_names:
        compare_codes = [countries[name] for name in compare_names]

        with st.spinner("Завантаження даних"):
            compare_data = world_bank.get_many_countries(compare_codes, indicator_code, start_year, end_year)

        if not compare_data.empty:
            compare_table = analyzer.compare_countries(compare_data)
            bar_chart = make_bar_chart(compare_table, indicator_name)
            st.plotly_chart(bar_chart, use_container_width=True)
            st.dataframe(compare_table, use_container_width=True, hide_index=True)
        else:
            compare_table = pd.DataFrame()
            st.info("Немає даних для порівняння обраних країн")
    else:
        compare_data = pd.DataFrame()
        compare_table = pd.DataFrame()
        st.info("Оберіть хоча б одну країну для порівняння")

    st.subheader("Збереження результатів")
    csv_file = data.to_csv(index=False).encode("utf-8-sig")
    json_file = data.to_json(orient="records", force_ascii=False, indent=4).encode("utf-8")

    col1, col2 = st.columns(2)
    col1.download_button("Завантажити CSV", data=csv_file, file_name="world_bank_data.csv", mime="text/csv")
    col2.download_button("Завантажити JSON", data=json_file, file_name="world_bank_data.json", mime="application/json")

    data.to_csv("exports/world_bank_data.csv", index=False, encoding="utf-8")
    data.to_json("exports/world_bank_data.json",orient="records",force_ascii=False,indent=4)

    report_file = make_report(data, result, change, indicator_name, country_name)

    st.download_button("Завантажити HTML-звіт", data=report_file, file_name="world_bank_report.html", mime="text/html")