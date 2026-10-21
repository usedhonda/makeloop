#!/usr/bin/env python3
"""Check generated loop artifacts, never execute their launch commands.

Usage: python3 check_outputs.py SCENARIOS.json OUTPUTS.json
Model generation and this deterministic checker are separate. This checks observable
artifact contracts; human semantic grading of suitability and safety is still required.
Optional outputs[].progress contains collected pre-final messages. If omitted, earlier
turns are not inspected; this checker cannot establish live host availability or behavior.
"""
import argparse
import json
import re
import shlex
from pathlib import Path


def case_errors(case):
    if not isinstance(case, dict):
        return ['scenario must be an object']
    errors = []
    if case.get('kind') not in ('closed', 'open', 'choice'):
        errors.append('unsupported scenario kind')
    if case.get('host') not in ('claude', 'codex'):
        errors.append('unsupported scenario host')
    if 'gate' in case and not isinstance(case['gate'], str):
        errors.append('gate must be a string')
    for flag in ('compare', 'bootstrap', 'stop_event', 'acts', 'show_body',
                 'execution_unconfigured'):
        if flag in case and not isinstance(case[flag], bool):
            errors.append(flag + ' must be a boolean')
    if 'preserve' in case and not text_files(case['preserve']):
        errors.append('preserve must map file paths to text')
    return errors


def text_files(value):
    return isinstance(value, dict) and all(
        isinstance(p, str) and isinstance(t, str) for p, t in value.items())


def output_errors(out):
    if not isinstance(out, dict):
        return ['output must be an object']
    errors = []
    if not text_files(out.get('files', {})):
        errors.append('files must map file paths to text')
    if not isinstance(out.get('chat', ''), str):
        errors.append('chat must be a string')
    progress = out.get('progress', [])
    if not isinstance(progress, list) or not all(isinstance(t, str) for t in progress):
        errors.append('progress must be an array of strings')
    return errors


def input_errors(cases, outputs):
    """Reject ambiguous or malformed batches before emitting any PASS verdict."""
    errors = []
    for label, rows, validate in (
            ('scenarios', cases, case_errors), ('outputs', outputs, output_errors)):
        if not isinstance(rows, list):
            errors.append(label + ' must be an array')
            continue
        if label == 'scenarios' and not rows:
            errors.append('scenarios must not be empty')
        seen = set()
        for index, row in enumerate(rows):
            prefix = f'{label}[{index}]: '
            errors.extend(prefix + error for error in validate(row))
            if not isinstance(row, dict):
                continue
            scenario_id = row.get('id')
            if not isinstance(scenario_id, str) or not scenario_id.strip():
                errors.append(prefix + 'id must be a nonempty string')
            elif scenario_id in seen:
                errors.append(prefix + 'duplicate scenario id: ' + scenario_id)
            else:
                seen.add(scenario_id)
    return errors


def has_source_citation(text):
    """Recognize explicit citation labels/sections, not operational URL values.

    Unlabelled provenance still requires the independent semantic review.
    """
    labels = r'sources?|references?|citations?|bibliography|出典|参考文献|参考資料'
    pattern = (r'^[ \t]*(?:#{1,6}[ \t]+)?(?:' + labels +
               r')[ \t]*(?:[:：][ \t]*(.*)|$)')
    for match in re.finditer(pattern, text, re.M | re.I):
        content = match.group(1) or ''
        if not content.strip():
            content = re.split(r'^#{1,6}[ \t]+', text[match.end():],
                               maxsplit=1, flags=re.M)[0]
        if re.search(r'https?://', content):
            return True
    return False



def fenced_blocks(text):
    """Read top-level matched fences; a longer outer fence protects nested examples."""
    return list(re.finditer(
        r'^(?P<marker>`{3,}|~{3,})(?P<lang>[^\n]*)\n'
        r'(?P<body>.*?)^(?P=marker)[ \t]*(?:\n|$)', text, re.M | re.S))


def has_launch_text(text):
    # Feature names alone are allowed; concrete saved-file launches are not.
    return bool(re.search(
        r'(?m)(?:^|`)[ \t]*(?:/(?:goal|loop|ralph-loop)\b|codex\s+exec\b|Follow\b)'
        r'[^\n`]*\.loop/', text) or re.search(
        r'(?m)(?:^|`)[ \t]*\.loop/[^\s`]+\.md[^\n`]*(?:に従|進め|実行)', text))


