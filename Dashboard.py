#region IMPORTS
from classes.ui.header import HeaderMenu
from classes.ui.footer import Footer
from classes.ui.pages import Pages
from classes.ui.textelement import TextElement
from classes.ui.metrics import DisplayMetrics
from classes.data.fetchdata import DataConnection
from classes.ui.data import PlotData
import streamlit as st
#endregion

#region PAGE CONFIGURATION
Pages(name="TributoSmart Analytics", icon="📊", page_layout="wide")
HeaderMenu.hide_menu()
#endregion

tab1, tab2 = st.tabs(["ANÁLISE", "DASHBOARD"])
with tab1:
    # region PAGE'S HEADER
    TextElement.set_title("📊 Análise da planilha de tributos")
    TextElement.set_caption("**EMPRESA:** Nova Era Tecnologia LTDA")
    TextElement.write_text("---")
    # endregion

    dataframe = DataConnection.get_tax_dataframe()

    # --- FILTROS LADO A LADO ---
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        # Filtro por ano base
        options = ["Todos"] + sorted(dataframe['ano_base'].dropna().unique().tolist())
        selected = st.selectbox(
            label='ANO BASE',
            placeholder='Selecione um ano base...',
            options=options,
            key='year_selection'
        )

    with col2:
        # Filtro por tributo
        tax_options = ["Todos"] + sorted(dataframe['tributo'].dropna().unique().tolist())
        selected_tax = st.selectbox(
            label='TRIBUTO',
            placeholder='Selecione um tributo...',
            options=tax_options,
            key='tax_selection'
        )

    # Aplicando filtros ao dataframe
    filtered_df = dataframe.copy()

    if selected != "Todos":
        filtered_df = filtered_df[filtered_df['ano_base'] == selected]

    if selected_tax != "Todos":
        filtered_df = filtered_df[filtered_df['tributo'] == selected_tax]

    st.dataframe(filtered_df)

    # region FINAL ANALYSIS
    TextElement.write_text("""
        ## Observações
        ---

        1. **Ano Base:** Refere-se ao ano em que o tributo foi pago ou registrado.
        2. **Tributo:** Tipo de imposto (PIS, COFINS, ICMS, ISS).
        3. **Total Pago:** Valor total pago pelo contribuinte em cada tributo naquele ano.
        4. **Valor Recuperável Estimado:** Estimativa de quanto pode ser recuperado ou compensado.
        5. **Prazo de Recuperação:** Tempo previsto (em meses) para recuperar o valor estimado.
        6. **Juros Estimado:** Valor estimado de juros que incidem sobre o tributo recuperável.
        7. **Valor Líquido a Receber:** Soma do valor recuperável com os juros estimados, representando o montante final esperado.

        ## Insights
        ---

        - O **PIS** aparece nos anos 2014, 2018 e 2022, mostrando crescimento constante no valor pago e recuperável.
        - **COFINS** e **ICMS** também apresentam aumento gradual ao longo dos anos.
        - O **ISS** tem valores menores, mas mantém consistência nos pagamentos e recuperação.
        - O **prazo de recuperação** varia de 12 a 24 meses, refletindo a complexidade e o tempo estimado para compensação ou restituição.
        - O **valor líquido a receber** cresce ano a ano, acompanhado do aumento do tributo pago e dos juros estimados.


    """)

    Footer.footer()

with tab2:
    #region PAGE'S HEADER
    TextElement.set_title("📊 Dashboard de Recuperação Tributária")
    TextElement.set_caption("**EMPRESA:** Nova Era Tecnologia LTDA")
    TextElement.write_text("---")
    #endregion

    #region METRICS DISPLAY
    column1, column2, column3, column4 = st.columns(4, gap="medium")

    with column1:
        total_amount = filtered_df["total_pago"].sum()
        DisplayMetrics(
            ":material/payment: Total Pago",
            value=f"R$ {total_amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            delta=f"{-total_amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            help_icon="Valor total de tributos pagos ao longo dos anos."
        )

    with column2:
        total_amount = filtered_df["recuperavel_estimado"].sum()
        DisplayMetrics(
            ":material/paid: Valor Recuperável Estimado",
            value=f"R$ {total_amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            delta=f"{total_amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            help_icon="Valor estimado a ser recuperado."
        )

    with column3:
        total_amount = filtered_df["juros_estimado"].sum()
        DisplayMetrics(
            ":material/account_balance: Valor de Juros Estimado",
            value=f"R$ {total_amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            delta=f"{total_amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            help_icon="Valor total de juros sobre os créditos a recuperar."
        )

    with column4:
        total_amount = filtered_df["liquido_receber"].sum()
        DisplayMetrics(
            ":material/money_bag: Valor Líquido a receber",
            value=f"R$ {total_amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            delta=f"{total_amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            help_icon="Valor líquido total a ser recebido."
        )
    #endregion

    #region CHARTS DISPLAY
    column1, column2 = st.columns(2, gap="medium")
    with column1:
        with st.container(border=True):
            PlotData.pie_plot(
                dataframe=filtered_df,
                title="Distribuição de tributos",
                names="tributo",
                values="total_pago",
                show=True,
                color="tributo"
            )

    with column2:
        with st.container(border=True):
            tax_content_sorted = filtered_df.sort_values("ano_base")
            PlotData.line_plot(
                tax_content_sorted,
                title="Evolução de pagamentos",
                x="ano_base",
                y="total_pago",
                show=True
            )

    with st.container(border=True):
        PlotData.bar_plot(
            filtered_df,
            x="ano_base",
            y="total_pago",
            color="light blue",
            title="Pagamentos por ano",
            show=True
        )
    #endregion

    #region FOOTER
    Footer.footer()
    #endregion
