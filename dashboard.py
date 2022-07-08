import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)

    return data


@st.cache(allow_output_mutation=True)
def clear_data(data):
    data_clear = data.dropna(subset=['id'])
    data_clear = data_clear.drop_duplicates(subset='id', keep='last').reset_index(drop=True)
    data_clear = data_clear.drop(15870)
    data_clear['date'] = pd.to_datetime(data_clear['date'], format='%Y-%m-%d')

    return data_clear


@st.cache(allow_output_mutation=True)
def data_transform(data_cleaned):
    data_cleaned['month'] = data_cleaned['date'].dt.month
    data_cleaned['year'] = data_cleaned['date'].dt.year.astype(str)

    data_cleaned['season'] = data_cleaned['month'].apply(lambda x: 'spring' if (x >= 3) & (x <= 5) else
    'summer' if (x >= 6) & (x <= 8) else
    'fall' if (x >= 9) & (x <= 11) else
    'winter')
    data_cleaned['yr_old'] = data_cleaned['yr_built'].apply(lambda x: 'old' if (x <= 1955) else 'new')
    data_cleaned['basement'] = data_cleaned['sqft_basement'].apply(lambda x: 'yes' if (x != 0) else 'no')
    data_cleaned['state'] = data_cleaned['condition'].apply(lambda x: 'good' if (x >= 3) else 'bad')
    data_cleaned['remodeling'] = data_cleaned['yr_renovated'].apply(lambda x: 'yes' if (x != 0) else 'no')
    data_cleaned['view_condition'] = data_cleaned['view'].apply(lambda x: 'good' if (x >= 2) else 'bad')
    data_cleaned['amount_bedrooms'] = data_cleaned['bedrooms'].apply(lambda x: 'many' if (x >= 3) else 'little')
    data_cleaned['view_waterfront'] = data_cleaned['waterfront'].apply(lambda x: 'yes' if (x!=0) else 'no')

    return data_cleaned

@st.cache(allow_output_mutation=True)
def buy_data(data_transformed):
    resp01 = data_transformed.dropna(subset=['id'])

    price_median = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()

    resp01 = pd.merge(resp01, price_median, on='zipcode', how='inner')

    for i in range(len(resp01)):
        if ((resp01.loc[i, 'price_x'] < resp01.loc[i, 'price_y']) & (resp01.loc[i, 'condition'] > 2)):
            resp01.loc[i, 'status'] = 'compra'
        else:
            resp01.loc[i, 'status'] = 'nao_compra'

    resp01.rename(columns={'price_x': 'price'}, inplace=True)
    resp01.rename(columns={'price_y': 'price_mediana'}, inplace=True)

    resp01 = resp01[
        ['id','zipcode','season','price','price_mediana','condition','lat','long','view_condition','basement','bathrooms','bedrooms','status']].copy()

    return resp01

@st.cache(allow_output_mutation=True)
def sale_data(data_buy):
    resp02 = data_buy.dropna(subset=['id'])

    resp02 = resp02[resp02['status'] == 'compra'].copy()

    price_median2 = resp02[['price', 'zipcode', 'season']].groupby(['zipcode', 'season']).median('price').reset_index()

    resp02 = pd.merge(resp02, price_median2, on=['zipcode', 'season'], how='inner')

    for i in range(len(resp02)):
        resp02.loc[i, 'seasonality'] = 1.3 if (resp02.loc[i, 'price_x'] < resp02.loc[i, 'price_y']) else 1.1

    for i in range(len(resp02)):
        resp02.loc[i, 'price_sell'] = resp02.loc[i, 'price_x'] * resp02.loc[i, 'seasonality']
        resp02.loc[i, 'profit'] = resp02.loc[i, 'price_sell'] - resp02.loc[i, 'price_x']

    resp02.rename(columns={'price_x': 'price'}, inplace=True)
    resp02.rename(columns={'price_y': 'price_median_season'}, inplace=True)

    resp02 = resp02[
        ['id', 'zipcode','view_condition','basement','bathrooms','bedrooms','price_median_season', 'season', 'price', 'price_sell', 'profit']].copy()

    return resp02

@st.cache(allow_output_mutation=True)
def map_opportunities(data_buy):
    fig = px.scatter_mapbox(
        data_buy,
        lat='lat',
        lon='long',
        color='status',
        size='price',
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=10)

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

    return fig

