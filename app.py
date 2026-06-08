import sqlite3
from io import BytesIO

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Consulta de Produtos CBZ",
    page_icon="📦",
    layout="wide"
)

DB = "cbz.db"


# ==========================
# BANCO DE DADOS
# ==========================

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos(
            codigo_cbz TEXT PRIMARY KEY,
            descricao TEXT NOT NULL,
            ean TEXT NOT NULL
        )
    """)

    con.commit()
    con.close()


def get_produtos():
    con = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM produtos", con)
    con.close()
    return df


init_db()


# ==========================
# CSS
# ==========================

st.markdown("""
<style>

/* Fundo */

.stApp{
    background:#0B1120;
}

/* Título */

.main-title{
    color:white;
    font-size:42px;
    font-weight:700;
    margin-bottom:5px;
}

.sub-title{
    color:#94A3B8;
    margin-bottom:25px;
}

/* Card principal */

.metric-card{
    background:#111827;
    border:1px solid #1F2937;
    border-radius:16px;
    padding:25px;
    margin-bottom:20px;
}

.metric-number{
    font-size:38px;
    font-weight:700;
    color:#3B82F6;
}

.metric-label{
    color:#CBD5E1;
    font-size:14px;
}

/* Inputs */

.stTextInput input{
    background:#1E293B !important;
    color:white !important;
    border:1px solid #334155 !important;
    border-radius:10px !important;
}

/* Botões */

.stButton > button{
    width:100%;
    background:#2563EB !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    padding:12px !important;
    font-weight:600 !important;
}

.stButton > button:hover{
    background:#1D4ED8 !important;
}

/* Download */

.stDownloadButton > button{
    width:100%;
    background:#10B981 !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    padding:12px !important;
    font-weight:600 !important;
}

/* Tabela */

div[data-testid="stDataFrame"]{
    border:1px solid #1F2937;
    border-radius:14px;
    overflow:hidden;
}

/* Upload */

[data-testid="stFileUploader"]{
    background:#111827;
    border-radius:12px;
    padding:15px;
}

/* ==================================
   CORRIGE TEXTOS ESCUROS
================================== */

/* Labels dos campos */

