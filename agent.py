#!/usr/bin/env python3
"""Executive One-Pager Agent — generates beautiful HTML/CSS executive presentations."""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = """You are an executive communications specialist with deep expertise in creating
compelling one-page presentations for C-suite and board audiences.

Your role is to gather information about a topic through a focused conversation, then produce
a visually stunning, information-dense one-page executive briefing as HTML/CSS.

## Conversation phase
Ask targeted questions to gather:
1. Topic and context (what decision or update this supports)
2. Target audience (CEO, board, investors, etc.)
3. Key metrics or data points
4. Main findings or insights (2-4 bullet points)
5. Recommendations or next steps
6. Timeframe and urgency

Ask ONE question at a time. Be concise and professional. When you have enough information
(typically 5-7 exchanges), inform the user you're ready to generate the one-pager and ask
for confirmation.

## Generation phase
When the user confirms, call the `generate_one_pager` tool with all collected information.

## HTML/CSS design principles
The one-pager must:
- Fit on a single A4/Letter page (print-optimized)
- Use a professional executive visual design: clean layout, strong typography, strategic use of color
- Include a header with title, date, and audience label
- Organize content in clear sections with visual hierarchy
- Be print-ready (works with browser "Print to PDF")
- Use a cohesive color palette (deep navy/slate + accent color)
- Avoid clipart or placeholder images — use CSS-only design elements"""

TOOLS = [
    {
        "name": "generate_one_pager",
        "description": "Generate the executive one-pager HTML/CSS document with all collected information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Presentation title"},
                "subtitle": {"type": "string", "description": "Optional subtitle or tagline"},
                "audience": {"type": "string", "description": "Target audience (e.g. Board of Directors)"},
                "date": {"type": "string", "description": "Date or period covered"},
                "executive_summary": {"type": "string", "description": "2-3 sentence executive summary"},
                "key_metrics": {
                    "type": "array",
                    "description": "Key metrics/KPIs to highlight (max 4)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "label": {"type": "string"},
                            "value": {"type": "string"},
                            "trend": {"type": "string", "description": "up, down, or neutral"},
                            "note": {"type": "string", "description": "brief context"}
                        },
                        "required": ["label", "value"]
                    }
                },
                "insights": {
                    "type": "array",
                    "description": "Key findings/insights (2-4 items)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "heading": {"type": "string"},
                            "detail": {"type": "string"}
                        },
                        "required": ["heading", "detail"]
                    }
                },
                "recommendations": {
                    "type": "array",
                    "description": "Recommended actions (2-3 items)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string"},
                            "rationale": {"type": "string"},
                            "priority": {"type": "string", "description": "High, Medium, or Low"}
                        },
                        "required": ["action", "priority"]
                    }
                },
                "footer_note": {"type": "string", "description": "Optional confidentiality notice or source note"},
                "accent_color": {
                    "type": "string",
                    "description": "Hex color for accent (e.g. #E84855 for red, #2ECC71 for green). Match to topic sentiment."
                }
            },
            "required": ["title", "audience", "executive_summary", "key_metrics", "insights", "recommendations"]
        }
    }
]


