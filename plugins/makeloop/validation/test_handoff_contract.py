"""Handoff wiring and authored rendering regressions; no LLM or host is launched.

The source assertions guard integration points, not semantic equivalence of arbitrary prose.
Rendered fixtures exercise the real template and existing output checker. They are NOT blind
model generation, independent review, or proof of native pause/stop behavior.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import unittest

from check_outputs import check, input_errors

ROOT = Path(os.environ.get('MAKELOOP_TEST_ROOT', Path(__file__).resolve().parents[1]))
COMMAND = (ROOT / 'commands/makeloop.md').read_text()
TEMPLATE = (ROOT / 'templates/loop-prompt.tmpl.md').read_text()
GUIDE = (ROOT / 'references/output-guide.md').read_text()


def section(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]


CLOSED = section(TEMPLATE, '# ============ CLOSED CORE', '# ============ OPEN CORE')
OPEN = section(TEMPLATE, '# ============ OPEN CORE', '# ============ OPTIONAL blocks')
HANDOFF = next(b for b in TEMPLATE.split('\n## ') if '] Morning handoff' in b)
NORMAL = re.sub(r'\s+', ' ', HANDOFF)
STATE_PATH = '.loop/repair-state.md'
CONTRACT_PATH = '.loop/repair.md'


def rendered_output(host, *, handoff=True, existing=None, done_ledger=False):
    """Author a bounded fixture from the actual CLOSED scaffold; never run its contents."""
    contract = CLOSED.split('\n# LOOP:', 1)[1]
    contract = '# LOOP:' + contract
    values = {
        '<short goal name>': 'Repair auth',
        '<one sentence, objective, checkable>': 'Repair the auth behavior within src/auth',
        '<runbook path if one exists>': '',
        '<verifiable criterion 1>': 'Existing auth behavior checks pass.',
        '<criterion 2>': 'The required independent human review passes.',
        '<criterion 3 — include any hard invariant from profile D>': 'No edits outside src/auth.',
        '<each criterion -> check, intended target/input, observation-validity condition,\npass rule, evidence location and invalidation; include required review/delivery>':
            'C1: npm test, collected auth suite, current target, exit 0, .loop/auth-test.log; '
            'C2: human review receipt on that target; C3: inspected diff. Relevant changes invalidate proof.',
        '<project-specific observable improvement or evidence that rules out a suspected cause>':
            'A failing auth case is fixed or a tested cause is eliminated, with current evidence.',
        '<verify command 1, e.g. npm run typecheck>': 'npm test',
        '<verify command 2, e.g. npm test>': 'git diff --check',
        '<exact pass condition, e.g. all tests green, 0 type errors, exit 0>':
            'All original criteria including the independent human review have current proof',
        '<completion token>': 'FINAL',
        '<N>': '8',
        '<off-limits from profile D>': 'Do not edit files outside src/auth except bound loop state.',
    }
    for key, value in values.items():
        contract = contract.replace(key, value)
    contract = contract.replace('.loop/state.md', STATE_PATH)
    if handoff:
        # This assembly models the Step 3 delivery mapping; source tests separately guard that rule.
        contract = contract.replace('EVIDENCE MAP:',
            '- C-HANDOFF: The receiving summary is saved and read back against current evidence.\n\nEVIDENCE MAP:', 1)
        contract = contract.replace('PROGRESS:',
            'C-HANDOFF: read back ' + STATE_PATH + ' section MORNING HANDOFF; compare current run, '
            'target, results and artifact pointers.\nPROGRESS:', 1)
        block = '## ' + HANDOFF
        block = block.replace('<exact state path and existing summary section/field>',
                              STATE_PATH + ' section MORNING HANDOFF')
        block = block.replace('<bound handoff criterion ID in SUCCESS CRITERIA and EVIDENCE MAP>',
                              'C-HANDOFF')
        contract += '\n' + block
    contract = contract.strip() + '\n'
    state = existing if existing is not None else '# Repair state\nStatus: not started\nIterations used: 0\n'
    files = {CONTRACT_PATH: contract, STATE_PATH: state, '.loop/INDEX.md':
             'repair | closed | npm test | cap 8 | manual | ' + STATE_PATH + '\n'}
    if done_ledger:
        files['.loop/done.json'] = '[{"criterion":"C1","status":"fail","verified_by":null}]\n'
    host_label = 'Claude Code' if host == 'claude' else 'Codex CLI'
    receipt = ('Morning handoff: execution will maintain ' + STATE_PATH + ' section MORNING HANDOFF.\n'
               if handoff else '')
    brief = ('Loop brief: repair auth and preserve the required review.\n'
             'How it stops: success, pending user pause, or the cumulative 8-attempt limit; '
             'one owner only.\n' + receipt +
             ('Codex run options: A — one manual iteration.\n' if host == 'codex' else
              'Run options: A — one manual iteration.\n') +
             'Generated, not configured, not started. No review is claimed performed.\n')
    chat = (brief + '\n```markdown\n' + contract + '```\n\n## Launch commands\n'
            '### A — Recommended: one iteration | ' + host_label + ' input\n```text\n'
            'Follow ' + CONTRACT_PATH + ' for exactly one iteration. Read and preserve ' +
            STATE_PATH + '; keep all saved limits and pending pauses; return after one iteration.\n```')
    out = {'id': 'handoff-' + host, 'files': files, 'chat': chat, 'progress': []}
    case = {'id': out['id'], 'kind': 'closed', 'host': host, 'gate': 'npm test'}
    if existing is not None:
        case['preserve'] = {STATE_PATH: existing}
    return case, out


class HandoffWiringTests(unittest.TestCase):
    def test_delivery_mapped_before_assembly(self):
        step3 = section(COMMAND, '## Step 3', '## Step 4')
        for phrase in ('C-HANDOFF', 'SUCCESS CRITERIA', 'EVIDENCE MAP', 'saved, read back'):
            self.assertIn(phrase, step3)
        self.assertNotIn('only when explicitly requested as an acceptance criterion', COMMAND)

    def test_kind_selection_and_opt_out(self):
        self.assertIn('Morning handoff | ✅ | ❌', COMMAND)
        self.assertIn('honor an explicit opt-out', COMMAND)
        self.assertIn('narrow refine adds', COMMAND)
        self.assertNotIn('Morning handoff', OPEN)

    def test_location_preserves_structured_state(self):
        for phrase in ('never prepend Markdown to JSON', 'existing supported summary',
                       'storage gap before offering an executable run'):
            self.assertIn(phrase, COMMAND)
        self.assertIn('HANDOFF LOCATION:', HANDOFF)

    def test_generation_does_not_rewrite_progress(self):
        self.assertIn('Generation preserves existing state bytes', COMMAND)
        self.assertIn('new state is marked not started', COMMAND)

    def test_current_run_before_new_work(self):
        self.assertIn('before new project work', NORMAL)
        self.assertIn('previous run\'s success is not current delivery', NORMAL)
        self.assertIn('run/attempt', NORMAL)
        self.assertIn('uncommitted changes', NORMAL)

    def test_readback_checks_evidence_not_only_existence(self):
        for phrase in ('save then read back', 'against current ledger/evidence',
                       'resolve the cited local artifacts', 'stale, unreadable'):
            self.assertIn(phrase, NORMAL)

    def test_no_change_is_still_delivered_without_retesting(self):
        self.assertIn('already green or no changes', NORMAL)
        self.assertIn('reuse valid tests rather than rerunning', NORMAL)
        self.assertIn('quiet escalation rule does not suppress', NORMAL)

    def test_controlled_exits_and_crash_are_distinct(self):
        self.assertIn('success, pause, budget, failure or cancellation', NORMAL)
        self.assertIn('crash can leave only the last durable checkpoint', NORMAL)
        self.assertIn('no invented final timestamp', NORMAL)

    def test_limits_and_pending_pause_survive(self):
        for phrase in ('do not restart tests, reviews or project work', 'within existing limits',
                       'without releasing a pause or resetting limits', 'endless report retry'):
            self.assertIn(phrase, NORMAL)

    def test_failed_delivery_prevents_false_completion(self):
        self.assertIn('never emit FINAL while required delivery is unproved', NORMAL)
        self.assertIn('Preserve original unmet criteria even if the summary is ready', NORMAL)
        self.assertIn('last confirmed saved checkpoint', NORMAL)

    def test_no_extra_authority_or_native_stop_claim(self):
        self.assertIn('commit/push/upload or schedule is authorized', NORMAL)
        self.assertIn('native stop requested/confirmed/unknown', NORMAL)
        self.assertIn('Do not put secrets', NORMAL)

    def test_receiver_is_described_before_launch_group(self):
        self.assertIn('Morning handoff / 翌朝の受け取り', GUIDE)
        self.assertIn('exact\n   state path/section', GUIDE)
        self.assertLess(GUIDE.index('Morning handoff / 翌朝の受け取り'),
                        GUIDE.index('5. **Launch commands'))
        self.assertIn('Nothing follows', COMMAND)

    def test_existing_cores_are_unchanged(self):
        self.assertEqual(hashlib.sha256(CLOSED.encode()).hexdigest(), 'a5122a1423cbe7c853d3917fc9b7331ad55d2211b5b3a30e84a964cc0bea5766')
        self.assertEqual(hashlib.sha256(OPEN.encode()).hexdigest(), '463715cefb054fd7631cfb61fe9f1a596ceee3ce2411f91441755949fa90e2b3')


class HandoffRenderingTests(unittest.TestCase):
    def test_bound_rendering_passes_existing_checker_on_both_hosts(self):
        for host in ('claude', 'codex'):
            with self.subTest(host=host):
                case, out = rendered_output(host)
                contract = out['files'][CONTRACT_PATH]
                self.assertEqual(check(case, out), [])
                self.assertNotRegex(contract, r'<[^>]+>')
                self.assertIn('DELIVERY CRITERION: C-HANDOFF', contract)
                self.assertEqual(set(out['files']), {CONTRACT_PATH, STATE_PATH, '.loop/INDEX.md'})

    def test_existing_state_preserved_during_generation(self):
        state = ('---\nowner: current-run\n---\n# Existing state\nIterations used: 7\n'
                 'Deadline: 2026-10-22T06:00:00+09:00\nPause: pending\n'
                 'Pending effect: receipt unknown\n## History\nDo not erase.\n')
        for host in ('claude', 'codex'):
            with self.subTest(host=host):
                case, out = rendered_output(host, existing=state)
                self.assertEqual(check(case, out), [])
                self.assertEqual(out['files'][STATE_PATH], state)

    def test_rendered_files_survive_save_and_readback(self):
        state = '# Existing state\nIterations used: 7\nPause: pending\n'
        for host in ('claude', 'codex'):
            with self.subTest(host=host), tempfile.TemporaryDirectory() as directory:
                case, out = rendered_output(host, existing=state, done_ledger=True)
                root = Path(directory)
                for path, content in out['files'].items():
                    target = root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(content, encoding='utf-8')
                saved = {path: (root / path).read_text(encoding='utf-8')
                         for path in out['files']}
                self.assertEqual(saved, out['files'])
                self.assertEqual(check(case, dict(out, files=saved)), [])
                self.assertEqual(saved[STATE_PATH], state)

    def test_json_done_ledger_is_not_rewritten_as_markdown(self):
        case, out = rendered_output('codex', done_ledger=True)
        self.assertEqual(check(case, out), [])
        self.assertEqual(json.loads(out['files']['.loop/done.json'])[0]['status'], 'fail')
        self.assertIn(STATE_PATH, out['files'][CONTRACT_PATH])

    def test_unselected_block_is_absent(self):
        for host in ('claude', 'codex'):
            with self.subTest(host=host):
                case, out = rendered_output(host, handoff=False)
                self.assertEqual(check(case, out), [])
                self.assertNotIn('C-HANDOFF', out['files'][CONTRACT_PATH])
                self.assertNotIn('HANDOFF LOCATION', out['files'][CONTRACT_PATH])

    def test_semantic_scenario_inputs_are_well_formed(self):
        path = Path(__file__).with_name('handoff-scenarios.json')
        cases = json.loads(path.read_text())
        self.assertEqual(input_errors(cases, []), [])
        self.assertTrue(all(c.get('review') for c in cases))


if __name__ == '__main__':
    unittest.main()
