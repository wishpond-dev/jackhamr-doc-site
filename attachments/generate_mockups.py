#!/usr/bin/env python3
"""Generate 7 mockup PNGs for the JackHamr documentation website spec."""
import os
from playwright.sync_api import sync_playwright

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Shared CSS — the design system from jackhamr.ai
BASE_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: #0f172a;
  color: #fff;
}
.mono { font-family: 'JetBrains Mono', 'Courier New', monospace; }

/* Nav */
.nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  padding: 14px 48px;
  display: flex; align-items: center; justify-content: space-between;
}
.nav-brand { font-weight: 700; font-size: 18px; letter-spacing: -0.02em; }
.nav-brand .dot { color: #7c3aed; }
.nav-links { display: flex; gap: 28px; }
.nav-link {
  font-size: 13px; color: #94a3b8; text-decoration: none; font-weight: 500;
  transition: color 0.2s;
}
.nav-link.active { color: #fff; }
.nav-link:hover { color: #fff; }
.nav-cta {
  background: #7c3aed; color: #fff; border: none;
  border-radius: 8px; padding: 8px 18px; font-size: 13px; font-weight: 600;
  font-family: inherit; cursor: pointer;
}

/* Layout */
.section { max-width: 1280px; margin: 0 auto; padding: 80px 48px; }
.section-label {
  font-size: 12px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1.5px; color: #7c3aed; margin-bottom: 12px;
}
.section-title {
  font-size: 32px; font-weight: 700; letter-spacing: -0.03em;
  margin-bottom: 16px; line-height: 1.2;
}
.section-desc {
  font-size: 16px; color: #94a3b8; line-height: 1.7;
  max-width: 720px; margin-bottom: 40px;
}

/* Cards */
.card-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 28px;
  transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
}
.card:hover {
  border-color: rgba(124, 58, 237, 0.4);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(124, 58, 237, 0.1);
}
.card-icon {
  width: 44px; height: 44px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 18px; font-size: 20px;
}
.card h3 { font-size: 17px; font-weight: 600; margin-bottom: 10px; }
.card p { font-size: 13px; color: #94a3b8; line-height: 1.65; }
.card ul { list-style: none; padding: 0; margin-top: 12px; }
.card li {
  font-size: 13px; color: #94a3b8; line-height: 1.6;
  padding-left: 18px; position: relative; margin-bottom: 6px;
}
.card li::before {
  content: '▸'; position: absolute; left: 0; color: #7c3aed;
}

/* Pipeline */
.pipeline-bar {
  display: flex; gap: 0; margin: 40px 0; border-radius: 12px; overflow: hidden;
}
.pipeline-phase {
  flex: 1; padding: 20px 16px; text-align: center;
  background: rgba(255,255,255,0.02);
  border-right: 1px solid rgba(255,255,255,0.05);
  transition: background 0.4s, color 0.4s;
}
.pipeline-phase:last-child { border-right: none; }
.pipeline-phase .phase-icon { font-size: 20px; margin-bottom: 8px; opacity: 0.4; }
.pipeline-phase .phase-name {
  font-size: 13px; font-weight: 600; color: #94a3b8;
  font-family: 'JetBrains Mono', monospace;
}
.pipeline-phase.lit {
  background: rgba(124, 58, 237, 0.12);
}
.pipeline-phase.lit .phase-icon { opacity: 1; }
.pipeline-phase.lit .phase-name { color: #fff; }

/* Reveal animation */
.reveal { opacity: 0.3; transform: translateY(15px); transition: all 0.6s ease-out; }
.reveal.revealed { opacity: 1; transform: translateY(0); }

/* Hero */
.hero { padding: 120px 48px 60px; max-width: 1280px; margin: 0 auto; }
.hero h1 {
  font-size: 48px; font-weight: 700; letter-spacing: -0.04em;
  line-height: 1.1; margin-bottom: 20px;
}
.hero h1 .accent { color: #7c3aed; }
.hero .tagline { font-size: 18px; color: #94a3b8; max-width: 640px; line-height: 1.6; }

/* Code block */
.code-block {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 18px 22px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12.5px; line-height: 1.7; color: #c7d2fe;
  margin-top: 16px;
}
.code-block .comment { color: #6b7280; }
.code-block .key { color: #818cf8; }
.code-block .str { color: #34d399; }

/* Footer */
.footer {
  border-top: 1px solid rgba(255,255,255,0.06);
  padding: 40px 48px; text-align: center;
  max-width: 1280px; margin: 0 auto;
}
.footer p { font-size: 13px; color: #64748b; }

/* Accent colors */
.bg-violet { background: rgba(124, 58, 237, 0.15); color: #a78bfa; }
.bg-emerald { background: rgba(52, 211, 153, 0.15); color: #34d399; }
.bg-sky { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
.bg-amber { background: rgba(251, 191, 36, 0.15); color: #fbbf24; }
.bg-indigo { background: rgba(129, 140, 248, 0.15); color: #818cf8; }
.bg-teal { background: rgba(45, 212, 191, 0.15); color: #2dd4bf; }
.bg-orange { background: rgba(251, 146, 60, 0.15); color: #fb923c; }
"""

def nav_html(active=None):
    links = [
        ("overview", "Overview"),
        ("pipeline", "Pipeline"),
        ("agents", "Agents"),
        ("orchestration", "Orchestration"),
        ("skills", "Skills"),
        ("memory", "Memory"),
        ("gates", "Gates"),
        ("environments", "Environments"),
        ("board", "Board"),
        ("integrations", "Integrations"),
        ("customization", "Customization"),
    ]
    items = ""
    for sid, label in links:
        cls = "nav-link active" if sid == active else "nav-link"
        items += f'<a class="{cls}" href="#{sid}">{label}</a>'
    return f"""
    <nav class="nav">
      <div class="nav-brand">Jack<span class="dot">Hamr</span></div>
      <div class="nav-links">{items}</div>
      <button class="nav-cta">Get Started</button>
    </nav>
    """

def page_shell(body, extra_css=""):
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{BASE_CSS}{extra_css}</style>
</head><body>
{body}
</body></html>"""


# ============================================================
# Mockup A — Hero / Default State
# ============================================================
def mockup_a():
    body = nav_html() + """
    <div class="hero">
      <div class="section-label">AI Agent Orchestration Platform</div>
      <h1>Jack<span class="accent">Hamr</span> ships software<br>end-to-end.</h1>
      <p class="tagline">Specialist AI agents that spec, plan, build, test, and review code on hosted cloud environments. They learn from every task, so they get smarter the more you work together.</p>
    </div>

    <div class="section" id="overview" style="padding-top: 20px;">
      <div class="section-label">Overview</div>
      <div class="section-title">What JackHamr Is</div>
      <div class="section-desc">
        JackHamr is an AI agent orchestration platform. You give it a task — it provisions a cloud environment, plans the work, writes the code, tests it, reviews it, and ships it. Every agent has a name, a personality, and a pipeline it runs end to end.
      </div>

      <div class="pipeline-bar">
        <div class="pipeline-phase"><div class="phase-icon">📋</div><div class="phase-name">Spec</div></div>
        <div class="pipeline-phase"><div class="phase-icon">🗺️</div><div class="phase-name">Plan</div></div>
        <div class="pipeline-phase"><div class="phase-icon">🔨</div><div class="phase-name">Build</div></div>
        <div class="pipeline-phase"><div class="phase-icon">🧪</div><div class="phase-name">Test</div></div>
        <div class="pipeline-phase"><div class="phase-icon">👁️</div><div class="phase-name">Review</div></div>
        <div class="pipeline-phase"><div class="phase-icon">🚀</div><div class="phase-name">Ship</div></div>
      </div>

      <div class="card-grid" style="margin-top: 40px;">
        <div class="card reveal">
          <div class="card-icon bg-violet">⚡</div>
          <h3>Full Autonomy</h3>
          <p>Spec → plan → build → test → review → ship — without human intervention between phases.</p>
        </div>
        <div class="card reveal">
          <div class="card-icon bg-emerald">🤖</div>
          <h3>Named Agents</h3>
          <p>Every agent has a name, personality, and soul prompt. Not anonymous bots — teammates.</p>
        </div>
        <div class="card reveal">
          <div class="card-icon bg-sky">👁️</div>
          <h3>Watch It Think</h3>
          <p>Real-time status, mood, and progress. You see what the agent is doing at every step.</p>
        </div>
      </div>
    </div>
    """
    return page_shell(body)


# ============================================================
# Mockup B — Pipeline Section Active (phases lighting up)
# ============================================================
def mockup_b():
    body = nav_html("pipeline") + """
    <div class="section" id="pipeline">
      <div class="section-label">Pipeline Lifecycle</div>
      <div class="section-title">Spec → Plan → Build → Test → Review → Ship</div>
      <div class="section-desc">
        Every task moves through six phases. The orchestrator spawns a phase-specific sub-agent for each, then checks in with you only when a decision is needed.
      </div>

      <div class="pipeline-bar">
        <div class="pipeline-phase lit"><div class="phase-icon">📋</div><div class="phase-name">Spec</div></div>
        <div class="pipeline-phase lit"><div class="phase-icon">🗺️</div><div class="phase-name">Plan</div></div>
        <div class="pipeline-phase lit"><div class="phase-icon">🔨</div><div class="phase-name">Build</div></div>
        <div class="pipeline-phase"><div class="phase-icon">🧪</div><div class="phase-name">Test</div></div>
        <div class="pipeline-phase"><div class="phase-icon">👁️</div><div class="phase-name">Review</div></div>
        <div class="pipeline-phase"><div class="phase-icon">🚀</div><div class="phase-name">Ship</div></div>
      </div>

      <div class="card-grid">
        <div class="card revealed">
          <div class="card-icon bg-violet">📋</div>
          <h3>Spec</h3>
          <p>The spec-builder sub-agent reads the brief and clarifications, writes <code class="mono">spec.md</code> with acceptance criteria, generates mockups, and produces a PDF.</p>
        </div>
        <div class="card revealed">
          <div class="card-icon bg-indigo">🗺️</div>
          <h3>Plan</h3>
          <p>The implementation-planner reads the spec, maps the codebase, and writes a detailed implementation plan with file-level changes.</p>
        </div>
        <div class="card revealed">
          <div class="card-icon bg-emerald">🔨</div>
          <h3>Build</h3>
          <p>The developer sub-agent implements the plan — writes code, runs builds, fixes errors — until the feature compiles and works.</p>
        </div>
        <div class="card reveal" style="opacity: 0.35;">
          <div class="card-icon bg-amber">🧪</div>
          <h3>Test</h3>
          <p>The QA tester runs E2E and unit tests, validates acceptance criteria, and reports pass/fail per test case.</p>
        </div>
        <div class="card reveal" style="opacity: 0.2;">
          <div class="card-icon bg-sky">👁️</div>
          <h3>Review</h3>
          <p>The code reviewer audits the diff for quality, security, and spec compliance before the change can ship.</p>
        </div>
        <div class="card reveal" style="opacity: 0.1;">
          <div class="card-icon bg-teal">🚀</div>
          <h3>Ship</h3>
          <p>Commits land on the feature branch, PR is created, and the pipeline completes. The board card moves to "Shipped".</p>
        </div>
      </div>
    </div>
    """
    return page_shell(body)


# ============================================================
# Mockup C — Mid-Scroll with Nav Active State, Reveal In Progress
# ============================================================
def mockup_c():
    body = nav_html("orchestration") + """
    <div class="section" id="orchestration">
      <div class="section-label">Orchestration Model</div>
      <div class="section-title">The Conductor Spawns Phase-Specific Sub-Agents</div>
      <div class="section-desc">
        A conductor sub-agent owns the pipeline run. It spawns the right specialist sub-agent for each phase, passes context forward, and enforces approval gates between phases.
      </div>

      <div class="code-block">
<span class="comment"># Orchestration flow</span>
<span class="key">orchestrator</span> ──► <span class="key">spec-builder</span>     <span class="comment"># writes spec.md + mockups + PDF</span>
    │                         │
    │◄────────────────────────┘  <span class="comment"># Gate A: user approves spec</span>
    │
    ├─► <span class="key">impl-planner</span>     <span class="comment"># writes implementation plan</span>
    │                         │
    │◄────────────────────────┘  <span class="comment"># Gate B: user approves plan</span>
    │
    ├─► <span class="key">developer</span>        <span class="comment"># writes the code</span>
    ├─► <span class="key">qa-tester</span>        <span class="comment"># runs E2E + unit tests</span>
    └─► <span class="key">code-reviewer</span>    <span class="comment"># audits the diff</span>
      </div>

      <div class="card-grid" style="margin-top: 32px;">
        <div class="card revealed">
          <div class="card-icon bg-violet">🎼</div>
          <h3>Conductor</h3>
          <ul>
            <li>Owns the pipeline run lifecycle</li>
            <li>Spawns phase-specific sub-agents</li>
            <li>Passes context forward between phases</li>
            <li>Enforces approval gates</li>
          </ul>
        </div>
        <div class="card reveal" style="opacity: 0.45; transform: translateY(10px);">
          <div class="card-icon bg-indigo">🤖</div>
          <h3>Phase Sub-Agents</h3>
          <ul>
            <li>spec-builder, impl-planner, developer</li>
            <li>qa-tester, code-reviewer</li>
            <li>Each runs in isolation</li>
            <li>Results flow back to conductor</li>
          </ul>
        </div>
        <div class="card reveal" style="opacity: 0.15; transform: translateY(20px);">
          <div class="card-icon bg-emerald">✅</div>
          <h3>Approval Gates</h3>
          <ul>
            <li>Gate A: spec approval</li>
            <li>Gate B: plan approval</li>
            <li>Human decides what ships</li>
          </ul>
        </div>
      </div>
    </div>
    """
    return page_shell(body)


# ============================================================
# Mockup D — Agents & Soul Prompts Section (fully revealed)
# ============================================================
def mockup_d():
    body = nav_html("agents") + """
    <div class="section" id="agents">
      <div class="section-label">Agent System</div>
      <div class="section-title">Every Agent Has a Soul</div>
      <div class="section-desc">
        Agents are not anonymous bots. Each one has a name, a personality defined by a soul prompt, and identity traits that shape how it communicates and approaches problems.
      </div>

      <div class="card-grid">
        <div class="card">
          <div class="card-icon bg-violet">🧹</div>
          <h3>Soul Prompts</h3>
          <p>Custom system prompts define agent personality — tone, approach, values. The soul prompt is the agent's identity.</p>
          <div class="code-block">
<span class="comment"># Example soul prompt</span>
<span class="str">"Quietly competent, direct,</span>
<span class="str"> dry wit. Gets things done</span>
<span class="str"> without drama."</span>
          </div>
        </div>
        <div class="card">
          <div class="card-icon bg-indigo">🎭</div>
          <h3>Identity Traits</h3>
          <p>Traits shape communication style — how the agent talks in Slack, how it formats responses, how it handles ambiguity.</p>
          <ul>
            <li>Tone: direct, dry wit</li>
            <li>Style: concise, no filler</li>
            <li>Approach: finish, don't promise</li>
            <li>Personality: quietly competent</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-icon bg-emerald">🏷️</div>
          <h3>Named Agents</h3>
          <p>Every agent gets a name (e.g. "Rachel", "Atlas", "Nexus"). Names make them feel like teammates, not services.</p>
          <ul>
            <li>Per-agent customization</li>
            <li>Organization-wide sharing</li>
            <li>Clone and reuse setups</li>
            <li>Distinct role per agent</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="section" id="skills" style="padding-top: 0;">
      <div class="section-label">Skills System</div>
      <div class="section-title">Custom Skills with Progressive Disclosure</div>
      <div class="section-desc">
        Skills are reusable agent capabilities. Only the name and description are loaded into context — full instructions are fetched on demand when the skill triggers. Always-on skills apply to every turn without loading.
      </div>
      <div class="card-grid">
        <div class="card">
          <div class="card-icon bg-sky">📦</div>
          <h3>Custom Skills</h3>
          <p>Reusable capabilities — code reviewers, spec builders, domain-specific workflows. Created and shared across your organization.</p>
        </div>
        <div class="card">
          <div class="card-icon bg-amber">🔓</div>
          <h3>Progressive Disclosure</h3>
          <p>Only name + description sit in context. Full instructions load via <code class="mono">skill_read</code> when the skill triggers — keeps context lean.</p>
        </div>
        <div class="card">
          <div class="card-icon bg-teal">⚡</div>
          <h3>Always-On Skills</h3>
          <p>Some skills are always active — their full instructions apply every turn. E.g. the memory-wiki skill that maintains a persistent knowledge base.</p>
        </div>
      </div>
    </div>
    """
    return page_shell(body)


# ============================================================
# Mockup E — Completion / Footer (all content loaded)
# ============================================================
def mockup_e():
    body = nav_html("customization") + """
    <div class="section" id="customization">
      <div class="section-label">Customization</div>
      <div class="section-title">Your Workflow. Your Agents. Your Rules.</div>
      <div class="section-desc">
        Bring your own LLM, create custom skills, build orchestrations. JackHamr adapts to how your team works.
      </div>
      <div class="card-grid">
        <div class="card">
          <div class="card-icon bg-violet">🧠</div>
          <h3>Bring Your Own LLM</h3>
          <p>OpenAI, Anthropic, or self-hosted. Use the model provider that fits your team and budget.</p>
        </div>
        <div class="card">
          <div class="card-icon bg-indigo">🎨</div>
          <h3>Dark / Light Mode</h3>
          <p>Match your preference. The platform persists your choice across sessions.</p>
        </div>
        <div class="card">
          <div class="card-icon bg-emerald">🔧</div>
          <h3>Custom Skills & Orchestrations</h3>
          <p>Build and share custom agent skills. Create orchestration pipelines for any workflow.</p>
        </div>
      </div>
    </div>

    <div class="footer">
      <p><strong>JackHamr</strong> — AI Agent Orchestration Platform. Spec it, plan it, build it, test it, review it, ship it.</p>
      <p style="margin-top: 8px;">Technical documentation · Sourced from first-hand knowledge of the system</p>
    </div>
    """
    return page_shell(body)


# ============================================================
# Mockup F — Mobile Responsive Layout
# ============================================================
def mockup_f():
    mobile_css = """
    .nav { padding: 12px 16px; }
    .nav-links { display: none; }
    .nav-cta { padding: 6px 14px; font-size: 12px; }
    .section { padding: 48px 16px; }
    .hero { padding: 60px 16px 30px; }
    .hero h1 { font-size: 30px; }
    .hero .tagline { font-size: 15px; }
    .section-title { font-size: 24px; }
    .card-grid { grid-template-columns: 1fr; gap: 16px; }
    .pipeline-bar { flex-wrap: wrap; }
    .pipeline-phase { flex: 1 0 33%; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .pipeline-phase .phase-name { font-size: 11px; }
    .code-block { font-size: 10px; padding: 12px 14px; }
    .footer { padding: 32px 16px; }
    """
    body = nav_html("pipeline") + """
    <div class="hero">
      <div class="section-label">AI Agent Orchestration Platform</div>
      <h1>Jack<span class="accent">Hamr</span> ships software end-to-end.</h1>
      <p class="tagline">Specialist AI agents that spec, plan, build, test, and review code on hosted cloud environments.</p>
    </div>

    <div class="section" id="pipeline" style="padding-top: 20px;">
      <div class="section-label">Pipeline Lifecycle</div>
      <div class="section-title">Spec → Plan → Build → Test → Review → Ship</div>
      <div class="pipeline-bar">
        <div class="pipeline-phase lit"><div class="phase-icon">📋</div><div class="phase-name">Spec</div></div>
        <div class="pipeline-phase lit"><div class="phase-icon">🗺️</div><div class="phase-name">Plan</div></div>
        <div class="pipeline-phase lit"><div class="phase-icon">🔨</div><div class="phase-name">Build</div></div>
        <div class="pipeline-phase"><div class="phase-icon">🧪</div><div class="phase-name">Test</div></div>
        <div class="pipeline-phase"><div class="phase-icon">👁️</div><div class="phase-name">Review</div></div>
        <div class="pipeline-phase"><div class="phase-icon">🚀</div><div class="phase-name">Ship</div></div>
      </div>

      <div class="card-grid">
        <div class="card">
          <div class="card-icon bg-violet">📋</div>
          <h3>Spec</h3>
          <p>The spec-builder writes spec.md with acceptance criteria, generates mockups, and produces a PDF.</p>
        </div>
        <div class="card">
          <div class="card-icon bg-indigo">🗺️</div>
          <h3>Plan</h3>
          <p>The implementation-planner maps the codebase and writes a detailed implementation plan.</p>
        </div>
        <div class="card">
          <div class="card-icon bg-emerald">🔨</div>
          <h3>Build</h3>
          <p>The developer implements the plan — writes code, runs builds, fixes errors.</p>
        </div>
      </div>
    </div>
    """
    return page_shell(body, mobile_css)


# ============================================================
# Mockup G — Error / Fallback State (CDN fail, no-JS)
# ============================================================
def mockup_g():
    fallback_css = """
    body { background: #0f172a; color: #fff; font-family: monospace; }
    .fallback-nav {
      background: rgba(15, 23, 42, 0.95);
      border-bottom: 1px solid #333;
      padding: 12px 24px; font-weight: bold; font-size: 16px;
    }
    .fallback-content { padding: 40px 24px; max-width: 700px; margin: 0 auto; }
    .fallback-content h1 { font-size: 28px; margin-bottom: 16px; }
    .fallback-content h2 { font-size: 18px; margin: 28px 0 10px; color: #aaa; }
    .fallback-content p { font-size: 14px; line-height: 1.7; color: #ccc; margin-bottom: 12px; }
    .fallback-content ul { padding-left: 20px; }
    .fallback-content li { font-size: 14px; color: #ccc; line-height: 1.7; }
    .fallback-note {
      background: rgba(251, 146, 60, 0.1);
      border: 1px solid rgba(251, 146, 60, 0.3);
      border-radius: 8px; padding: 12px 16px;
      font-size: 12px; color: #fb923c; margin-bottom: 24px;
    }
    .reveal { opacity: 1 !important; transform: none !important; }
    """
    body = """
    <div class="fallback-nav">JackHamr — Documentation</div>
    <div class="fallback-content">
      <div class="fallback-note">⚠ Stylesheet failed to load. Content is shown with minimal fallback styling.</div>
      <h1>JackHamr ships software end-to-end.</h1>
      <p>JackHamr is an AI agent orchestration platform. Specialist agents spec, plan, build, test, and review code on hosted cloud environments.</p>

      <h2>Pipeline Lifecycle</h2>
      <p>Spec → Plan → Build → Test → Review → Ship</p>
      <ul>
        <li>Spec: spec-builder writes spec.md, mockups, PDF</li>
        <li>Plan: implementation-planner maps codebase, writes plan</li>
        <li>Build: developer writes code, runs builds, fixes errors</li>
        <li>Test: QA tester runs E2E + unit tests</li>
        <li>Review: code-reviewer audits diff for quality</li>
        <li>Ship: commits land, PR created, card moves to Shipped</li>
      </ul>

      <h2>Agent System</h2>
      <p>Every agent has a name, personality (soul prompt), and identity traits.</p>

      <h2>Memory Wiki</h2>
      <p>Persistent knowledge base: inbox → librarian merge → pages.</p>
    </div>
    """
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>{fallback_css}</style>
</head><body>{body}</body></html>"""


# ============================================================
# Generate all mockups
# ============================================================
mockups = [
    ("mockup-a-hero-default.png", mockup_a(), 1280, 900),
    ("mockup-b-pipeline-active.png", mockup_b(), 1280, 1100),
    ("mockup-c-loading-scroll.png", mockup_c(), 1280, 1000),
    ("mockup-d-agents-detail.png", mockup_d(), 1280, 1200),
    ("mockup-e-completion-footer.png", mockup_e(), 1280, 800),
    ("mockup-f-mobile-layout.png", mockup_f(), 390, 844),
    ("mockup-g-error-fallback.png", mockup_g(), 800, 700),
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/usr/local/bin/chromium",
        args=["--no-sandbox", "--disable-setuid-sandbox"],
    )
    for filename, html, width, height in mockups:
        page = browser.new_page()
        page.set_viewport_size({"width": width, "height": height})
        page.set_content(html, wait_until="networkidle")
        page.wait_for_timeout(1200)  # wait for fonts
        out_path = os.path.join(OUT_DIR, filename)
        page.screenshot(path=out_path, full_page=True)
        print(f"  ✓ {filename} ({width}x{height})")
        page.close()
    browser.close()

print("\nAll 7 mockups generated.")