@st.cache(allow_output_mutation=True)
def hypothesis_1_2(data_transformed):
    house_waterfront = data_transformed[['price', 'view_waterfront']].groupby('view_waterfront').mean().reset_index()
    hip1 = px.bar(house_waterfront, y='price', x='view_waterfront', color='view_waterfront',
                  template='simple_white', labels={"view_waterfront": 'Vista para água'},
                  title='Imóveis com vista para água, são 3x mais valorizados.')

    hip1.update_layout(showlegend=False)

    yr_old = data_transformed[['price', 'yr_old']].groupby('yr_old').mean().reset_index()
    hip2 = px.bar(yr_old, y='price', x='yr_old', color='yr_old',
                  template='simple_white', labels={"yr_old": 'Ano de construção'},
                  title='O ano de construção interfere pouco na valorização do imóvel')

    hip2.update_layout(showlegend=False)

    return hip1, hip2


@st.cache(allow_output_mutation=True)
def hypothesis_3_4(data_transformed):
    basement_area = data_transformed[['sqft_lot', 'basement']].groupby('basement').mean().reset_index()
    hip3 = px.bar(basement_area, y='sqft_lot', x='basement', color='basement',
                  template='simple_white', labels={"basement": 'Imóveis com porão'},
                  title='Casas sem porão possuem uma área total 20% maior ')

    hip3.update_layout(showlegend=False)

    yoy = data_transformed[['price', 'year']].groupby('year').sum().reset_index()
    hip4 = px.bar(yoy, y='price', x='year', color='year',
                  template='simple_white', labels={"year": 'Preço dos imóveis'},
                  title='Há uma queda no preço dos imóveis do ano de 2014 para o 2015')

    hip4.update_layout(showlegend=False)

    return hip3, hip4


@st.cache(allow_output_mutation=True)
def hypothesis_5_6(data_transformed):
    bathrooms_price = data_transformed[['month', 'price', 'bathrooms']].groupby(['month', 'bathrooms']).sum(
        'price').reset_index()
    bathrooms_price2 = bathrooms_price[bathrooms_price.bathrooms == 3]

    hip5 = px.line(bathrooms_price2, y='price', x = 'month', labels = {"month": 'Meses'},
                     title = 'Há decaimentos e crescimentos, no preço, com o passar dos meses')

    hip5.update_layout(showlegend=False)

    state_houses = data_transformed[['price', 'state']].groupby('state').mean().reset_index()
    hip6 = px.bar(state_houses, y='price', x='state', color='state',
              template='simple_white', labels={'state': 'Condições do imóvel'},
              title='Imóveis em boas condições são 62% mais caros')

    hip6.update_layout(showlegend=False)

    return hip5, hip6

@st.cache(allow_output_mutation=True)
def hypothesis_7_8(data_transformed):
    remodeling_houses = data_transformed[['price', 'remodeling']].groupby('remodeling').mean().reset_index()

    hip7 = px.bar(remodeling_houses, y='price', x='remodeling', color='remodeling',
                  template='simple_white', labels={'remodeling': 'Imóveis reformados'},
                  title='Os imóveis que ja foram reformados, tem um aumento de 40% preço')

    hip7.update_layout(showlegend=False)

    basement_price = data_transformed[['price', 'basement']].groupby('basement').mean().reset_index()
    hip8 = px.bar(basement_price, y='price', x='basement', color='basement',
                  template='simple_white', labels={'basement': 'Imóveis com porão'},
                  title='Imóveis com porão são 30% mais valorizados')

    hip8.update_layout(showlegend=False)

    return hip7, hip8

@st.cache(allow_output_mutation=True)
def hypothesis_9_10(data_transformed):
    view_good = data_transformed[['price', 'view_condition']].groupby('view_condition').mean().reset_index()
    hip9 = px.bar(view_good, y='price', x='view_condition', color='view_condition',
    template = 'simple_white', labels = {'view_condition': 'Qualidade da vista'},
                                        title = 'Imóveis com boa vista, são quase duas vezes (91%) mais valorizados')

    hip9.update_layout(showlegend=False)

    bedrooms_houses = data_transformed[['price', 'amount_bedrooms']].groupby('amount_bedrooms').mean().reset_index()
    hip10 = px.bar(bedrooms_houses, y='price', x='amount_bedrooms', color='amount_bedrooms',
                            template ='simple_white', labels={'amount_bedrooms': 'Classificação da quantidade de quartos'},
                            title = 'Imóveis com maior quantidade de quartos são 40% mais valorizados')

    hip10.update_layout(showlegend=False)

    return hip9, hip10

