# 🏢 Villa Contabilidade - Sistema de Conferência de Notas Fiscais

Interface vermelha e branca para conferência automática de notas fiscais FSIST x SINTEGRA.

## Instalação

```bash
pip install -r requirements.txt
```

## Como usar

```bash
streamlit run app_villa.py
```

Acesse `http://localhost:8501`

## Funcionalidades

✅ Interface visual com tema vermelho e branco  
✅ Upload drag-and-drop para FSIST e SINTEGRA  
✅ Agregação automática de notas SINTEGRA por data + número  
✅ Normalização de números (últimos 6 dígitos do FSIST)  
✅ Comparação por número + valor  
✅ Dashboard com métricas em tempo real  
✅ Download do resultado com timestamp  
✅ Preview com abas (Todas/Divergentes/Comuns)  

## Lógica

1. **SINTEGRA**: Soma valores de notas com mesma data + número
2. **FSIST**: Considera apenas últimos 6 dígitos (ex: 1.104.770 → 104770)
3. **Comparação**: Número + Valor (ignora diferença de data)
4. **Saída**: Planilha única com coluna Status

## Interface

- Header vermelho com gradiente
- Cards brancos com bordas vermelhas
- Métricas coloridas (verde para comuns, vermelho para divergentes)
- Botão de download estilizado
- Footer com branding Villa Contabilidade

## Desenvolvido para

**Villa Contabilidade** © 2025
