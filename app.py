import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Muay Thai Analytics",
    page_icon="🥊",
    layout="wide"
)

df_lutadores = pd.read_csv("Lutador.csv")
df_golpes = pd.read_csv("Golpe.csv")

st.title("🥊 Muay Thai Analytics: Tawanchai vs Superbon")
st.markdown("Análise estatística detalhada da super luta realizada entre Tawanchai vs Superbon no **ONE Friday Fights 46**.")

st.info("""
### Como funciona uma luta de Muay Thai?

- **5 rounds** de 3 minutos cada, com 2 minutos de descanso entre eles
- Cada golpe tentado é classificado por **tipo** (chute, soco, cotovelada...) e **alvo** (cabeça, corpo, perna)
- **Precisão** = golpes conectados ÷ golpes lançados × 100 — quanto maior, mais eficiente o lutador foi
- Vencer não é só sobre quantos golpes você dá, mas **onde** acerta e com **qual eficiência**
""")

st.write("---")

st.success("""
    🏆 **Resultado Oficial:** **Tawanchai PK.Saenchai** venceu **Superbon Singha Mawynn** por **Decisão Unânime (UD)** após 5 rounds intensos, mantendo o cinturão mundial Peso-Pena de Muay Thai do ONE Championship!
""")
st.write("")

with st.expander("👀 Clique aqui para inspecionar os dados brutos de Lutadores"):
    st.dataframe(df_lutadores)

with st.expander("📊 Clique aqui para inspecionar os dados brutos de Golpes"):
    st.dataframe(df_golpes)

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

with st.sidebar.expander("📖 O que significa cada golpe?"):
    st.markdown("""
    - **Chute**: golpe com a perna (pode ser na cabeça, corpo ou perna)
    - **Teep**: chute frontal tipo empurrão, usado para manter distância
    - **Jab**: soco rápido com a mão da frente
    - **Direto**: soco reto potente com a mão de trás
    - **Cruzado**: soco lateral com a mão de trás
    - **Cotovelada**: golpe cortante com o cotovelo (muito danoso)
    - **Uppercut**: soco de baixo para cima, geralmente no queixo
    """)

df_filtrado = df_golpes.copy()

if opcao_lutador == "Tawanchai":
    df_filtrado = df_filtrado[df_filtrado["ID_Lutador"] == 1]
elif opcao_lutador == "Superbon":
    df_filtrado = df_filtrado[df_filtrado["ID_Lutador"] == 2]

if opcao_golpe != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo_Golpe"] == opcao_golpe]

if opcao_alvo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Alvo"] == opcao_alvo]

df_filtrado["Eficacia (%)"] = (df_filtrado["Conectado"] / df_filtrado["Lancado"] * 100).round(1)
df_filtrado["Eficacia (%)"] = df_filtrado["Eficacia (%)"].fillna(0.0)

# Dados completos para análises globais (não são afetadas pelos filtros)
df_global = df_golpes.copy()
df_global["Eficacia (%)"] = (df_global["Conectado"] / df_global["Lancado"] * 100).round(1)
df_global["Eficacia (%)"] = df_global["Eficacia (%)"].fillna(0.0)


def calcular_metricas_lutador(dados, id_lutador):
    df_lut = dados[dados["ID_Lutador"] == id_lutador]
    lancados = int(df_lut["Lancado"].sum())
    conectados = int(df_lut["Conectado"].sum())
    eficacia = round((conectados / lancados * 100), 1) if lancados > 0 else 0.0
    return lancados, conectados, eficacia


def obter_caminho_imagem(nome_base):
    if os.path.exists(f"{nome_base}.jpg"):
        return f"{nome_base}.jpg"
    elif os.path.exists(f"{nome_base}.png"):
        return f"{nome_base}.png"
    return None


foto_tawanchai = obter_caminho_imagem("tawanchai")
foto_superbon = obter_caminho_imagem("superbon")


