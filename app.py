import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração global da página do navegador (Título, Ícone e Layout expandido)
st.set_page_config(
    page_title="Muay Thai Analytics",
    page_icon="🥊",
    layout="wide"
)

# Carregamento dos arquivos de dados CSV estruturados no projeto
df_lutadores = pd.read_csv("Lutador.csv")
df_golpes = pd.read_csv("Golpe.csv")

# Exibição do cabeçalho principal da página web com títulos informativos
st.title("🥊 Muay Thai Analytics: Tawanchai vs Superbon")
st.markdown("Análise estatística detalhada da super luta realizada entre Tawanchai vs Superbon no **ONE Friday Fights 46**.")
st.write("---") 

# Exibição do resultado oficial da luta em destaque na página
st.success("""
    🏆 **Resultado Oficial:** **Tawanchai PK.Saenchai** venceu **Superbon Singha Mawynn** por **Decisão Unânime (UD)** após 5 rounds intensos, mantendo o cinturão mundial Peso-Pena de Muay Thai do ONE Championship!
""")
st.write("")

# Criação de seções expansíveis para verificação e auditoria dos dados brutos
with st.expander("👀 Clique aqui para inspecionar os dados brutos de Lutadores"):
    st.dataframe(df_lutadores)

with st.expander("📊 Clique aqui para inspecionar os dados brutos de Golpes"):
    st.dataframe(df_golpes)

# Construção dos componentes de seleção de filtros na barra lateral esquerda
st.sidebar.header("🔍 Filtros de Análise")

opcao_lutador = st.sidebar.selectbox(
    "1. Escolha o Lutador:",
    ["Ambos", "Tawanchai", "Superbon"]
)

opcao_golpe = st.sidebar.selectbox(
    "2. Escolha o Tipo de Golpe:",
    ["Todos", "Chute", "Teep", "Jab", "Direto", "Cruzado", "Cotovelada", "Uppercut"]
)

opcao_alvo = st.sidebar.selectbox(
    "3. Escolha o Alvo do Golpe:",
    ["Todos", "Corpo", "Cabeça", "Perna"]
)

# Processamento da lógica de filtragem sequencial (funil de dados) com base nas escolhas
df_filtrado = df_golpes.copy()

if opcao_lutador == "Tawanchai":
    df_filtrado = df_filtrado[df_filtrado["ID_Lutador"] == 1]
elif opcao_lutador == "Superbon":
    df_filtrado = df_filtrado[df_filtrado["ID_Lutador"] == 2]

if opcao_golpe != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo_Golpe"] == opcao_golpe]

if opcao_alvo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Alvo"] == opcao_alvo]

# Engenharia de atributos: Criação matemática da coluna de eficácia com tratamento de erros
df_filtrado["Eficacia (%)"] = (df_filtrado["Conectado"] / df_filtrado["Lancado"] * 100).round(1)
df_filtrado["Eficacia (%)"] = df_filtrado["Eficacia (%)"].fillna(0.0)


# Função explicativa: Calcula as métricas somadas isolando o ID de um lutador específico
def calcular_metricas_lutador(dados, id_lutador):
    df_lut = dados[dados["ID_Lutador"] == id_lutador]
    lancados = int(df_lut["Lancado"].sum())
    conectados = int(df_lut["Conectado"].sum())
    eficacia = round((conectados / lancados * 100), 1) if lancados > 0 else 0.0
    return lancados, conectados, eficacia


# Bloco explicativo: Renderiza cartões de métricas (KPIs) totalmente identificados na interface
if opcao_lutador == "Tawanchai":
    lan, con, ef = calcular_metricas_lutador(df_filtrado, 1)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric(label="Golpes Lançados (Tawanchai)", value=lan)
    with c2: st.metric(label="Golpes Conectados (Tawanchai)", value=con)
    with c3: st.metric(label="Precisão Geral (Tawanchai)", value=f"{ef}%")

elif opcao_lutador == "Superbon":
    lan, con, ef = calcular_metricas_lutador(df_filtrado, 2)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric(label="Golpes Lançados (Superbon)", value=lan)
    with c2: st.metric(label="Golpes Conectados (Superbon)", value=con)
    with c3: st.metric(label="Precisão Geral (Superbon)", value=f"{ef}%")

