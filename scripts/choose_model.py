"""Offline selection from agent-verified within-plan tiers; no model/network calls."""
from __future__ import annotations
import json, math, sys

def select(data: dict) -> dict:
    current = data['current']
    task = data['task']
    keep = {'provider':current['provider'], 'model':current['model']}
    def unchanged(status, reason):
        return {'status':status, 'route':keep, 'reason':reason, 'applied':False, 'savings':'unmeasured'}
    if task.get('scope', 'background') not in ('background', 'foreground'):
        raise ValueError('scope must be background or foreground')
    if task.get('scope') == 'foreground' and task.get('foreground_change_authorized') is not True:
        return unchanged('unchanged', 'A foreground model change is not authorized.')
    if task.get('host_supports_route') is not True:
        return unchanged('unsupported', 'Host routing is unavailable or unverified; recommendation only.')
    required_context = task.get('required_context_tokens', 0)
    if isinstance(required_context, bool) or not isinstance(required_context, int) or required_context < 0:
        raise ValueError('required_context_tokens must be a nonnegative integer')
    required = task.get('required_capabilities', [])
    if not isinstance(required, list) or not all(isinstance(x, str) for x in required):
        raise ValueError('required_capabilities must be a list of strings')
    eligible = []
    for model in data['models']:
        # Same provider and billing account only. Cross-provider choices need an
        # explicitly authorized adapter, not an implicit decision by this helper.
        if model.get('provider') != current['provider'] or model.get('account') != current.get('account'):
            continue
        if model.get('available') is not True or model.get('authenticated') is not True:
            continue
        if model.get('rank_verified') is not True or not model.get('tier_source'):
            continue
        rank = model.get('rank')
        context = model.get('context_tokens')
        if isinstance(rank, bool) or not isinstance(rank, (int, float)) or not math.isfinite(rank) or rank < 0:
            continue
        if isinstance(context, bool) or not isinstance(context, int) or context < required_context:
            continue
        capabilities = model.get('capabilities')
        if not isinstance(capabilities, list) or not set(required).issubset(capabilities):
            continue
        if not isinstance(model.get('model'), str) or not model['model']:
            continue
        eligible.append(model)
    if not eligible:
        return unchanged('unverified', 'No available, authenticated, capable model has a verified within-plan tier rank.')
    selected = min(eligible, key=lambda m:(m['rank'], m['model'] != current['model'], m['model']))
    current_entry = next((m for m in eligible if m['model'] == current['model']), None)
    if selected['model'] == current['model']:
        return unchanged('unchanged', 'The current model is already the lowest verified capable tier.')
    # A claimed downgrade needs a verified comparison with the current model.
    if current_entry is None:
        return unchanged('unverified', 'Current model tier/capability is unverified; cannot establish a downgrade.')
    return {'status':'proposed', 'route':{'provider':selected['provider'], 'model':selected['model']},
            'reason':'Lowest verified available tier meeting the supplied context and capabilities.',
            'tier_source':selected['tier_source'], 'applied':False, 'savings':'unmeasured'}

if __name__ == '__main__':
    try:
        with open(sys.argv[1], encoding='utf-8') as handle:
            result = select(json.load(handle))
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        print(json.dumps({'status':'invalid_input', 'error':str(exc), 'applied':False}), file=sys.stderr)
        raise SystemExit(2)