# ---- MÉTRICAS ----
if opcao_lutador == "Tawanchai":
    lan, con, ef = calcular_metricas_lutador(df_filtrado, 1)
    with st.container(border=True):
        st.markdown("#### 🔴 👑 Tawanchai (Vencedor)")
        foto_col, dados_col = st.columns([1, 4])
        with foto_col:
            if foto_tawanchai:
                st.image(foto_tawanchai, use_container_width=True)
            else:
                st.info("📷 Foto não encontrada.")
        with dados_col:
            c1, c2, c3 = st.columns(3)
            with c1: st.metric(label="Golpes Lançados", value=lan)
            with c2: st.metric(label="Golpes Conectados", value=con)
            with c3: st.metric(label="Precisão Geral", value=f"{ef}%")

elif opcao_lutador == "Superbon":
    lan, con, ef = calcular_metricas_lutador(df_filtrado, 2)
    with st.container(border=True):
        st.markdown("#### 🔵 🥊 Superbon (Desafiante)")
        foto_col, dados_col = st.columns([1, 4])
        with foto_col:
            if foto_superbon:
                st.image(foto_superbon, use_container_width=True)
            else:
                st.info("📷 Foto não encontrada.")
        with dados_col:
            c1, c2, c3 = st.columns(3)
            with c1: st.metric(label="Golpes Lançados", value=lan)
            with c2: st.metric(label="Golpes Conectados", value=con)
            with c3: st.metric(label="Precisão Geral", value=f"{ef}%")

else:
    lan1, con1, ef1 = calcular_metricas_lutador(df_filtrado, 1)
    lan2, con2, ef2 = calcular_metricas_lutador(df_filtrado, 2)

    col_tawanchai, col_superbon = st.columns(2)

    with col_tawanchai:
        with st.container(border=True):
            st.markdown("#### 🔴 👑 Tawanchai (Vencedor)")
            foto_col, dados_col = st.columns([1, 2])
            with foto_col:
                if foto_tawanchai:
                    st.image(foto_tawanchai, use_container_width=True)
                else:
                    st.info("📷 Foto não encontrada.")
            with dados_col:
                st.metric(label="Lançados", value=lan1)
                st.metric(label="Conectados", value=con1)
                st.metric(label="Precisão", value=f"{ef1}%")

    with col_superbon:
        with st.container(border=True):
            st.markdown("#### 🔵 🥊 Superbon (Desafiante)")
            foto_col, dados_col = st.columns([1, 2])
            with foto_col:
                if foto_superbon:
                    st.image(foto_superbon, use_container_width=True)
                else:
                    st.info("📷 Foto não encontrada.")
            with dados_col:
                st.metric(label="Lançados", value=lan2)
                st.metric(label="Conectados", value=con2)
                st.metric(label="Precisão", value=f"{ef2}%")


# ---- SCORECARD RODADA A RODADA (Item 5) ----
st.write("### 🏆 Placar Round a Round")

df_score = df_global.groupby(["Round", "ID_Lutador"])[["Lancado", "Conectado"]].sum().reset_index()
df_score["Eficacia"] = (df_score["Conectado"] / df_score["Lancado"] * 100).round(1)
df_score["Eficacia"] = df_score["Eficacia"].fillna(0.0)
df_score["Lutador"] = df_score["ID_Lutador"].map({1: "Tawanchai", 2: "Superbon"})

linhas_placar = []
vencedores_round = {}
for r in range(1, 6):
    dados_r = df_score[df_score["Round"] == r]
    if len(dados_r) == 2:
        t = dados_r[dados_r["ID_Lutador"] == 1].iloc[0]
        s = dados_r[dados_r["ID_Lutador"] == 2].iloc[0]
        if t["Conectado"] > s["Conectado"]:
            vencedor = "Tawanchai"
        elif s["Conectado"] > t["Conectado"]:
            vencedor = "Superbon"
        else:
            vencedor = "Empate"
        vencedores_round[r] = vencedor
        linhas_placar.append({
            "Round": r,
            "Tawanchai (Lancados)": int(t["Lancado"]),
            "Tawanchai (Conectados)": int(t["Conectado"]),
            "Tawanchai (Precisao)": f"{t['Eficacia']:.1f}%",
            "Superbon (Lancados)": int(s["Lancado"]),
            "Superbon (Conectados)": int(s["Conectado"]),
            "Superbon (Precisao)": f"{s['Eficacia']:.1f}%",
            "Vencedor do Round": vencedor
        })

