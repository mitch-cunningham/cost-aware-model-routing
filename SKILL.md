---
name: cost-aware-model-routing
description: Choose and configure the lowest-cost available model tier capable of an agent task, especially automatic reviews, memory maintenance, summaries, and background work. Use across Claude/Anthropic, GPT/OpenAI, Grok/xAI, Nous, proxies, and other providers without hard-coded model IDs. Audit routes, avoid expensive fallback, and preserve main models unless a main-model change is explicitly requested.
license: MIT
metadata:
  compatibility: Any agent with model-catalog and configuration access. Hosted agents without routing controls receive a recommendation, not a claimed configuration change. The optional offline selector requires Python 3.10+.
  version: "1.0.0"
  author: Mitch Cunningham
---

# Cost-Aware Model Routing

Use the lowest available tier that can reliably do the job. Let the host agent
resolve the actual model from its live provider catalog and task requirements;
never assume a historical name, branding label, or a provider's absolute smallest
model is appropriate. A skill cannot switch its own underlying model unless its
host exposes a routing/configuration interface.

## 1. Establish the task and authorized scope

Identify what is being routed: background review, extraction, summary, tool work,
vision, or main conversation. For background work, change only the auxiliary route;
keep the primary agent's model unchanged. Change a main/default model only when
that is explicitly requested. Preserve credentials, subscriptions, existing budgets,
runaway protection, schedules, and data-handling rules.

Infer routine choices from the user's request. Ask only for a missing decision that
would change spend, data destination, authorization, or critical task quality.

## 2. Discover actual choices

Read the installed framework's documentation/configuration and the authenticated
provider's live model list. An endpoint, subscription, and API plan can expose
different models even for the same vendor. Static catalogs are hints, not proof of
account access. Verify credentials without printing them or moving them to another
endpoint. Identify the actual execution path, including desktop backends and workers.

Use [provider-neutral discovery guidance](references/providers.md). Try the user's
current provider, account, and plan first. Do not silently switch subscriptions,
create a paid API account, or route data to another provider to obtain a cheaper model.

## 3. Select the lowest capable tier

Build a short candidate list from available, authenticated models. Filter by context
size (system prompt, tools, input and expected output), required tool calling,
structured output, modalities, latency, data restrictions, and task quality.

Rank eligible choices using current account-specific pricing, quota multipliers,
or a provider-verified tier order. Compare like billing units on the same plan.
Consider whole-task cost: repeated weak-model retries, cold context, caching, and
reasoning can outweigh a nominally cheaper model. Use a compact digest for reviews
when safe, preserving facts, decisions, unresolved work, and tool observations.

Where prices or subscription accounting are opaque, pick a verified lower tier
when possible and label savings unmeasured. Do not invent percentages or translate
API token prices into subscription credits. If tier order cannot be verified,
recommend candidates and state uncertainty instead of asserting a cheapest route.
If no lower capable model exists, keep the current model and report that outcome.

The optional [offline selector](scripts/choose_model.py) can apply an agent-supplied,
verified tier order and capability filter. It does not fetch catalogs, verify their
truth, mutate settings, or estimate bills. See [its input example](examples/catalog.json).

## 4. Apply a narrow route

Back up the relevant settings. Use the framework's native per-task/auxiliary model
route when available. Keep the foreground route intact for a background-only change.
Verify the provider runtime actually resolves to the requested model; a config key
alone is not proof. Reload every process that caches clients or configuration.

If the host does not support separate routing, state that limitation and leave the
main model unchanged. Offer a documented dedicated worker as a recommendation;
do not invent a host API or claim a prompt changed the runtime. If another provider
would be required, request authorization before moving work or adding billing.

## 5. Prevent expensive fallback and review loops

A missing/unavailable selected model must not silently fall back to an expensive
primary model, another provider, or a paid API. For unattended auxiliary work, skip
that auxiliary run and report the reason once; foreground work keeps functioning.
A bounded escalation to a stronger model is allowed only under the user's existing
fallback policy or explicit authorization. Share job accounting across attempts;
never reset counters or switch models to evade a stopped job.

Preserve the host's runaway protections. Reviews cannot launch reviews, and the same
conversation snapshot should not be automatically reviewed repeatedly. See the
[companion runaway protection skill](https://github.com/mitch-cunningham/runaway-agent-protection).
No new human-only admission gate or global daily cap is needed for routing.

## 6. Validate before claiming success

Use offline fixtures first. If authorized and needed, run a small bounded canary
with side-effecting tools and memory writes disabled. Where tool calling is required,
use a bounded mock or read-only tool to verify it. Confirm actual provider/model at dispatch,
required capabilities and output quality, primary route unchanged, safe failure
behavior, and continued normal schedules/memory/collaboration. Keep rejected or
failed canaries bounded; do not repeatedly retry an unsupported model.

For the final report use at most five bullets: scope, chosen route and rationale,
validation, measured/unknown savings, and limitations/rollback. Explicitly separate
configured, runtime-verified, and recommendation-only results. See
[the rollout checklist](references/rollout.md).
