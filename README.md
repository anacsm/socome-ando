# Executive One-Pager Agent

Um agente de IA especializado em criar apresentações executivas no estilo "one page", geradas como HTML/CSS prontas para exportar como PDF.

## Requisitos

- Python 3.11+
- Chave de API da Anthropic

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Uso

### Modo interativo (CLI)

O agente faz perguntas no terminal para coletar as informações necessárias:

```bash
python agent.py
```

### Modo arquivo (briefing)

Forneça um arquivo de briefing em texto ou markdown:

```bash
python agent.py --briefing briefing.md
```

### Opções

```
--briefing, -b FILE    Arquivo de briefing (texto/markdown)
--output,   -o FILE    Arquivo HTML de saída (padrão: one_pager_TIMESTAMP.html)
```

## Exportar como PDF

1. Abra o arquivo `.html` gerado no navegador
2. `Ctrl+P` (ou `Cmd+P` no Mac) → **Salvar como PDF**
3. Em "Mais configurações", selecione **Papel: A4** e marque **Gráficos de fundo**

## Exemplo de arquivo de briefing

```markdown
# Briefing: Resultados Q2 2024

**Público:** Conselho de Administração
**Tópico:** Resultados financeiros do segundo trimestre

## Métricas principais
- Receita: R$ 42M (+18% vs Q1)
- EBITDA: R$ 8,4M (margem 20%)
- Clientes ativos: 12.400 (+8%)
- Churn: 2,1%

## Destaques
- Expansão para 3 novos estados
- Lançamento do produto Premium com boa adesão inicial

## Recomendações
- Aprovar orçamento adicional para expansão comercial
- Avaliar aquisição de concorrente regional
```