df_placar = pd.DataFrame(linhas_placar)
st.dataframe(df_placar.style
    .set_properties(**{'background-color': '#1E2235', 'color': '#FFFFFF', 'border-color': '#2D3250'})
    .apply(lambda row: ['background-color: #1B5E20' if row['Vencedor do Round'] == 'Tawanchai' else 'background-color: #1A237E' if row['Vencedor do Round'] == 'Superbon' else '' for _ in row], axis=1),
    use_container_width=True
)

# Placar resumo
v_tawan = sum(1 for v in vencedores_round.values() if v == "Tawanchai")
v_super = sum(1 for v in vencedores_round.values() if v == "Superbon")
st.markdown(f"**Placar:** 🔴 Tawanchai **{v_tawan}** × **{v_super}** 🔵 Superbon")


# ---- ROUND MAIS DECISIVO (Item 10) + SEMÁFORO (Item 3) ----
melhor_round = None
maior_diferenca = -1
dados_melhor_round = None

for r in range(1, 6):
    dados_r = df_score[df_score["Round"] == r]
    if len(dados_r) == 2:
        t = dados_r[dados_r["ID_Lutador"] == 1].iloc[0]
        s = dados_r[dados_r["ID_Lutador"] == 2].iloc[0]
        diff = abs(int(t["Conectado"]) - int(s["Conectado"]))
        if diff > maior_diferenca:
            maior_diferenca = diff
            melhor_round = r
            dados_melhor_round = (t, s)

col_semaforo, col_decisivo = st.columns(2)

with col_semaforo:
    st.markdown("##### 🚦 Semáforo de Performance por Round")
    for r in range(1, 6):
        v = vencedores_round.get(r, "Empate")
        dados_r = df_score[df_score["Round"] == r]
        if len(dados_r) == 2:
            t_con = int(dados_r[dados_r["ID_Lutador"] == 1].iloc[0]["Conectado"])
            s_con = int(dados_r[dados_r["ID_Lutador"] == 2].iloc[0]["Conectado"])
            diff = abs(t_con - s_con)
            if diff >= 5:
                icone = "🟢"
                status = "dominante"
            elif diff >= 2:
                icone = "🟡"
                status = "equilibrado"
            else:
                icone = "🔴"
                status = "disputado"
            st.markdown(f"{icone} **Round {r}:** {v} ({t_con} × {s_con} conectados) — {status}")

with col_decisivo:
    if dados_melhor_round is not None:
        t, s = dados_melhor_round
        vencedor_melhor = vencedores_round[melhor_round]
        st.markdown("##### ⭐ Round Mais Decisivo")
        st.info(f"**Round {melhor_round}** — maior diferença da luta!\n\n"
                f"🔴 Tawanchai conectou **{int(t['Conectado'])}** de **{int(t['Lancado'])}** ({t['Eficacia']:.1f}%)\n\n"
                f"🔵 Superbon conectou **{int(s['Conectado'])}** de **{int(s['Lancado'])}** ({s['Eficacia']:.1f}%)\n\n"
                f"Diferença de **{maior_diferenca}** golpes conectados — **{vencedor_melhor}** dominou este round!")


# ---- NARRATIVA DINÂMICA (Item 2) ----
st.write("### 💡 Entendendo os Números")

lan_t, con_t, ef_t = calcular_metricas_lutador(df_global, 1)
lan_s, con_s, ef_s = calcular_metricas_lutador(df_global, 2)

col_narrativa1, col_narrativa2 = st.columns(2)

with col_narrativa1:
    com_a_cada = round(con_t / lan_t * 10) if lan_t > 0 else 0
    st.markdown(f"🔴 **Tawanchai:** A cada **10** golpes que tentou, **{com_a_cada}** conectaram (precisão de {ef_t}%). "
                f"Foram **{lan_t}** tentativas e **{con_t}** acertos no total.")

