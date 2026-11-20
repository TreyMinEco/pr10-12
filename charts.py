import plotly.express as px

def make_line_chart(data, indicator_name):
    chart = px.line(data, x="Рік", y="Значення", markers=True, title=f"Динаміка показника: {indicator_name}")
    chart.update_layout(xaxis_title="Рік", yaxis_title="Значення", template="plotly_white")

    return chart

def make_bar_chart(data, indicator_name):
    chart = px.bar(data, x="Країна", y="Значення", color="Країна", title=f"Порівняння країн: {indicator_name}")
    chart.update_layout(xaxis_title="Країна", yaxis_title="Значення", template="plotly_white", showlegend=False)

    return chart