else:
    lan1, con1, ef1 = calcular_metricas_lutador(df_filtrado, 1)
    lan2, con2, ef2 = calcular_metricas_lutador(df_filtrado, 2)
    
    col_tawanchai, col_superbon = st.columns(2)
    with col_tawanchai:
        st.markdown("#### 🔴 👑 Tawanchai (Vencedor)")
        st.metric(label="Lançados", value=lan1)
        st.metric(label="Conectados", value=con1)
        st.metric(label="Precisão", value=f"{ef1}%")
        
    with col_superbon:
        st.markdown("#### 🔵 🥊 Superbon (Desafiante)")
        st.metric(label="Lançados", value=lan2)
        st.metric(label="Conectados", value=con2)
        st.metric(label="Precisão", value=f"{ef2}%")

st.write("---")

# Renderização do título dinâmico e exibição da tabela final resumida e estilizada
st.subheader(f"📊 Análise: {opcao_lutador} ➔ {opcao_golpe} ➔ {opcao_alvo}")

colunas_limpas = ["Round", "Tipo_Golpe", "Alvo", "Lado", "Lancado", "Conectado", "Eficacia (%)"]

if not df_filtrado.empty:
    # Aplica a cor de fundo, texto e formata a coluna de eficácia com 1 casa decimal e símbolo %
    tabela_estilizada = (df_filtrado[colunas_limpas].style
        .set_properties(**{
            'background-color': '#1E2235',
            'color': '#FFFFFF',
            'border-color': '#2D3250'
        })
        .format({'Eficacia (%)': '{:.1f}%'}) # Força o Pandas a mostrar apenas 1 casa decimal + %
    )
    st.dataframe(tabela_estilizada, use_container_width=True)
else:
    st.warning("Nenhum golpe encontrado para essa combinação de filtros! 🥊")

# Verificação se existem dados para gerar o gráfico de barras por Alvo
if not df_filtrado.empty:
    st.write("### 🎯 Distribuição de Golpes por Alvo")
    
    df_grafico_alvo = df_filtrado.groupby("Alvo")["Conectado"].sum().reset_index()
    cores_alvo = {"Cabeça": "#EF553B", "Corpo": "#636EFA", "Perna": "#00CC96"}
    
    fig_alvo = px.bar(
        df_grafico_alvo, 
        x="Alvo", 
        y="Conectado",
        labels={"Conectado": "Golpes Conectados"},
        color="Alvo",
        color_discrete_map=cores_alvo,
        template="plotly_dark"
    )
    
    # Customização do layout para remover fundos cinzas e tornar transparente
    fig_alvo.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#FFFFFF",
        yaxis=dict(showgrid=True, gridcolor='#2D3250'),
        xaxis=dict(showgrid=False)
    )
    
    st.plotly_chart(fig_alvo, use_container_width=True)

# Verificação se existem dados para gerar a análise de intensidade por round
if not df_filtrado.empty:
    st.write("### 🥊 Intensidade e Desgaste: Lançados vs Conectados por Round")
    
    df_energia = df_filtrado.groupby(["Round", "ID_Lutador"])[["Lancado", "Conectado"]].sum().reset_index()
    
    mapeamento_nomes = {1: "Tawanchai", 2: "Superbon"}
    df_energia["Lutador"] = df_energia["ID_Lutador"].map(mapeamento_nomes)
    
    df_melted = pd.melt(
        df_energia, 
        id_vars=["Round", "Lutador"], 
        value_vars=["Lancado", "Conectado"],
        var_name="Status do Golpe", 
        value_name="Quantidade"
    )
    
    df_melted["Lutador_Status"] = df_melted["Lutador"] + " - " + df_melted["Status do Golpe"]
    
    cores_customizadas = {
        "Tawanchai - Lancado": "#EF553B",    
        "Tawanchai - Conectado": "#FAC5BB",  
        "Superbon - Lancado": "#636EFA",      
        "Superbon - Conectado": "#CCD1FF"     
    }
    
    fig_intensidade = px.bar(
        df_melted,
        x="Round",
        y="Quantidade",
        color="Lutador_Status",
        barmode="group",
        color_discrete_map=cores_customizadas,
        labels={"Quantidade": "Total de Golpes", "Round": "Número do Round", "Lutador_Status": "Legenda"},
        template="plotly_dark"
    )
    
    # Customização do layout do segundo gráfico para transparência total
    fig_intensidade.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#FFFFFF",
        xaxis=dict(tickmode="linear", tick0=1, dtick=1, showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2D3250')
    )
    
    st.plotly_chart(fig_intensidade, use_container_width=True)