with col_narrativa2:
    com_a_cada_s = round(con_s / lan_s * 10) if lan_s > 0 else 0
    st.markdown(f"🔵 **Superbon:** A cada **10** golpes que tentou, **{com_a_cada_s}** conectaram (precisão de {ef_s}%). "
                f"Foram **{lan_s}** tentativas e **{con_s}** acertos no total.")

if lan_t > 0 and lan_s > 0:
    dif_precisao = round(ef_t - ef_s, 1)
    if dif_precisao > 0:
        st.success(f"📊 **Tawanchai** foi **{dif_precisao}%** mais preciso que Superbon na luta toda.")
    elif dif_precisao < 0:
        st.success(f"📊 **Superbon** foi **{abs(dif_precisao)}%** mais preciso que Tawanchai na luta toda.")
    else:
        st.success("📊 **Empate técnico** em precisão geral entre os dois lutadores.")


# ---- VANTAGEM DE BASE (Item 8) ----
st.write("### 🧭 Vantagem de Base: Canhoto vs Destro")
st.markdown("Tawanchai é **canhoto** (base esquerda), Superbon é **destro** (base direita). "
            "Ataques vindos do lado oposto ao tradicional podem ser mais difíceis de defender.")

df_base = df_global.groupby(["ID_Lutador", "Lado"])[["Lancado", "Conectado"]].sum().reset_index()
df_base["Eficacia"] = (df_base["Conectado"] / df_base["Lancado"] * 100).round(1)
df_base["Eficacia"] = df_base["Eficacia"].fillna(0.0)
df_base["Lutador"] = df_base["ID_Lutador"].map({1: "Tawanchai (Canhoto)", 2: "Superbon (Destro)"})
df_base["Lado_label"] = df_base["Lado"].map({"Esquerdo": "🫲 Esquerdo", "Direito": "🫱 Direito"})

fig_base = px.bar(df_base, x="Lado_label", y="Eficacia", color="Lutador", barmode="group",
                  text="Eficacia", template="plotly_dark",
                  labels={"Lado_label": "Lado do Golpe", "Eficacia": "Precisão (%)"})
fig_base.update_traces(texttemplate='%{text}%', textposition='outside')
fig_base.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                       font_color="#FFFFFF", yaxis=dict(showgrid=True, gridcolor='#2D3250'))
st.plotly_chart(fig_base, use_container_width=True)


st.write("---")

# ---- TABELA ESTILIZADA ----
st.subheader(f"📊 Análise: {opcao_lutador} ➔ {opcao_golpe} ➔ {opcao_alvo}")
colunas_limpas = ["Round", "Tipo_Golpe", "Alvo", "Lado", "Lancado", "Conectado", "Eficacia (%)"]

if not df_filtrado.empty:
    tabela_estilizada = (df_filtrado[colunas_limpas].style
        .set_properties(**{
            'background-color': '#1E2235',
            'color': '#FFFFFF',
            'border-color': '#2D3250'
        })
        .format({'Eficacia (%)': '{:.1f}%'})
    )
    st.dataframe(tabela_estilizada, use_container_width=True)
else:
    st.warning("Nenhum golpe encontrado para essa combinação de filtros! 🥊")


# ---- SEÇÃO DE GRÁFICOS ----
st.write("---")
st.write("### 📊 Análise Gráfica Avançada")

# Linha 1: Gráficos existentes
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        with st.container(border=True):
            st.write("##### 🎯 Distribuição de Golpes por Alvo")
            df_grafico_alvo = df_filtrado.groupby("Alvo")["Conectado"].sum().reset_index()
            cores_alvo = {"Cabeça": "#EF553B", "Corpo": "#636EFA", "Perna": "#00CC96"}

            fig_alvo = px.bar(df_grafico_alvo, x="Alvo", y="Conectado", color="Alvo",
                              color_discrete_map=cores_alvo, template="plotly_dark")

            fig_alvo.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                   font_color="#FFFFFF", yaxis=dict(showgrid=True, gridcolor='#2D3250'), xaxis=dict(showgrid=False))
            st.plotly_chart(fig_alvo, use_container_width=True)

