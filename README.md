# Executive One-Pager Agent

Um agente de IA especializado em criar apresentações executivas no estilo "one page", geradas como HTML/CSS prontas para exportar como PDF.

Este repositório também contém o **Agente de Posicionamento Estratégico — LinkedIn (IA & Dados)** (`linkedin_agent.py`), documentado na seção correspondente mais abaixo.

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

---

# Agente de Posicionamento Estratégico — LinkedIn (IA & Dados)

Um agente de IA que constrói autoridade técnica e de negócio no LinkedIn em torno de IA e
Dados, focado em atrair recrutadores e oportunidades PJ/freelancer — não em acumular
curtidas. Opera em dois modos:

1. **Reformulação** — pega um conteúdo existente (rascunho, post antigo, ideia solta, case)
   e o transforma em algo estrategicamente posicionado, sempre entregando duas versões
   (enxuta para alcance, densa para autoridade técnica).
2. **Geração periódica** — cria posts novos, no mínimo a cada 15 dias, seguindo um rodízio
   entre cinco pilares de conteúdo (bastidor técnico-estratégico, ponto de vista
   contra-intuitivo, tradução de complexidade, case/resultado concreto, provocação de
   mercado).

O agente conversa para coletar o necessário e, ao final, avalia o post contra um checklist de
posicionamento antes de salvá-lo como Markdown. Um arquivo de estado local (`linkedin_state.json`
por padrão) guarda o histórico de pilares usados e a data do último post, para não repetir
pilar duas vezes seguidas e para alertar quando a cadência quinzenal estourar.

## Uso

```bash
export ANTHROPIC_API_KEY=sk-ant-...

# Reformular um conteúdo existente
python linkedin_agent.py --mode reformular --content rascunho.md

# Gerar um post novo dentro do rodízio de pilares
python linkedin_agent.py --mode gerar

# Modo interativo (pergunta qual dos dois modos usar)
python linkedin_agent.py
```

### Opções

```
--mode,    -m {reformular,gerar}   Modo de operação
--content, -c FILE                 Conteúdo existente a reformular (texto/markdown)
--output,  -o FILE                 Arquivo Markdown de saída (padrão: linkedin_post_TIMESTAMP.md)
--state,   -s FILE                 Arquivo de estado de rodízio/cadência (padrão: linkedin_state.json)
```
