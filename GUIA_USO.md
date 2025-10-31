# 🚀 Guia Rápido - Villa Contabilidade

## 1. Instalar

```bash
pip install -r requirements.txt
```

## 2. Rodar

```bash
streamlit run app_villa.py
```

## 3. Usar

1. Arraste FSIST.xlsx no primeiro card
2. Arraste SINTEGRA.xls/.xlsx no segundo card
3. Aguarde processamento
4. Veja métricas no dashboard
5. Clique em "BAIXAR RESULTADO"
6. Confira preview nas abas

## Resultado

Planilha Excel com colunas:
- **Data**: dd/mm/aaaa
- **Número**: 6 dígitos normalizados
- **Valor Contábil**: valor em R$
- **Status**: EM COMUM / SOMENTE SINTEGRA / SOMENTE FSIST

## Dúvidas?

O sistema:
- Soma valores do SINTEGRA quando há subdivisões
- Usa últimos 6 dígitos do FSIST
- Compara por número E valor
- Ignora diferença de datas

---
**Villa Contabilidade** • Sistema v1.0
