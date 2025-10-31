import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Villa Contabilidade - Conferência NF",
    page_icon="📊",
    layout="wide"
)

# CSS customizado - Tema vermelho e branco
st.markdown("""
    <style>
    /* Fundo principal */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #ffe6e6 100%);
    }
    
    /* Header customizado */
    .header-villa {
        background: linear-gradient(90deg, #c41e3a 0%, #8b0000 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .header-villa h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: bold;
    }
    
    .header-villa p {
        color: #ffcccc;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Cards de upload */
    .upload-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #c41e3a;
        box-shadow: 0 2px 4px rgba(196,30,58,0.1);
        margin-bottom: 1rem;
    }
    
    /* Métricas customizadas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #c41e3a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #c41e3a;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Botões */
    .stDownloadButton button {
        background: linear-gradient(90deg, #c41e3a 0%, #8b0000 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 5px;
        width: 100%;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(90deg, #8b0000 0%, #c41e3a 100%);
    }
    
    /* Tabelas */
    .dataframe {
        border: 2px solid #c41e3a !important;
    }
    
    /* Footer */
    .footer-villa {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #666;
        border-top: 2px solid #c41e3a;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed #c41e3a;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #d4edda;
        border-color: #c41e3a;
    }
    
    .stError {
        background-color: #f8d7da;
        border-color: #8b0000;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-villa">
        <h1>🏢 VILLA CONTABILIDADE</h1>
        <p>Sistema de Conferência de Notas Fiscais</p>
    </div>
""", unsafe_allow_html=True)

# Funções de processamento
def normalizar_numero(num, ultimos_6=False):
    num_str = str(num).replace('.', '').replace(' ', '').strip()
    if ultimos_6:
        return num_str[-6:]
    return num_str

def converter_valor(val):
    if isinstance(val, str):
        return float(val.replace('.', '').replace(',', '.'))
    return float(val)

# Layout em duas colunas para upload
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown("### 📁 PLANILHA FSIST")
    fsist_file = st.file_uploader("Selecione FSIST.xlsx", type=['xlsx'], key='fsist')
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown("### 📁 PLANILHA SINTEGRA")
    sintegra_file = st.file_uploader("Selecione SINTEGRA.xlsx ou .xls", type=['xlsx', 'xls'], key='sintegra')
    st.markdown('</div>', unsafe_allow_html=True)

