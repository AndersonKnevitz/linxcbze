
import sqlite3, pandas as pd, streamlit as st
from io import BytesIO

st.set_page_config(page_title="Consulta de Produtos CBZ", layout="wide")

DB="cbz.db"

def init_db():
    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS produtos(
        codigo_cbz TEXT PRIMARY KEY,
        descricao TEXT NOT NULL,
        ean TEXT NOT NULL)""")
    con.commit(); con.close()

init_db()

st.markdown("""
<style>
.stApp{background:#0f1115;color:white}
.card{background:#1b1f27;padding:15px;border-radius:12px}
</style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth=False

tab1,tab2=st.tabs(["Consulta","Administração"])

with tab1:
    st.title("Consulta de Produtos CBZ")
    con=sqlite3.connect(DB)
    df=pd.read_sql("select * from produtos",con)
    con.close()

    busca=st.text_input("Pesquisar por Código CBZ, Descrição ou EAN")
    if busca:
        m=(df["codigo_cbz"].astype(str).str.contains(busca,case=False,na=False)|
           df["descricao"].astype(str).str.contains(busca,case=False,na=False)|
           df["ean"].astype(str).str.contains(busca,case=False,na=False))
        df=df[m]

    c1,c2,c3=st.columns(3)
    c1.metric("Produtos",len(df))
    c2.metric("Status","Online")
    c3.metric("Banco","SQLite")

    st.dataframe(df,use_container_width=True)

with tab2:
    if not st.session_state.auth:
        u=st.text_input("Usuário")
        p=st.text_input("Senha",type="password")
        if st.button("Entrar"):
            if u=="suporte" and p=="1":
                st.session_state.auth=True
                st.rerun()
            else:
                st.error("Login inválido")
    else:
        st.header("Painel Administrativo")

        con=sqlite3.connect(DB)
        df=pd.read_sql("select * from produtos",con)

        st.metric("Total Produtos",len(df))

        with st.form("cad"):
            codigo=st.text_input("Código CBZ")
            desc=st.text_input("Descrição")
            ean=st.text_input("EAN")
            ok=st.form_submit_button("Salvar")
            if ok and codigo and desc and ean:
                con.execute("INSERT OR REPLACE INTO produtos values(?,?,?)",(codigo,desc,ean))
                con.commit()
                st.success("Registro salvo")

        st.subheader("Importar Excel")
        arq=st.file_uploader("Planilha",type=["xlsx"])
        if arq:
            imp=pd.read_excel(arq)
            for _,r in imp.iterrows():
                con.execute("INSERT OR REPLACE INTO produtos values(?,?,?)",
                            (str(r.iloc[0]),str(r.iloc[1]),str(r.iloc[2])))
            con.commit()
            st.success("Importação concluída")

        df=pd.read_sql("select * from produtos",con)

        st.subheader("Produtos")
        st.dataframe(df,use_container_width=True)

        csv=df.to_csv(index=False).encode()
        st.download_button("Exportar CSV",csv,"produtos.csv","text/csv")

        bio=BytesIO()
        with pd.ExcelWriter(bio,engine="openpyxl") as w:
            df.to_excel(w,index=False)
        st.download_button("Exportar Excel",bio.getvalue(),"produtos.xlsx")
        con.close()
