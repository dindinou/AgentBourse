# AgentBourse

Un agent qui investit en bourse, construit pas à pas par un débutant.

> ⚠️ Projet d'apprentissage. Il fonctionne en **argent fictif** (paper trading) par défaut. Ce n'est pas un conseil en investissement.

## Analyseur halal

Tape le nom d'une action, même mal écrit. Le programme propose les actions qui ressemblent, tu choisis, puis il dit à quel point elle est conforme selon 5 normes (stricte, AAOIFI, S&P Shariah, MSCI Islamic, Malaisie), avec une légende et la part de dividende à purifier.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python analyser.py "apple"
```

Tests (sans internet) : `.venv/Scripts/python -m pytest`

> ⚠️ Outil de tri, pas une fatwa. Chiffres de Yahoo Finance, parfois faux ou anciens.