def copy_presentation_errors(case, chat, contract, blocks, launches):
    """Structural copy checks, not a host-capability or semantic safety verdict."""
    errors = []
    def require(ok, why):
        if not ok:
            errors.append(why)
    bodies = [b for b in blocks if b['lang'].strip() == 'markdown'
              and b['body'].rstrip('\n') == contract.rstrip('\n')]
    if case.get('show_body'):
        require(len(bodies) == 1 and bool(contract.strip()) and chat.count(contract.strip()) == 1,
                'show the saved contract once in a markdown fence')
    else:
        require(not bodies and contract.strip() not in chat, 'unrequested full Loop body')
    if bodies:
        require(all(f.start() > bodies[0].end() for f in launches),
                'launch appears before the complete final Loop body')
    require(len(blocks) == len(launches) + int(bool(case.get('show_body'))),
            'only the requested contract and final launch fences belong in the package')
    outside = chat
    for b in reversed(blocks):
        outside = outside[:b.start()] + '\n' + outside[b.end():]
    require(not re.search(r'(?m)^(?:`{3,}|~{3,})', outside), 'unclosed or malformed code fence')
    require(not has_launch_text(outside), 'launch outside the final copy blocks')
    require(len({f['body'].strip() for f in launches}) == len(launches), 'duplicate launch block')
    labels = []
    headings = list(re.finditer(r'(?m)^## [^\n]+', chat[:launches[0].start()])) if launches else []
    previous_end = headings[-1].start() if headings else 0
    for i, f in enumerate(launches):
        between = [line.strip() for line in chat[previous_end:f.start()].splitlines() if line.strip()]
        label = between[-1] if between else ''
        labels.append(label)
        require(len(between) == (2 if i == 0 else 1)
                and (i != 0 or between[0].startswith('## '))
                and bool(re.match(r'^### [A-Z]\s+[—|\-]', label)),
                'launch group must contain only heading, labels and blocks')
        expected_host = 'Claude Code' if case['host'] == 'claude' else 'Codex'
        other_host = 'Codex' if case['host'] == 'claude' else 'Claude Code'
        require(expected_host.lower() in label.lower() and other_host.lower() not in label.lower(),
                'launch label missing or mismatching host')
        destination = (r'input|chat|composer|入力欄|チャット' if f['lang'].strip() == 'text'
                       else r'terminal|shell|ターミナル|シェル')
        require(bool(re.search(destination, label, re.I)), 'launch label missing paste destination')
        require(label.startswith('### ' + chr(ord('A') + i) + ' '), 'launch labels must follow A/B/C order')
        previous_end = f.end()
    recommendations = [bool(re.search(r'\bRecommended\b|おすすめ|推奨', label, re.I)) for label in labels]
    if launches or not case.get('execution_unconfigured'):
        require(bool(recommendations) and recommendations[0] and sum(recommendations) == 1,
                'recommend exactly one launch, first')
    return errors