with col_graf2:
    if not df_filtrado.empty:
        with st.container(border=True):
            st.write("##### 🥊 Lançados vs Conectados por Round")
            df_energia = df_filtrado.groupby(["Round", "ID_Lutador"])[["Lancado", "Conectado"]].sum().reset_index()
            df_energia["Lutador"] = df_energia["ID_Lutador"].map({1: "Tawanchai", 2: "Superbon"})
            df_melted = pd.melt(df_energia, id_vars=["Round", "Lutador"], value_vars=["Lancado", "Conectado"],
                                var_name="Status do Golpe", value_name="Quantidade")
            df_melted["Lutador_Status"] = df_melted["Lutador"] + " - " + df_melted["Status do Golpe"]

            cores_customizadas = {"Tawanchai - Lancado": "#EF553B", "Tawanchai - Conectado": "#FAC5BB",
                                  "Superbon - Lancado": "#636EFA", "Superbon - Conectado": "#CCD1FF"}

            fig_intensidade = px.bar(df_melted, x="Round", y="Quantidade", color="Lutador_Status", barmode="group",
                                     color_discrete_map=cores_customizadas, template="plotly_dark")

            fig_intensidade.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFFFFF",
                                           xaxis=dict(tickmode="linear", tick0=1, dtick=1, showgrid=False), yaxis=dict(showgrid=True, gridcolor='#2D3250'))
            st.plotly_chart(fig_intensidade, use_container_width=True)

# Linha 2: Mapa de Calor (Item 6) + Taxa de Conversão (Item 9)
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        with st.container(border=True):
            st.write("##### 🔥 Mapa de Calor: Eficácia por (Golpe × Alvo)")
            df_heat = df_filtrado.groupby(["Tipo_Golpe", "Alvo"])[["Lancado", "Conectado"]].sum().reset_index()
            df_heat["Efic"] = (df_heat["Conectado"] / df_heat["Lancado"] * 100).round(1)
            df_heat["Efic"] = df_heat["Efic"].fillna(0.0)

            pivot = df_heat.pivot(index="Tipo_Golpe", columns="Alvo", values="Efic").fillna(0)
            if not pivot.empty:
                fig_heat = px.imshow(pivot, text_auto=True, color_continuous_scale="RdYlGn",
                                     template="plotly_dark", aspect="auto",
                                     labels={"x": "Alvo", "y": "Tipo de Golpe", "color": "Eficácia (%)"})
                fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                       font_color="#FFFFFF", coloraxis_showscale=False)
                st.plotly_chart(fig_heat, use_container_width=True)

with col_graf4:
    if not df_filtrado.empty:
        with st.container(border=True):
            st.write("##### 📈 Taxa de Conversão por Tipo de Golpe")
            df_conv = df_filtrado.groupby(["ID_Lutador", "Tipo_Golpe"])[["Lancado", "Conectado"]].sum().reset_index()
            df_conv["Eficacia"] = (df_conv["Conectado"] / df_conv["Lancado"] * 100).round(1)
            df_conv["Eficacia"] = df_conv["Eficacia"].fillna(0.0)
            df_conv["Lutador"] = df_conv["ID_Lutador"].map({1: "Tawanchai", 2: "Superbon"})

            fig_conv = px.bar(df_conv, x="Eficacia", y="Tipo_Golpe", color="Lutador",
                              barmode="group", orientation="h", template="plotly_dark",
                              text="Eficacia", labels={"Eficacia": "Precisão (%)", "Tipo_Golpe": ""})
            fig_conv.update_traces(texttemplate='%{text}%', textposition='outside')
            fig_conv.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                   font_color="#FFFFFF", xaxis=dict(showgrid=True, gridcolor='#2D3250'),
                                   yaxis=dict(showgrid=False), legend=dict(orientation="h", yanchor="bottom", y=1.02))
            st.plotly_chart(fig_conv, use_container_width=True)
