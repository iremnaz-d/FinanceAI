import streamlit as st
from src.application.financial_services import DashboardService
import datetime


class DashboardFeatures:
    def __init__(self):
        self.service = DashboardService()
        self.col1, self.col2, self.col3= st.columns(3)

    def monthly_difference(self):
        today = datetime.date.today()

        months = []
        for i in range(24):
            date = today - datetime.timedelta(days = i*30)
            formatted_date = date.strftime('%B %Y')
            if formatted_date not in months:
                months.append(formatted_date)


        with self.col1:
            period = st.selectbox('Choose month: ', months)
            current_month, current_year = period.split()
            current_amount, dif = self.service.get_monthly_comparison(current_month, current_year)

            delta_dif = ""
            value_str = ""
            label_str = f"This month's spending: {current_amount} TL"

            if dif >= 0:
                delta_dif = "-" + str(dif) + "%"
                value_str = f"You spent :red[%{dif}] more than last month"
            else:
                dif = abs(dif)
                delta_dif = "+" + str(dif) + "%"
                value_str = f"You spent :green[%{dif}] less than last month"

            """st.markdown(f":gray-background[### {label_str}\n## {value_str}]")
            st.metric(label="", value="", delta=delta_dif)"""
            with st.container(border=True):
                st.caption(label_str)
                st.subheader(value_str)





