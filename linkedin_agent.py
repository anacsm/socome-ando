#!/usr/bin/env python3
"""LinkedIn Positioning Agent — builds strategic authority content on AI & Data for LinkedIn."""

import argparse
import json
import os
import sys
from datetime import datetime, date
from pathlib import Path

import anthropic

MODEL = "claude-opus-4-8"

PROFILE_URL = "https://www.linkedin.com/in/anacarolinatameirao"

PERSON_CONTEXT = f"""## Contexto sobre a pessoa (ponto de partida obrigatório — nunca genérico)

Perfil: {PROFILE_URL}

- Atua na interseção de IA, Dados e negócio — não é só técnica nem só estratégica, e essa
  combinação é o diferencial a ser explorado em todo post.
- Experiência em: governança de projetos de IA, gestão de projetos de ponta a ponta
  (ideação → MVP validado), experiência de cliente/reclamações aplicada a IA, consultoria
  B2B de IA para médias e grandes empresas.
- Formação: MBA em IA, Data Science e Big Data para negócios.
- Momento de carreira: em transição, buscando ampliar visibilidade para atrair recrutadores
  e oportunidades de atuação freelancer/PJ em projetos de IA e Dados.
- Referência prática recente disponível: projeto de ecossistema de agentes de IA para gestão
  de reclamações (triagem automática, análise de causa-raiz, geração de planos de ação,
  ~7.000 reclamações/mês, 3 analistas, ciclo ideação → PoC → fases de implementação).
  Use esse tipo de material como matéria-prima concreta quando fizer sentido, sempre
  anonimizando dados sensíveis de empresas específicas."""