def build_html(data: dict) -> str:
    accent = data.get("accent_color", "#1A56DB")
    date_str = data.get("date", datetime.now().strftime("%B %Y"))
    footer = data.get("footer_note", "CONFIDENTIAL — For internal use only")
    subtitle = data.get("subtitle", "")

    metrics_html = ""
    for m in data.get("key_metrics", []):
        trend = m.get("trend", "neutral")
        arrow = "↑" if trend == "up" else ("↓" if trend == "down" else "→")
        arrow_color = "#2ECC71" if trend == "up" else ("#E84855" if trend == "down" else "#94A3B8")
        note = f'<span class="metric-note">{m["note"]}</span>' if m.get("note") else ""
        metrics_html += f"""
        <div class="metric-card">
            <div class="metric-value">{m["value"]} <span style="color:{arrow_color};font-size:1.1rem">{arrow}</span></div>
            <div class="metric-label">{m["label"]}</div>
            {note}
        </div>"""

    insights_html = ""
    for i, ins in enumerate(data.get("insights", []), 1):
        insights_html += f"""
        <div class="insight-item">
            <div class="insight-number" style="background:{accent}">{i}</div>
            <div>
                <div class="insight-heading">{ins["heading"]}</div>
                <div class="insight-detail">{ins["detail"]}</div>
            </div>
        </div>"""

    rec_html = ""
    priority_colors = {"High": "#E84855", "Medium": "#F59E0B", "Low": "#2ECC71"}
    for rec in data.get("recommendations", []):
        p_color = priority_colors.get(rec.get("priority", "Medium"), "#F59E0B")
        rationale = f'<div class="rec-rationale">{rec["rationale"]}</div>' if rec.get("rationale") else ""
        rec_html += f"""
        <div class="rec-item">
            <span class="priority-badge" style="background:{p_color}">{rec.get("priority","")}</span>
            <div>
                <div class="rec-action">{rec["action"]}</div>
                {rationale}
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{data["title"]}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #F1F5F9;
    color: #1E293B;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .page {{
    width: 210mm;
    min-height: 297mm;
    margin: 20px auto;
    background: #fff;
    box-shadow: 0 4px 24px rgba(0,0,0,0.12);
    display: flex;
    flex-direction: column;
  }}

  /* HEADER */
  .header {{
    background: #0F172A;
    padding: 24px 32px 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 4px solid {accent};
  }}
  .header-left {{ flex: 1; }}
  .audience-tag {{
    display: inline-block;
    background: {accent};
    color: #fff;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
    margin-bottom: 8px;
  }}
  .header-title {{
    color: #F8FAFC;
    font-size: 22px;
    font-weight: 800;
    line-height: 1.15;
  }}
  .header-subtitle {{
    color: #94A3B8;
    font-size: 12px;
    font-weight: 400;
    margin-top: 4px;
  }}
  .header-right {{
    text-align: right;
    color: #64748B;
    font-size: 11px;
    line-height: 1.6;
  }}
  .header-date {{
    color: #CBD5E1;
    font-size: 13px;
    font-weight: 600;
  }}

  /* BODY */
  .body {{ flex: 1; padding: 24px 32px; display: grid; gap: 20px; }}

  /* EXECUTIVE SUMMARY */
  .summary-box {{
    background: #F8FAFC;
    border-left: 4px solid {accent};
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
  }}
  .section-label {{
    font-size: 8px;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: {accent};
    margin-bottom: 6px;
  }}
  .summary-text {{
    font-size: 12.5px;
    line-height: 1.55;
    color: #334155;
  }}

  /* METRICS */
  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }}
  .metric-card {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 14px 16px;
    text-align: center;
  }}
  .metric-value {{
    font-size: 22px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1;
    margin-bottom: 4px;
  }}
  .metric-label {{
    font-size: 10px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }}
  .metric-note {{
    display: block;
    font-size: 9px;
    color: #94A3B8;
    margin-top: 4px;
  }}

  /* TWO-COLUMN LAYOUT */
  .two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }}

  /* INSIGHTS */
  .section-title {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #E2E8F0;
  }}
  .insight-item {{
    display: flex;
    gap: 12px;
    margin-bottom: 12px;
    align-items: flex-start;
  }}
  .insight-number {{
    min-width: 22px;
    height: 22px;
    border-radius: 50%;
    color: #fff;
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
  }}
  .insight-heading {{
    font-size: 11.5px;
    font-weight: 600;
    color: #1E293B;
    margin-bottom: 2px;
  }}
  .insight-detail {{
    font-size: 10.5px;
    color: #475569;
    line-height: 1.45;
  }}

  /* RECOMMENDATIONS */
  .rec-item {{
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    align-items: flex-start;
  }}
  .priority-badge {{
    color: #fff;
    font-size: 8px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 3px 7px;
    border-radius: 3px;
    flex-shrink: 0;
    margin-top: 2px;
  }}
  .rec-action {{
    font-size: 11.5px;
    font-weight: 600;
    color: #1E293B;
    margin-bottom: 2px;
  }}
  .rec-rationale {{
    font-size: 10px;
    color: #64748B;
    line-height: 1.4;
  }}

  /* FOOTER */
  .footer {{
    background: #0F172A;
    padding: 10px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .footer-left {{
    font-size: 8.5px;
    color: #475569;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }}
  .footer-bar {{
    height: 3px;
    width: 40px;
    background: {accent};
    border-radius: 2px;
  }}

  @media print {{
    body {{ background: #fff; }}
    .page {{ margin: 0; box-shadow: none; width: 100%; min-height: 100vh; }}
  }}
</style>
</head>
<body>
<div class="page">
  <div class="header">
    <div class="header-left">
      <div class="audience-tag">{data["audience"]}</div>
      <div class="header-title">{data["title"]}</div>
      {"<div class='header-subtitle'>" + subtitle + "</div>" if subtitle else ""}
    </div>
    <div class="header-right">
      <div class="header-date">{date_str}</div>
      <div>Executive Briefing</div>
    </div>
  </div>

  <div class="body">
    <div class="summary-box">
      <div class="section-label">Executive Summary</div>
      <div class="summary-text">{data["executive_summary"]}</div>
    </div>

    <div>
      <div class="section-label">Key Metrics</div>
      <div class="metrics-grid">{metrics_html}</div>
    </div>

    <div class="two-col">
      <div>
        <div class="section-title">Key Findings</div>
        {insights_html}
      </div>
      <div>
        <div class="section-title">Recommendations</div>
        {rec_html}
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="footer-left">{footer}</div>
    <div class="footer-bar"></div>
  </div>
</div>
</body>
</html>"""


