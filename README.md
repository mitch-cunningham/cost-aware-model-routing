# Cost-Aware Model Routing

A portable skill that asks an agent to discover its real model options and choose
**the lowest-cost tier capable of the task**. It is especially useful for automatic
reviews, summaries, memory maintenance, extraction, and routine background jobs.

It works as guidance across Claude, GPT, Grok, Nous, and other providers. There are
no built-in model names to go stale. The agent chooses from its account's available
models and verifies the route; it reports hosts that cannot route separately.

## Install and use

Copy this repository into the skill directory supported by your agent, under
`cost-aware-model-routing`, retaining `SKILL.md`, `references/`, and `scripts/`.
For a host using `.agents/skills/`:

```sh
git clone https://github.com/mitch-cunningham/cost-aware-model-routing.git \
  .agents/skills/cost-aware-model-routing
```

Other hosts may use `.claude/skills/`, `~/.hermes/skills/`, or a managed skill catalog.
Use the host's documented installation path.

Example request:

> Use cost-aware-model-routing for our automatic reviews. Choose the lowest tier
> available on each agent's existing provider that can handle the work. Keep the
> main models and current protections unchanged. Test the actual routes and tell
> me which hosts cannot support this.

Installing instructions does not grant API access or magically change a hosted
model. The agent needs authorized configuration access and a supported host route.

## What it does

- Discovers models available to the actual account and subscription.
- Checks context, tools, structured output, modality, latency, and task quality.
- Selects a capable lower tier without assuming “smallest” always means best value.
- Keeps background routing separate from main conversations where supported.
- Skips unavailable auxiliary routes instead of silently using an expensive fallback.
- Preserves existing budgets, schedules, memory, and runaway protection.

There is no guarantee that fewer tokens or a lower-tier label means a specific
subscription saving. Opaque billing is reported as unmeasured, never guessed.
Changing providers or introducing a paid API needs the user's authorization.

## Optional offline helper

Python 3.10+, no dependencies or network calls:

```sh
python scripts/choose_model.py examples/catalog.json
python -m unittest discover -s tests -v
```

The helper filters an agent-supplied catalog using verified **within-plan** tier
ranks and required capabilities. The example uses fictional model IDs, not live
recommendations. The helper proposes a route; only your host adapter can apply and
test it. The agent remains responsible for obtaining current, trustworthy inputs.

- [Skill](SKILL.md)
- [Provider discovery](references/providers.md)
- [Rollout and rollback](references/rollout.md)
- [Companion: Runaway Agent Protection](https://github.com/mitch-cunningham/runaway-agent-protection)

MIT licensed. See [LICENSE](LICENSE).