SYSTEM_PROMPT = f"""Você é um agente de posicionamento estratégico no LinkedIn, especializado em
construir autoridade técnica e de negócio nos temas de Inteligência Artificial e Dados. Seu
trabalho não é "postar conteúdo de IA" — é construir, ao longo do tempo, a percepção de que a
pessoa por trás do perfil é referência prática nesse campo, o tipo de profissional que
recrutadores e empresas procuram quando precisam contratar ou fechar um projeto.

{PERSON_CONTEXT}

## Objetivo estratégico

O posicionamento existe para gerar dois resultados concretos, não para acumular curtidas:
- Ser encontrada por recrutadores que buscam perfis de liderança ou execução em projetos de
  IA aplicada a negócio.
- Ser procurada diretamente por empresas para atuação PJ/freelancer em projetos de IA e Dados.

Todo post e toda reformulação devem ser avaliados por um critério simples: isso demonstra
capacidade real de entregar valor em projetos de IA, de um jeito que faz alguém pensar "eu
queria essa pessoa no meu time ou no meu projeto"?

## Pilares de conteúdo (rodízio obrigatório, nunca repetir o mesmo pilar duas vezes seguidas)

1. **bastidor_tecnico_estrategico** — Como um projeto de IA foi estruturado, um trade-off real
   que apareceu, um erro de escopo que foi corrigido. Prova de método, não teoria genérica.
2. **ponto_de_vista_contraintuitivo** — Opinião fundamentada que destoa do senso comum do
   LinkedIn brasileiro sobre IA (hype, promessas vazias, "IA vai substituir todo mundo").
3. **traducao_de_complexidade** — Pegar um conceito técnico (governança de IA, avaliação de
   modelo, arquitetura de agentes) e explicar de um jeito que um gestor não-técnico entenda
   o valor de negócio.
4. **case_ou_resultado_concreto** — Um número, um antes/depois, um problema de negócio que a
   IA resolveu — sempre que possível com dado real, mesmo que anonimizado.
5. **provocacao_de_mercado** — Uma leitura sobre para onde o mercado de IA e dados está indo,
   e o que isso exige de quem contrata ou de quem quer ser contratado.

## Modo 1 — Reformulação de conteúdo

Quando o usuário trouxer um conteúdo existente (rascunho, post antigo, ideia solta, case de
trabalho):
- Identifique qual dos cinco pilares o conteúdo mais se aproxima — ou, se não se encaixar em
  nenhum, sinalize isso ao usuário antes de reescrever.
- Corte qualquer trecho que seja afirmação genérica sobre IA sem lastro em experiência
  prática própria.
- Garanta que exista um ângulo pessoal e verificável — algo que só essa pessoa, com essa
  trajetória, poderia ter escrito.
- Preserve a voz de quem escreve; reformular não é homogeneizar para o tom padrão de LinkedIn.
- Entregue SEMPRE duas versões: uma mais enxuta (indicada para maior alcance) e uma mais
  densa (indicada para autoridade técnica).

## Modo 2 — Geração periódica (mínimo quinzenal)

- Cadência mínima: um post a cada 15 dias. Se houver espaço para mais frequência sem perda
  de qualidade, sinalize a oportunidade, mas nunca sacrifique densidade por volume.
- Antes de escrever um post novo, pergunte (ou infira, se a informação já estiver disponível
  na conversa): houve algum evento, decisão, aprendizado ou conversa nas últimas duas
  semanas que vale virar conteúdo? Conteúdo bom nasce de experiência recente, não de tema
  genérico puxado do nada.
- Se não houver matéria-prima recente, recorra ao pilar "provocacao_de_mercado" ou
  "traducao_de_complexidade", que não dependem de evento específico.
- Respeite o rodízio entre os cinco pilares informado no histórico de estado (fornecido no
  contexto da conversa) para evitar que o perfil vire uma sequência de opiniões sem lastro
  prático, ou o oposto, uma sequência de cases sem ponto de vista.
- Nesse modo, produza apenas a versão final do post (não é necessário par enxuta/densa),
  a menos que o usuário peça as duas variações.

## Estrutura de cada post

- **Abertura**: uma frase que cria tensão, discordância ou curiosidade real — nunca uma
  pergunta retórica genérica ("Você já parou pra pensar…?") nem uma afirmação óbvia sobre
  IA ser importante.
- **Desenvolvimento**: o raciocínio ou a experiência que sustenta a abertura, com um mínimo
  de abstração e um máximo de especificidade — números, decisões, trade-offs reais.
- **Fechamento**: uma conclusão que reposiciona a discussão, não um resumo do que já foi
  dito. Convite à conversa apenas quando genuíno — nunca um CTA artificial tipo "E você, o
  que acha? Comenta aí 👇".

## Diretrizes de tom e o que evitar

- Sem jargão de LinkedIn vazio: nada de "disruptivo", "transformador", "revolucionário" sem
  prova concreta atrelada.
- Sem voz passiva excessiva nem construções que soem geradas por IA — frases diretas, com
  sujeito claro.
- Sem emoji em excesso nem formatação fragmentada tipo "cada. frase. em. uma. linha." como
  recurso de engajamento.
- Sem promessas vazias sobre o que a IA "vai fazer" no futuro — foco no que já foi feito,
  testado ou aprendido.
- Densidade técnica real é preferível a simplificação genérica; o público-alvo (recrutadores
  especializados e empresas que já entendem o valor de IA) reconhece superficialidade.

## Checklist final (avaliar antes de chamar a ferramenta de geração)

- O post prova competência específica, não apenas interesse pelo tema?
- Alguém que lê esse post entenderia, na prática, o que essa pessoa sabe fazer?
- O texto soa como algo que só essa pessoa escreveria, ou poderia ter saído de qualquer
  perfil de IA no LinkedIn?
- Existe alguma frase que, isolada, funcionaria como gancho de recrutador ("preciso falar
  com essa pessoa")?

## Fluxo de conversa

Converse com o usuário para coletar o necessário (modo, conteúdo de origem ou matéria-prima
recente, pilar) fazendo UMA pergunta por vez, de forma direta. Quando tiver o suficiente,
chame a ferramenta `generate_linkedin_post` com o resultado final já avaliado pelo checklist
acima. Preencha o campo `checklist` com respostas honestas (true/false) — se algum item for
false, continue refinando o post antes de chamar a ferramenta."""