label,
[data-testid="stWidgetLabel"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span{
    color:#E5E7EB !important;
}

/* Títulos */

h1,
h2,
h3,
h4,
h5{
    color:#FFFFFF !important;
}

/* Placeholders */

input::placeholder{
    color:#94A3B8 !important;
    opacity:1 !important;
}

/* Texto dos tabs */

button[role="tab"]{
    color:#CBD5E1 !important;
}

button[role="tab"][aria-selected="true"]{
    color:#3B82F6 !important;
}

/* Login */

[data-testid="stForm"] label{
    color:#F8FAFC !important;
}

/* Subheaders */

.stSubheader{
    color:#FFFFFF !important;
}

/* Texto geral */

p,
span,
small,
div{
    color:#E2E8F0;
}
/* Selectbox Dark */

[data-baseweb="select"] > div{
    background:#1E293B !important;
    border:1px solid #334155 !important;
    border-radius:10px !important;
}

[data-baseweb="select"] span{
    color:#F8FAFC !important;
    font-weight:500 !important;
}

[data-baseweb="popover"]{
    background:#111827 !important;
}

div[role="option"]{
    background:#111827 !important;
    color:#F8FAFC !important;
}

div[role="option"]:hover{
    background:#1E293B !important;
}
/* ==================================
   SELECTBOX DARK MODE
================================== */

/* Campo fechado */

[data-baseweb="select"] > div{
    background:#1E293B !important;
    border:1px solid #334155 !important;
    border-radius:10px !important;
}

/* Texto selecionado */

[data-baseweb="select"] span{
    color:#FFFFFF !important;
    font-weight:500 !important;
}

/* Ícone da seta */

[data-baseweb="select"] svg{
    fill:#FFFFFF !important;
}

/* Dropdown aberto */

div[role="listbox"]{
    background:#111827 !important;
    border:1px solid #334155 !important;
}

/* Cada item da lista */

div[role="option"]{
    background:#111827 !important;
    color:#FFFFFF !important;
}

/* Texto dentro dos itens */

div[role="option"] *{
    color:#FFFFFF !important;
}

/* Item ao passar mouse */

div[role="option"]:hover{
    background:#1E293B !important;
}

/* Item selecionado */

div[aria-selected="true"]{
    background:#2563EB !important;
    color:#FFFFFF !important;
}

/* Corrige componentes internos do Streamlit */

[data-baseweb="popover"]{
    background:#111827 !important;
}

[data-baseweb="menu"]{
    background:#111827 !important;
}

[data-baseweb="menu"] *{
    color:#FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================
# SESSÃO
# ==========================

if "auth" not in st.session_state:
    st.session_state.auth = False


# ==========================
# ABAS
# ==========================

tab1, tab2 = st.tabs([
    "🔍 Consulta",
    "⚙️ Administração"
])


# =====================================================
# CONSULTA
# =====================================================

with tab1:

    df = get_produtos()

    st.markdown("""
    <div class="main-title">
        Consulta de Produtos CBZ
    </div>
    <div class="sub-title">
        Consulte rapidamente produtos através do Código CBZ, Descrição ou EAN.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{len(df)}</div>
        <div class="metric-label">
            Produtos cadastrados na base
        </div>
    </div>
    """, unsafe_allow_html=True)

    busca = st.text_input(
        "",
        placeholder="🔍 Pesquisar por Código CBZ, Descrição ou EAN"
    )

    if busca:

        filtro = (
            df["codigo_cbz"].astype(str).str.contains(busca, case=False, na=False)
            |
            df["descricao"].astype(str).str.contains(busca, case=False, na=False)
            |
            df["ean"].astype(str).str.contains(busca, case=False, na=False)
        )

        df = df[filtro]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# ADMIN
# =====================================================

with tab2:

    if not st.session_state.auth:

        st.subheader("Acesso Administrativo")

        usuario = st.text_input("Usuário")

        senha = st.text_input(
            "Senha",
            type="password"
        )

        if st.button("Entrar"):

            if usuario == "suporte" and senha == "1":

                st.session_state.auth = True
                st.rerun()

            else:
                st.error("Usuário ou senha inválidos")

    else:

        st.markdown("""
        <div class="main-title">
            Painel Administrativo
        </div>
        """, unsafe_allow_html=True)

        con = sqlite3.connect(DB)

        df = pd.read_sql(
            "SELECT * FROM produtos",
            con
        )

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(df)}</div>
            <div class="metric-label">
                Produtos cadastrados
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
<h2 style="color:white;margin-bottom:20px;">
📦 Novo Produto
</h2>
""", unsafe_allow_html=True)

        with st.form("cadastro", clear_on_submit=True):

            codigo = st.text_input("Código CBZ")
            descricao = st.text_input("Descrição")
            ean = st.text_input("EAN")

            salvar = st.form_submit_button("Salvar Produto")

            if salvar:

                if codigo and descricao and ean:

                    con.execute(
                        """
                        INSERT OR REPLACE INTO produtos
                        VALUES (?, ?, ?)
                        """,
                        (
                            codigo,
                            descricao,
                            ean
                        )
                    )

                    con.commit()

                    st.success(
                        "Produto salvo com sucesso."
                    )

                    st.rerun()

        st.divider()

        st.subheader("Importação em Massa")

        arquivo = st.file_uploader(
            "Selecione a planilha Excel",
            type=["xlsx"]
        )

        if arquivo:

            try:

                imp = pd.read_excel(arquivo)

                total = 0

                for _, row in imp.iterrows():

                    con.execute(
                        """
                        INSERT OR REPLACE INTO produtos
                        VALUES (?, ?, ?)
                        """,
                        (
                            str(row.iloc[0]),
                            str(row.iloc[1]),
                            str(row.iloc[2])
                        )
                    )

                    total += 1

                con.commit()

                st.success(
                    f"{total} registros importados."
                )

                st.rerun()

            except Exception as erro:
                st.error(str(erro))

        st.divider()

        st.subheader("Produtos Cadastrados")

        df = pd.read_sql(
            "SELECT * FROM produtos ORDER BY descricao",
            con
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("🗑️ Excluir Produto")

        if not df.empty:

            produto_excluir = st.selectbox(
                "Selecione o produto",
                options=df["codigo_cbz"].tolist(),
                format_func=lambda x: (
                    f"{x} - "
                    f"{df[df['codigo_cbz'] == x]['descricao'].iloc[0]}"
                )
            )

            confirmar = st.checkbox(
                "Confirmo que desejo excluir este produto"
            )

            if st.button("Excluir Produto"):

                if not confirmar:

                    st.warning(
                        "Marque a confirmação antes de excluir."
                    )

                else:

                    con.execute(
                        "DELETE FROM produtos WHERE codigo_cbz = ?",
                        (produto_excluir,)
                    )

                    con.commit()

                    st.success(
                        "Produto excluído com sucesso."
                    )

                    st.rerun()

        st.divider()

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "📄 Exportar CSV",
                csv,
                "produtos.csv",
                "text/csv"
            )

        with col2:

            st.download_button(
                "📊 Exportar Excel",
                excel_buffer.getvalue(),
                "produtos.xlsx"
            )

        con.close()