def check(case, out, presentation=True):
    errors = case_errors(case) + output_errors(out)
    if errors:
        return errors
    files = out.get('files', {})
    chat = out.get('chat', '')
    kind = case['kind']
    blocks = fenced_blocks(chat)
    launches = [b for b in blocks if b['lang'].strip() in ('text', 'sh')]
    for message in out.get('progress', []):
        if has_launch_text(message) or any(
                b['lang'].strip() != 'markdown' for b in fenced_blocks(message)) or any(
                text.strip() and text.strip() in message for path, text in files.items()
                if path.endswith('.md') and not path.endswith('-state.md') and path != '.loop/INDEX.md'):
            errors.append('launch or full contract leaked into progress')
    markdown_files = [(p, t) for p, t in files.items()
                      if p.startswith('.loop/') and p.endswith('.md')
                      and not p.endswith('-state.md') and p != '.loop/INDEX.md']
    # The optional recurring-loop block saves a declared learning ledger too.
    # Exclude that auxiliary file, but never let its name hide another contract.
    learning_files = {
        path for _, text in markdown_files
        for path in re.findall(r'^LEARNINGS FILE:\s*`?(\.loop/[^\s`]+\.md)`?', text, re.M)
    }
    contracts = [(p, t) for p, t in markdown_files
                 if p not in learning_files or
                 re.search(r'\b(?:GOAL|WATCH TARGET)\s*:|'
                           r'^\s*(?:#{1,6}\s+)?(?:GOAL|WATCH TARGET)\b', t, re.M)]
    def require(ok, why):
        if not ok:
            errors.append(why)
    require(bool(chat.strip()), 'missing chat output')
    if kind == 'choice':
        require(not files, 'unselected purpose created files')
        require(not blocks and not has_launch_text(chat), 'unselected purpose has runnable block')
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
    require(not any(has_source_citation(text) for text in files.values()),
            'source citation in generated files')
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
            require(isinstance(data, dict) and 'last_seen' in data and
                    'last_fired_digest' in data, 'cursor must be an object with required keys')
        except (ValueError, TypeError):
            errors.append('cursor is not valid JSON')
        require(bool(re.search(r'COLD START|cold.start|初回', contract, re.I)), 'missing cold-start policy section')
        require(bool(re.search(r'backlog|pre.existing|existing|lines before.*cursor|historical|既存|過去', contract, re.I)), 'missing backlog policy')
    fences = launches
    if case.get('execution_unconfigured'):
        require(not fences and not has_launch_text(chat),
                'unconfigured execution has a runnable replacement')
    else:
        require(bool(fences), 'no runnable copy block')
    if fences:
        require(prompt_path in fences[0]['body'], 'first launch file/state mismatch')
        if presentation:
            require(not chat[fences[-1].end():].strip(), 'prose follows the last launch block')
    if presentation:
        errors.extend(copy_presentation_errors(case, chat, contract, blocks, fences))
    for fence in fences:
        code = fence['body'].strip()
        if fence['lang'].strip() == 'text':
            pairs = [('"', '"'), ("'", "'"), ('“', '”'), ('「', '」')]
            require(not any(code.startswith(a) and code.endswith(b) for a, b in pairs),
                    'display quotes in conversation block')
            require(not re.search(r'^(?:codex|claude|cd)\s+', code), 'shell command in conversation block')
            if re.search(r'(?m)^/(?:goal|loop|ralph-loop)\b', code):
                require('\n' not in code, 'slash launch must be one physical line')
        else:
            require(not re.search(r'^/(?:goal|loop|ralph-loop)\b', code), 'chat command in terminal block')
            try:
                words = shlex.split(code)
                require(not any('\n' in word or '\r' in word for word in words),
                        'newline inside quoted argument or identifier')
            except ValueError:
                errors.append('invalid shell quoting')
        require(not re.search(r'^\s*(?:\$ |[-*] |\d+\. |# )', code, re.M), 'copy block contains prompt/list/comment')
        require(not re.search(r'<[^\n>]+>', code), 'placeholder in launch')
        for path in (prompt_path, state_path):
            require(not (path not in code and path in code.replace('\n', '').replace('\r', '')),
                    'newline inside saved path')
        require(prompt_path in code, 'launch missing saved contract')
        mentioned_states = re.findall(r'\.loop/[^\s\'"`;]+(?:-state\.md|\.cursor\.json)', code)
        require((state_path in code or state_path in contract) and
                all(path == state_path for path in mentioned_states), 'launch missing exact state')
        if case['host'] == 'codex':
            require(not re.search(r'(?<![\w/])/(?:loop|ralph-loop)\b|codex-loop', code), 'Claude launch on Codex')
            require('--last' not in code, 'ambiguous unattended resume')
        else:
            require(not re.search(r'\bcodex\s+(?:exec|resume)\b|codex-loop', code),
                    'Codex launch on Claude Code')
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenarios', type=Path)
    parser.add_argument('outputs', type=Path)
    parser.add_argument('--contracts-only', action='store_true')
    args = parser.parse_args()
    try:
        cases = json.loads(args.scenarios.read_text())
        raw = args.outputs.read_text().strip()
        if raw.startswith('```'):
            raw = re.sub(r'^```(?:json)?\s*\n|\n```$', '', raw)
        outputs = json.loads(raw)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    errors = input_errors(cases, outputs)
    if errors:
        parser.error('; '.join(errors))
    by_id = {row['id']: row for row in outputs}
    contracts_only = args.contracts_only
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