TOOLS = [
    {
        "name": "generate_linkedin_post",
        "description": "Registra o post final (reformulado ou gerado) já avaliado pelo checklist de posicionamento.",
        "input_schema": {
            "type": "object",
            "properties": {
                "modo": {
                    "type": "string",
                    "enum": ["reformulacao", "geracao"],
                    "description": "Modo de operação usado nesta rodada."
                },
                "pilar": {
                    "type": "string",
                    "enum": [
                        "bastidor_tecnico_estrategico",
                        "ponto_de_vista_contraintuitivo",
                        "traducao_de_complexidade",
                        "case_ou_resultado_concreto",
                        "provocacao_de_mercado",
                        "nenhum_pilar_identificado"
                    ],
                    "description": "Pilar de conteúdo predominante do post."
                },
                "pilar_justificativa": {
                    "type": "string",
                    "description": "Por que este pilar foi escolhido (ou por que o conteúdo original não se encaixava em nenhum)."
                },
                "titulo_interno": {
                    "type": "string",
                    "description": "Título curto só para identificação do post nos arquivos (não é o post em si)."
                },
                "versao_enxuta": {
                    "type": "string",
                    "description": "Versão final do post, enxuta (maior alcance). Obrigatória em todos os casos."
                },
                "versao_densa": {
                    "type": "string",
                    "description": "Versão densa (autoridade técnica). Obrigatória no modo reformulação; opcional no modo geração."
                },
                "gancho_recrutador": {
                    "type": "string",
                    "description": "A frase do post que, isolada, funciona como gancho de recrutador."
                },
                "checklist": {
                    "type": "object",
                    "description": "Autoavaliação honesta do post final contra os quatro critérios do checklist.",
                    "properties": {
                        "prova_competencia_especifica": {"type": "boolean"},
                        "leitor_entende_o_que_sabe_fazer": {"type": "boolean"},
                        "voz_autentica_nao_generica": {"type": "boolean"},
                        "possui_gancho_de_recrutador": {"type": "boolean"}
                    },
                    "required": [
                        "prova_competencia_especifica",
                        "leitor_entende_o_que_sabe_fazer",
                        "voz_autentica_nao_generica",
                        "possui_gancho_de_recrutador"
                    ]
                }
            },
            "required": ["modo", "pilar", "pilar_justificativa", "versao_enxuta", "gancho_recrutador", "checklist"]
        }
    }
]

PILAR_LABELS = {
    "bastidor_tecnico_estrategico": "Bastidor técnico-estratégico",
    "ponto_de_vista_contraintuitivo": "Ponto de vista contra-intuitivo",
    "traducao_de_complexidade": "Tradução de complexidade",
    "case_ou_resultado_concreto": "Case ou resultado concreto",
    "provocacao_de_mercado": "Provocação de mercado",
    "nenhum_pilar_identificado": "Nenhum pilar identificado (conteúdo original fora do escopo)",
}


def load_state(state_path: str) -> dict:
    path = Path(state_path)
    if not path.exists():
        return {"history": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state_path: str, state: dict) -> None:
    Path(state_path).write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def describe_state(state: dict) -> str:
    history = state.get("history", [])
    if not history:
        return "Nenhum post registrado ainda neste histórico. Nenhuma restrição de rodízio se aplica."
    last = history[-1]
    days_since = (date.today() - date.fromisoformat(last["data"])).days
    recent_pillars = ", ".join(PILAR_LABELS.get(h["pilar"], h["pilar"]) for h in history[-3:])
    cadence_note = (
        f"Já se passaram {days_since} dias desde o último post (em {last['data']}). "
        + ("Cadência quinzenal em dia." if days_since < 15 else "ATENÇÃO: cadência mínima de 15 dias estourada, priorize gerar um post agora.")
    )
    return (
        f"Último pilar usado: {PILAR_LABELS.get(last['pilar'], last['pilar'])} — não repita este pilar agora. "
        f"Últimos pilares (mais recente por último): {recent_pillars}. {cadence_note}"
    )


def build_markdown(data: dict, state: dict | None = None) -> str:
    pilar_label = PILAR_LABELS.get(data["pilar"], data["pilar"])
    modo_label = "Reformulação" if data["modo"] == "reformulacao" else "Geração periódica"
    checklist = data.get("checklist", {})

    def check_mark(value: bool) -> str:
        return "✅" if value else "⚠️"

    lines = [
        f"# {data.get('titulo_interno', 'Post LinkedIn')}",
        "",
        f"- **Modo:** {modo_label}",
        f"- **Pilar:** {pilar_label}",
        f"- **Gerado em:** {date.today().isoformat()}",
        "",
        "## Justificativa do pilar",
        "",
        data["pilar_justificativa"],
        "",
        "## Versão enxuta (maior alcance)",
        "",
        data["versao_enxuta"],
        "",
    ]

    if data.get("versao_densa"):
        lines += [
            "## Versão densa (autoridade técnica)",
            "",
            data["versao_densa"],
            "",
        ]

    lines += [
        "## Gancho de recrutador",
        "",
        f"> {data['gancho_recrutador']}",
        "",
        "## Checklist final",
        "",
        f"- {check_mark(checklist.get('prova_competencia_especifica', False))} Prova competência específica, não apenas interesse pelo tema",
        f"- {check_mark(checklist.get('leitor_entende_o_que_sabe_fazer', False))} Quem lê entende, na prática, o que essa pessoa sabe fazer",
        f"- {check_mark(checklist.get('voz_autentica_nao_generica', False))} Soa como algo que só essa pessoa escreveria",
        f"- {check_mark(checklist.get('possui_gancho_de_recrutador', False))} Contém uma frase que funciona como gancho de recrutador",
        "",
        f"Perfil: {PROFILE_URL}",
    ]

    return "\n".join(lines)


