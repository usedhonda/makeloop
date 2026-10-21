"""Regression tests for the checker input boundary; no model or launch execution."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_outputs import check, input_errors


CHECKER = Path(__file__).with_name('check_outputs.py')


def sample(kind='closed', host='codex'):
    case = {'id': 'example', 'kind': kind, 'host': host}
    prompt_path = '.loop/example.md'
    if kind == 'closed':
        contract = ('GOAL: repair the parser\nSUCCESS CRITERIA: accepted examples pass\n'
                    'VERIFY: python3 -m unittest\n'
                    'If already satisfied, report FINAL without a change.')
        state_path = '.loop/example-state.md'
        state = '# State\nNo work yet.'
    else:
        contract = ('WATCH TARGET: app.log\nTRIGGER CONDITION: new ERROR lines\n'
                    'RUN MODE: until cancelled\n'
                    'COLD START: existing backlog is already seen.')
        state_path = '.loop/example.cursor.json'
        state = json.dumps({'last_seen': None, 'last_fired_digest': None})
    launch = f'Follow {prompt_path} once; preserve and update {state_path}.'
    destination = 'Claude Code input' if host == 'claude' else 'Codex CLI input'
    chat = ('Loop brief: repair or watch the selected target.\n'
            'Codex run options: one manual tick.\n\n```markdown\n' + contract +
            '\n```\n\n## Launch commands\n\n### A — Recommended: one tick | ' + destination +
            '\n```text\n' + launch + '\n```')
    return case, {'id': case['id'], 'files': {prompt_path: contract, state_path: state},
                  'chat': chat}


class ArtifactInputTests(unittest.TestCase):
    def test_known_host_and_kind_still_accept_valid_artifacts(self):
        for host in ('claude', 'codex'):
            for kind in ('closed', 'open'):
                with self.subTest(host=host, kind=kind):
                    self.assertEqual(check(*sample(kind, host)), [])

    def test_unknown_kind_cannot_be_graded_as_a_watcher(self):
        case, out = sample('open')
        case['kind'] = 'opne'
        self.assertIn('unsupported scenario kind', check(case, out))

    def test_unknown_host_cannot_skip_host_specific_checks(self):
        case, out = sample()
        case['host'] = 'codxe'
        out['chat'] = out['chat'].replace('Follow .loop/', '/loop .loop/')
        self.assertIn('unsupported scenario host', check(case, out))

    def test_cursor_array_cannot_impersonate_required_object_keys(self):
        case, out = sample('open')
        out['files']['.loop/example.cursor.json'] = '["last_seen", "last_fired_digest"]'
        self.assertIn('cursor must be an object with required keys', check(case, out))

    def test_malformed_artifacts_report_errors_instead_of_crashing(self):
        for field, value in (('files', []), ('files', {'a': 1}), ('chat', {})):
            with self.subTest(field=field, value=value):
                case, out = sample()
                out[field] = value
                self.assertTrue(check(case, out))

    def test_blank_choice_is_not_a_response(self):
        case = {'kind': 'choice', 'host': 'codex'}
        self.assertIn('missing chat output', check(case, {'files': {}, 'chat': ' \n '}))

    def test_current_scenario_suite_satisfies_input_contract(self):
        cases = json.loads(CHECKER.with_name('scenarios.json').read_text())
        self.assertEqual(input_errors(cases, []), [])

    def test_operational_urls_are_not_source_citations(self):
        for kind in ('closed', 'open'):
            with self.subTest(kind=kind):
                case, out = sample(kind)
                path = '.loop/example.md'
                original = out['files'][path]
                if kind == 'closed':
                    case['gate'] = 'curl --fail https://example.com/health'
                    contract = original.replace('python3 -m unittest', case['gate'])
                    state_path = '.loop/example-state.md'
                    out['files'][state_path] += '\nEvidence: https://example.com/runs/42'
                else:
                    contract = original.replace('app.log', 'https://example.com/status')
                out['files'][path] = contract
                out['chat'] = out['chat'].replace(original, contract)
                self.assertEqual(check(case, out), [])

    def test_explicit_source_citations_are_rejected(self):
        for citation in ('Source: https://example.com/article',
                         '## Sources\n- [Article](https://example.com/article)',
                         '出典：https://example.com/article'):
            with self.subTest(citation=citation):
                case, out = sample()
                path = '.loop/example.md'
                original = out['files'][path]
                out['files'][path] += '\n' + citation
                out['chat'] = out['chat'].replace(original, out['files'][path])
                self.assertIn('source citation in generated files', check(case, out))

    def test_declared_learning_ledger_is_not_a_second_contract(self):
        for kind in ('closed', 'open'):
            with self.subTest(kind=kind):
                case, out = sample(kind)
                path = '.loop/example.md'
                original = out['files'][path]
                out['files'][path] += '\nLEARNINGS FILE: .loop/example-learnings.md'
                out['chat'] = out['chat'].replace(original, out['files'][path])
                out['files']['.loop/example-learnings.md'] = (
                    '# Learnings\n## DURABLE\nNone.\n## UNVERIFIED\nNone.')
                self.assertEqual(check(case, out), [])

    def test_learning_declaration_cannot_hide_another_contract(self):
        for kind in ('closed', 'open'):
            with self.subTest(kind=kind):
                case, out = sample()
                out['files']['.loop/example.md'] += (
                    '\nLEARNINGS FILE: .loop/example-learnings.md')
                out['files']['.loop/example-learnings.md'] = (
                    sample(kind)[1]['files']['.loop/example.md'])
                self.assertIn('must save exactly one contract', check(case, out))

    def test_undeclared_markdown_is_not_silently_ignored(self):
        case, out = sample()
        out['files']['.loop/example-learnings.md'] = '# Undeclared file'
        self.assertIn('must save exactly one contract', check(case, out))

    def test_learning_declaration_cannot_hide_heading_only_contract(self):
        for kind, label in (('closed', 'GOAL'), ('open', 'WATCH TARGET')):
            with self.subTest(kind=kind):
                case, out = sample()
                out['files']['.loop/example.md'] += (
                    '\nLEARNINGS FILE: .loop/example-learnings.md')
                hidden = sample(kind)[1]['files']['.loop/example.md']
                out['files']['.loop/example-learnings.md'] = hidden.replace(
                    label + ':', '## ' + label + '\n')
                self.assertIn('must save exactly one contract', check(case, out))


class CheckerCliTests(unittest.TestCase):
    def run_checker(self, cases, outputs, *flags):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scenarios = root / 'cases.json'
            artifacts = root / 'outputs.json'
            scenarios.write_text(json.dumps(cases))
            artifacts.write_text(json.dumps(outputs))
            return subprocess.run(
                [sys.executable, str(CHECKER), str(scenarios), str(artifacts), *flags],
                capture_output=True, text=True, check=False)

    def test_valid_complete_batch_passes(self):
        case, out = sample()
        for flags in ((), ('--contracts-only',)):
            with self.subTest(flags=flags):
                result = self.run_checker([case], [out], *flags)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('example: PASS', result.stdout)

    def test_duplicate_output_cannot_hide_a_failed_artifact(self):
        case, valid = sample()
        invalid = {'id': case['id'], 'files': {}, 'chat': ''}
        for outputs in ([invalid, valid], [valid, invalid]):
            with self.subTest(last_is_valid=outputs[-1] is valid):
                result = self.run_checker([case], outputs)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('duplicate scenario id', result.stderr)
                self.assertNotIn('PASS', result.stdout)

    def test_duplicate_expected_ids_reject_the_whole_batch(self):
        case, out = sample()
        result = self.run_checker([case, copy.deepcopy(case)], [out])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('duplicate scenario id', result.stderr)
        self.assertNotIn('PASS', result.stdout)

    def test_empty_suite_cannot_report_success(self):
        result = self.run_checker([], [])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('scenarios must not be empty', result.stderr)

    def test_domain_errors_reject_before_any_pass_verdict(self):
        case, out = sample('open')
        for field, value in (('kind', 'opne'), ('host', 'codxe'), ('id', ''),
                             ('acts', 'false'), ('gate', 123)):
            with self.subTest(field=field):
                malformed = dict(case, **{field: value})
                result = self.run_checker([case, dict(malformed, id='bad')]
                                          if field != 'id' else [malformed], [out])
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('PASS', result.stdout)

    def test_missing_and_unexpected_outputs_remain_failures(self):
        case, out = sample()
        unexpected = dict(out, id='unrequested')
        for outputs in ([], [out, unexpected]):
            with self.subTest(outputs=outputs):
                result = self.run_checker([case], outputs)
                self.assertNotEqual(result.returncode, 0)

    def test_non_array_batch_and_non_object_rows_fail_cleanly(self):
        case, out = sample()
        for cases, outputs in (({}, [out]), ([case], {}), ([None], [out]),
                               ([case], [None])):
            with self.subTest(cases=cases, outputs=outputs):
                result = self.run_checker(cases, outputs)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('error:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
