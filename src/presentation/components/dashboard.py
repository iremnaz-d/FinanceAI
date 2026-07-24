import streamlit as st
from src.application.financial_services import DashboardService
import datetime

from src.presentation.components.charts import FinancialVisualizer


class DashboardFeatures:
    def __init__(self):
        self.service = DashboardService()

    def monthly_view(self):
        today = datetime.date.today()

        months = []
        for i in range(24):
            date = today - datetime.timedelta(days = i*30)
            formatted_date = date.strftime('%B %Y')
            if formatted_date not in months:
                months.append(formatted_date)


        with st.container(border = True):
            col1,col2 = st.columns([2,3])
            with col1:
                period = st.selectbox('Choose month: ', months)
                current_month, current_year = period.split()
                current_amount, dif = self.service.get_monthly_comparison(current_month, current_year)

                delta_dif = ""
                value_str = ""
                label_str = f"This month's spending: \n{current_amount} TL"

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
                    st.text(label_str)
                    st.subheader(value_str)

            with col2:
                st.text("")
                st.subheader(f"Top 5 Expenses in {current_month} {current_year}", text_alignment='center')

                with st.container(border=True):

                    df = self.service.get_top_expenses(current_month, current_year)
                    st.dataframe(df, hide_index = True, use_container_width = True, column_config = {
                        'description': 'Description',
                        'amount': st.column_config.NumberColumn('Amount Spent (TL)', format="%.2f ₺"),
                        'category': 'Category'
                    })

            vis = FinancialVisualizer()
            fig = vis.line_burn_rate(current_month, current_year)
            st.plotly_chart(fig, use_container_width=True)