if __name__ == '__main__':

    # Título e descrições
    st.sidebar.title('Encontre os melhores imóveis - House Rocket (Insights)')
    st.sidebar.markdown(
        'A criação do aplicativo, é baseada na exibição dos resultados do projeto elaborado pela Comunidade DS, com o intuito de fixação dos conteúdos ensinados, no decorrer do módulo "Python do zero ao DS". Projeto este, construído com base em uma análise nas instruções de um post do blog Seja um Data Scientist, feita com o Kings County Dataset da Kaggle. O código e demais informações, estão hospedados no meu repositório do GitHub.')
    st.sidebar.markdown(
        'A House Rocket é uma plataforma digital americana que tem como modelo de negócio, a compra e a venda de imóveis usando tecnologia. Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita.')
    st.sidebar.markdown('Entretanto, as casas possuem muitos atributos que as tornam mais ou menos atrativas aos compradores e vendedores e a localização e o período do ano também podem influenciar os preços.')
    st.sidebar.markdown('Portanto, o meu trabalho, como estudante, de Data Scientist é responder as seguintes perguntas:')
    st.sidebar.markdown('1. Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?')
    st.sidebar.markdown('2. Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?')

    # ETL
    path = 'kc_house_data.csv'

    # Load data
    data = get_data(path)

    # Transform data
    data_cleaned = clear_data(data)
    data_transformed = data_transform(data_cleaned)

    # Carge data
    data_buy = buy_data(data_transformed)
    data_sale = sale_data(data_buy)

    # Map
    st.header('Oportunidades Imobiliárias')
    st.write(
        'No mapa abaixo, é possível identicar todos os imóveis disponíveis para compra. Em azul, encontramos os imóveis que foram classificados como boa opção de compra e os em vermelho, como uma má opção de requisição. Resultados estes, baseados na condição do valor de compra do imóvel. Mais abaixo, encontraremos a tabela com os imóveis classificados com boas recomendações de compra e com algumas atribuições para análises.')
    st.write('Se desejar filtrar o mapa, clique na categoria desejada na legenda do lado direito do mapa.')

    fig = map_opportunities(data_buy)
    st.plotly_chart(fig)

    st.markdown(
        'Este conjunto de dados, indicou quais casas devem ser compradas com base na análise de dados realizada, respondendo as duas questões propostas pelo projeto.')
    st.markdown(' Em ordem, é exibido o id identificador do imóvel, o CEP, as condições de vista do imóvel, se ele possui porão, quantidade de banheiros e quartos. Por fim, o preço médio de compra por estação, a melhor estação para venda do imóvel, preço de compra, preço de venda e o lucro esperado com a venda do imóvel. Selecione as informações segradas, que você tem para ver no menu suspenso abaixo.')

    column_selector = st.multiselect('Filtre as informações, para exibi-las, como desejar:', data_sale.columns.tolist())

    if column_selector == []:
        data_set = data_sale
    else:
        data_set = data_sale[column_selector]

    st.write(data_set)

    st.write('Se ainda não achou o imóvel e deseja ver todas as casas disponíveis e seus atributos, marque a caixa abaixo')

    display_db = st.checkbox('Mostrar todas as casas disponíveis')

    if display_db:
        st.subheader('Todas as casas disponíveis')
        st.write(data_transformed)

    st.markdown("<h1 style='text-align: center;'>Testing Business Hypothesis</h1>", unsafe_allow_html=True)
    st.markdown('Esta área do projeto, foi destinada a alguns insights gerados pelos dados coletados do negócio. Consulte, analise e leve em considerações as informações geradas abaixo, para escolher os melhores imóveis para compra e revenda. ')

    hip1, hip2 = hypothesis_1_2(data_transformed)
    hip3, hip4 = hypothesis_3_4(data_transformed)
    hip5, hip6 = hypothesis_5_6(data_transformed)
    hip7, hip8 = hypothesis_7_8(data_transformed)
    hip9, hip10 = hypothesis_9_10(data_transformed)

    # H1 and H2
    c1, c2 = st.columns(2)

    c1.plotly_chart(hip1, use_container_width=True)
    c2.plotly_chart(hip2, use_container_width=True)

    # H3, H4
    c3, c4 = st.columns(2)
    c3.plotly_chart(hip3, use_container_width=True)
    c4.plotly_chart(hip4, use_container_width=True)

    # H5 and H6
    c5, c6 = st.columns(2)
    c5.plotly_chart(hip5, use_container_width=True)
    c6.plotly_chart(hip6, use_container_width=True)

    # H7 and H8
    c7, c8 = st.columns(2)
    c7.plotly_chart(hip7, use_container_width=True)
    c8.plotly_chart(hip8, use_container_width=True)

    # H9 and H10
    c9, c10 = st.columns(2)
    c9.plotly_chart(hip9, use_container_width=True)
    c10.plotly_chart(hip10, use_container_width=True)