# Processamento
if fsist_file and sintegra_file:
    try:
        with st.spinner('🔄 Processando conferência...'):
            # Ler planilhas
            df_fsist = pd.read_excel(fsist_file)
            df_sintegra = pd.read_excel(sintegra_file)
            
            # Identificar colunas
            col_data_sintegra = [c for c in df_sintegra.columns if 'escrit' in c.lower() or 'data' in c.lower()][0]
            col_numero_sintegra = [c for c in df_sintegra.columns if 'número' in c.lower() or 'numero' in c.lower()][0]
            col_valor_sintegra = [c for c in df_sintegra.columns if 'contábil' in c.lower() or 'contabil' in c.lower() or 'valor' in c.lower()][-1]
            
            col_data_fsist = [c for c in df_fsist.columns if 'emiss' in c.lower() or 'data' in c.lower()][0]
            col_numero_fsist = [c for c in df_fsist.columns if 'número' in c.lower() or 'numero' in c.lower()][0]
            col_valor_fsist = [c for c in df_fsist.columns if 'valor' in c.lower()][0]
            
            # Processar SINTEGRA
            df_sintegra['Numero_norm'] = df_sintegra[col_numero_sintegra].apply(lambda x: normalizar_numero(x, ultimos_6=False))
            df_sintegra['Data_norm'] = pd.to_datetime(df_sintegra[col_data_sintegra], dayfirst=True).dt.date
            df_sintegra['Valor_norm'] = df_sintegra[col_valor_sintegra].apply(converter_valor)
            
            sintegra_agregado = df_sintegra.groupby(['Data_norm', 'Numero_norm']).agg({
                'Valor_norm': 'sum'
            }).reset_index()
            sintegra_agregado.columns = ['Data', 'Número', 'Valor Contábil']
            
            # Processar FSIST
            df_fsist['Numero_norm'] = df_fsist[col_numero_fsist].apply(lambda x: normalizar_numero(x, ultimos_6=True))
            df_fsist['Data_norm'] = pd.to_datetime(df_fsist[col_data_fsist]).dt.date
            df_fsist['Valor_norm'] = df_fsist[col_valor_fsist].apply(lambda x: float(x) if not isinstance(x, str) else converter_valor(x))
            
            fsist_processado = df_fsist[['Data_norm', 'Numero_norm', 'Valor_norm']].copy()
            fsist_processado.columns = ['Data', 'Número', 'Valor Contábil']
            
            # Comparar
            sintegra_agregado['Chave'] = sintegra_agregado['Número'] + '_' + sintegra_agregado['Valor Contábil'].round(2).astype(str)
            fsist_processado['Chave'] = fsist_processado['Número'] + '_' + fsist_processado['Valor Contábil'].round(2).astype(str)
            
            chaves_sintegra = set(sintegra_agregado['Chave'])
            chaves_fsist = set(fsist_processado['Chave'])
            comuns = chaves_sintegra & chaves_fsist
            
            # Gerar resultado
            notas_comuns = sintegra_agregado[sintegra_agregado['Chave'].isin(comuns)][['Data', 'Número', 'Valor Contábil']].copy()
            notas_comuns['Status'] = 'EM COMUM'
            
            apenas_sintegra_df = sintegra_agregado[~sintegra_agregado['Chave'].isin(comuns)][['Data', 'Número', 'Valor Contábil']].copy()
            apenas_sintegra_df['Status'] = 'SOMENTE SINTEGRA'
            
            apenas_fsist_df = fsist_processado[~fsist_processado['Chave'].isin(comuns)][['Data', 'Número', 'Valor Contábil']].copy()
            apenas_fsist_df['Status'] = 'SOMENTE FSIST'
            
            resultado_completo = pd.concat([notas_comuns, apenas_sintegra_df, apenas_fsist_df], ignore_index=True)
            resultado_completo = resultado_completo.sort_values(['Status', 'Data'])
            resultado_completo['Data'] = pd.to_datetime(resultado_completo['Data']).dt.strftime('%d/%m/%Y')
            
        # Métricas
        st.markdown("---")
        st.markdown("### 📊 RESULTADO DA CONFERÊNCIA")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{len(resultado_completo)}</p>
                    <p class="metric-label">Total de Notas</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value" style="color: #28a745;">{len(notas_comuns)}</p>
                    <p class="metric-label">Em Comum</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value" style="color: #ff6b6b;">{len(apenas_sintegra_df)}</p>
                    <p class="metric-label">Só SINTEGRA</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value" style="color: #ff6b6b;">{len(apenas_fsist_df)}</p>
                    <p class="metric-label">Só FSIST</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Download
        output = BytesIO()
        resultado_completo.to_excel(output, index=False, sheet_name='Conferência', engine='openpyxl')
        output.seek(0)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        st.download_button(
            label="⬇️ BAIXAR RESULTADO DA CONFERÊNCIA",
            data=output,
            file_name=f"villa_conferencia_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Preview
        st.markdown("### 👁️ PREVIEW DOS DADOS")
        
        tab1, tab2, tab3 = st.tabs(["✅ Todas as Notas", "🔴 Divergentes", "✅ Em Comum"])
        
        with tab1:
            st.dataframe(resultado_completo, use_container_width=True, height=400)
        
        with tab2:
            divergentes = resultado_completo[resultado_completo['Status'] != 'EM COMUM']
            st.dataframe(divergentes, use_container_width=True, height=400)
        
        with tab3:
            st.dataframe(notas_comuns[['Data', 'Número', 'Valor Contábil']], use_container_width=True, height=400)
        
    except Exception as e:
        st.error(f"❌ Erro ao processar: {str(e)}")
        st.exception(e)
else:
    st.info("👆 Faça upload dos dois arquivos para iniciar a conferência")

# Footer
st.markdown("""
    <div class="footer-villa">
        <p><strong>Villa Contabilidade</strong> • Sistema de Conferência de Notas Fiscais</p>
        <p>Desenvolvido com ❤️ • © 2025</p>
    </div>
""", unsafe_allow_html=True)
