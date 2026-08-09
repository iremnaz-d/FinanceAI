import os

import streamlit as st

from src.application.categorization_service import Categorizer, CategoryService
from src.application.financial_services import DashboardService, FinancialService
import datetime

from src.presentation.components.charts import FinancialVisualizer


class DashboardFeatures:
    def __init__(self):
        self.service = DashboardService()
        self.financial_service = FinancialService()
        self.category_service = CategoryService()

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
                label_str = f"💸 This month's spending: \n{current_amount} TL"

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
                    st.info(label_str)
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

        with st.container(border = True):
            df = self.service.get_predicted_expenses(current_month, current_year)
            df['category'] = df['category'].str.removesuffix(" (Predicted)")
            st.subheader(f"AI automatically categorized {len(df)} transactions this month", text_alignment='center')
            st.divider()

            col3, col4 ,col5, col6= st.columns([1,1,3,1])
            with col4:
                current_dir = os.path.dirname(__file__)
                image_path = os.path.join(current_dir, "computer_image.png")
                st.image(image_path, width = 100)
            with col5:
                st.write("")
                st.warning("💡 You can help me improve my prediction skills by correcting my mistakes in the category column below!")

            # st.dataframe(df, hide_index=True, column_config={
            #     'description': 'Description',
            #     'amount': st.column_config.NumberColumn('Amount Spent (TL)', format="%.2f ₺"),
            #     'category': 'Category'
            # })
            category_list = self.category_service.get_category_list()
            edited_df = st.data_editor(df, hide_index = True, disabled = ['amount', 'description'], column_config = {
                'id':None,
                'description':'Description',
                'amount': st.column_config.NumberColumn('Amount Spent (TL)', format="%.2f ₺"),
                'category': st.column_config.SelectboxColumn(
                    'Category',
                    options = category_list,
                    required = True
                )
            })

            col7, col8, col9 = st.columns([2,3,1])
            with col9:
                if st.button("Approve corrections", type = 'primary', use_container_width = True):
                    changed_df = edited_df[df['category'] != edited_df['category']]

                    if not changed_df.empty:
                        self.financial_service.update_transaction_category(changed_df)
                        st.cache_data.clear()
                        st.rerun()

            col10, col11, col12 = st.columns([2,3,1])

            with col10:
                category = st.text_input("Create a new Category name:")
                if st.button("➕ Add Category", type="secondary"):
                    if category.strip():
                        if self.category_service.add_new_category(category):
                            st.success("✅ Category is created successfully.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("This category already exists.")
                    else:
                        st.error("Please enter a category name.")

            with col11:
                category_list = self.category_service.get_category_list()
                category = st.selectbox("Delete a Category: ", category_list)

                if st.button("🗑️ Delete", type="secondary"):
                    if self.category_service.delete_category(category):
                        st.success("✅ Category is deleted successfully.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("This category does not exist.")