def process_tool_call(tool_name: str, tool_input: dict, output_path: str) -> str:
    if tool_name == "generate_one_pager":
        html = build_html(tool_input)
        Path(output_path).write_text(html, encoding="utf-8")
        return f"One-pager generated successfully and saved to: {output_path}"
    return "Unknown tool."


def load_briefing(path: str) -> str:
    content = Path(path).read_text(encoding="utf-8")
    return f"I have a briefing file with the following content. Please use it to generate the one-pager:\n\n{content}"


def run_agent(briefing_file: str | None, output_path: str):
    client = anthropic.Anthropic()
    messages = []

    print("\n━━━ Executive One-Pager Agent ━━━")
    print("Powered by Claude Opus 4.8 | Type 'exit' to quit\n")

    if briefing_file:
        user_input = load_briefing(briefing_file)
        print(f"[Briefing loaded from: {briefing_file}]\n")
    else:
        print("Hello! I'll help you create a professional executive one-pager.")
        print("Let's start — what topic or decision does this presentation need to address?\n")
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            return

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
            print(f"\nAgent: {''.join(text_parts)}\n")

        if tool_use_block:
            result = process_tool_call(tool_use_block.name, tool_use_block.input, output_path)
            print(f"\n✓ {result}")
            print(f"\nOpen {output_path} in your browser and use File → Print → Save as PDF to export.\n")

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
                    print(f"Agent: {block.text}\n")
            break

        if response.stop_reason == "end_turn":
            if briefing_file:
                print("[No tool was called. Providing the briefing again as explicit request.]\n")
                user_input = "Please generate the one-pager now based on the briefing I provided."
                briefing_file = None
                continue

            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit"):
                break


def main():
    parser = argparse.ArgumentParser(
        description="Executive One-Pager Agent — creates stunning executive briefings as HTML/CSS"
    )
    parser.add_argument(
        "--briefing", "-b",
        metavar="FILE",
        help="Path to a text/markdown briefing file (skips interactive Q&A)"
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        default=f"one_pager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
        help="Output HTML file path (default: one_pager_TIMESTAMP.html)"
    )
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    run_agent(args.briefing, args.output)


if __name__ == "__main__":
    main()
