#!/usr/bin/env python3
"""Check generated loop artifacts, never execute their launch commands.

Usage: python3 check_outputs.py SCENARIOS.json OUTPUTS.json
Model generation and this deterministic checker are separate. This checks observable
artifact contracts; human semantic grading of suitability and safety is still required.
"""
import json
import re
import sys
from pathlib import Path


def check(case, out, presentation=True):
    errors = []
    files = out.get('files', {})
    chat = out.get('chat', '')
    kind = case['kind']
    contracts = [(p, t) for p, t in files.items()
                 if p.startswith('.loop/') and p.endswith('.md')
                 and not p.endswith('-state.md') and p != '.loop/INDEX.md']
    def require(ok, why):
        if not ok:
            errors.append(why)
    require(bool(chat), 'missing chat output')
    if kind == 'choice':
        require(not files, 'unselected purpose created files')
        require(not re.search(r'```(?:text|sh)\s*\n', chat), 'unselected purpose has runnable block')
        if case.get('compare'):
            require(bool(re.search(r'closed|完了|修理', chat, re.I)) and
                    bool(re.search(r'open|監視|watch', chat, re.I)), 'purpose alternatives absent')
        return errors
    require(len(contracts) == 1, 'must save exactly one contract')
    if not contracts:
        return errors
    prompt_path, contract = contracts[0]
    body = '\n'.join(files.values())
    slug = prompt_path[:-3]
    state_path = slug + ('-state.md' if kind == 'closed' else '.cursor.json')
    require(state_path in files, 'missing matching state/cursor')
    # Safety-rule meaning is graded independently against the golden rubric, not
    # by forcing English labels onto valid Japanese or paraphrased contracts.
    require(not re.search(r'https?://', body), 'source citation in generated files')
    require(not re.search(r'<(?:slug|channel|event id|N|K|P|T|C|completion token|saved file)>', body, re.I),
            'unbound scaffold placeholder')
    if kind == 'closed':
        for term in ['GOAL', 'SUCCESS CRITERIA', 'VERIFY', 'FINAL']:
            require(term in contract, f'missing closed field: {term}')
        require('TRIGGER CONDITION' not in contract, 'open core leaked into closed')
        require('already' in contract.lower() or '既に' in contract or 'すでに' in contract,
                'missing first-VERIFY honesty')
        if case.get('gate'):
            require(case['gate'] in contract, 'explicit gate not preserved')
    else:
        for term in ['WATCH TARGET', 'TRIGGER CONDITION', 'RUN MODE']:
            require(term in contract, f'missing watcher field: {term}')
        positive_token_lines = [line for line in contract.splitlines() if 'FINAL' in line
                                and not re.search(r'no FINAL|never .*FINAL|not .*FINAL|FINAL.*not', line, re.I)]
        require(not positive_token_lines and not re.search(r'^SUCCESS CRITERIA', contract, re.M),
                'closed gate/token in watcher')
        cursor = files.get(state_path, '')
        try:
            data = json.loads(cursor)
            require('last_seen' in data and 'last_fired_digest' in data, 'cursor missing keys')
        except (ValueError, TypeError):
            errors.append('cursor is not valid JSON')
        require(bool(re.search(r'COLD START|cold.start|初回', contract, re.I)), 'missing cold-start policy section')
        require(bool(re.search(r'backlog|pre.existing|existing|lines before.*cursor|historical|既存|過去', contract, re.I)), 'missing backlog policy')
    fences = list(re.finditer(r'```(text|sh)\s*\n(.*?)\n```', chat, re.S))
    require(bool(fences), 'no runnable copy block')
    if fences:
        require(prompt_path in fences[0][2] and state_path in fences[0][2], 'first launch file/state mismatch')
        if presentation:
            body_start = chat.find(contract)
            require(body_start >= 0 and all(f.start() > body_start + len(contract) for f in fences),
                    'launch appears before the complete final Loop body')
            require(not chat[fences[-1].end():].strip(), 'prose follows the last launch block')
    for fence in fences:
        code = fence[2]
        require(not re.search(r'^\s*(?:\$ |[-*] |\d+\. |# )', code, re.M), 'copy block contains prompt/list/comment')
        require(not re.search(r'<[^\n>]+>', code), 'placeholder in launch')
        require(prompt_path in code, 'launch missing saved contract')
        require(state_path in code, 'launch missing exact state')
        if case['host'] == 'codex':
            require(not re.search(r'(?<![\w/])/(?:loop|ralph-loop)\b|codex-loop', code), 'Claude launch on Codex')
            require('--last' not in code, 'ambiguous unattended resume')
    require(bool(re.search(r'Loop brief|ループ概要', chat)), 'missing concrete Loop brief')
    if case['host'] == 'codex':
        require('Codex run options' in chat, 'missing Codex choices section')
    if case.get('lang') == 'ja':
        require(len(re.findall(r'[ぁ-んァ-ン一-龥]', body)) > 60, 'Japanese output not rendered')
    if case.get('bootstrap'):
        require(bool(re.search(r'ITERATION 0|iteration 0|反復0|反復 0', contract)), 'missing bootstrap')
        require(bool(re.search(r'\bred\b|actual failure|failing|赤', contract, re.I)), 'bootstrap has no failing gate')
    if case.get('stop_event'):
        require('TRIGGERED' in contract, 'stop-on-event sentinel missing')
    if case.get('acts'):
        require('Intent deny-list' in contract and 'Security tax' in contract, 'acting watcher missing safety')
        require('idempot' in contract.lower(), 'acting watcher missing idempotency')
        require('handoff' in contract.lower() or '引継' in contract, 'acting watcher missing handoff')
    if case['host'] == 'claude':
        for line in contract.splitlines():
            require(not (re.search(r'schedules? (?:are |is )?not restored', line, re.I)
                         and 'self-paced' not in line.lower()), 'self-paced resume limit generalized to all schedules')
    if case.get('preserve'):
        for p, original in case['preserve'].items():
            require(files.get(p) == original, 'existing state overwritten: ' + p)
    return errors


def main():
    cases = json.loads(Path(sys.argv[1]).read_text())
    raw = Path(sys.argv[2]).read_text().strip()
    if raw.startswith('```'):
        raw = re.sub(r'^```(?:json)?\s*\n|\n```$', '', raw)
    outputs = json.loads(raw)
    by_id = {row['id']: row for row in outputs}
    contracts_only = '--contracts-only' in sys.argv[3:]
    if contracts_only:
        print('Contract/content checks only; final-only presentation is not graded.')
    failures = 0
    for case in cases:
        errors = check(case, by_id.get(case['id'], {}), presentation=not contracts_only)
        print(f"{case['id']}: " + ('FAIL: ' + '; '.join(errors) if errors else 'PASS'))
        failures += bool(errors)
    extra = set(by_id) - {c['id'] for c in cases}
    if extra:
        print('Unexpected scenarios: ' + ', '.join(sorted(extra)))
        failures += 1
    raise SystemExit(bool(failures))

if __name__ == '__main__':
    main()