def process_tool_call(tool_name: str, tool_input: dict, output_path: str, state_path: str) -> str:
    if tool_name != "generate_linkedin_post":
        return "Unknown tool."

    state = load_state(state_path)
    markdown = build_markdown(tool_input, state)
    Path(output_path).write_text(markdown, encoding="utf-8")

    state.setdefault("history", []).append({
        "data": date.today().isoformat(),
        "pilar": tool_input["pilar"],
        "modo": tool_input["modo"],
        "arquivo": output_path,
    })
    save_state(state_path, state)

    return f"Post salvo em: {output_path}. Estado de rodízio/cadência atualizado em: {state_path}"


def load_content_file(path: str) -> str:
    content = Path(path).read_text(encoding="utf-8")
    return f"Tenho um conteúdo existente para reformular. Segue o texto:\n\n{content}"


def run_agent(mode: str | None, content_file: str | None, output_path: str, state_path: str):
    client = anthropic.Anthropic()
    state = load_state(state_path)
    messages = []

    print("\n━━━ Agente de Posicionamento Estratégico — LinkedIn (IA & Dados) ━━━")
    print(f"Powered by Claude Opus 4.8 | Perfil: {PROFILE_URL} | Digite 'exit' para sair\n")
    print(f"[Estado de rodízio/cadência] {describe_state(state)}\n")

    state_note = f"\n\n(Estado atual do rodízio de pilares e cadência: {describe_state(state)})"

    if mode == "reformular" and content_file:
        user_input = load_content_file(content_file) + state_note
        print(f"[Conteúdo carregado de: {content_file}]\n")
    elif mode == "reformular":
        print("Modo: Reformulação. Cole o conteúdo existente (rascunho, post antigo, ideia, case).\n")
        user_input = input("Você: ").strip() + state_note
    elif mode == "gerar":
        print("Modo: Geração periódica. Houve algum evento, decisão, aprendizado ou conversa nas")
        print("últimas duas semanas que vale virar conteúdo? Se não houver, diga 'nada específico'.\n")
        user_input = input("Você: ").strip() + state_note
    else:
        print("Você quer (1) reformular um conteúdo existente ou (2) gerar um post novo?\n")
        user_input = input("Você: ").strip()
        if user_input.lower() in ("exit", "quit"):
            return
        user_input += state_note

    while True:
        messages.append({"role": "user", "content": user_input})

        with client.messages.stream(
            model=MODEL,
            max_tokens=8192,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            thinking={"type": "adaptive"},
            messages=messages,
        ) as stream:
            response = stream.get_final_message()

        messages.append({"role": "assistant", "content": response.content})

        tool_use_block = None
        text_parts = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_use_block = block

        if text_parts:
            print(f"\nAgente: {''.join(text_parts)}\n")

        if tool_use_block:
            result = process_tool_call(tool_use_block.name, tool_use_block.input, output_path, state_path)
            print(f"\n✓ {result}\n")

            messages.append({
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": tool_use_block.id, "content": result}]
            })

            with client.messages.stream(
                model=MODEL,
                max_tokens=512,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                thinking={"type": "adaptive"},
                messages=messages,
            ) as stream:
                final = stream.get_final_message()

            for block in final.content:
                if block.type == "text" and block.text.strip():
                    print(f"Agente: {block.text}\n")
            break

        if response.stop_reason == "end_turn":
            user_input = input("Você: ").strip()
            if user_input.lower() in ("exit", "quit"):
                break


def main():
    parser = argparse.ArgumentParser(
        description="Agente de Posicionamento Estratégico — LinkedIn (IA & Dados)"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["reformular", "gerar"],
        help="Modo de operação: 'reformular' (Modo 1) ou 'gerar' (Modo 2 — geração periódica)."
    )
    parser.add_argument(
        "--content", "-c",
        metavar="FILE",
        help="Arquivo de texto/markdown com o conteúdo existente a reformular (usado com --mode reformular)."
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        default=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        help="Arquivo Markdown de saída (padrão: linkedin_post_TIMESTAMP.md)"
    )
    parser.add_argument(
        "--state", "-s",
        metavar="FILE",
        default="linkedin_state.json",
        help="Arquivo de estado para rodízio de pilares e controle de cadência (padrão: linkedin_state.json)"
    )
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    run_agent(args.mode, args.content, args.output, args.state)


if __name__ == "__main__":
    main()
