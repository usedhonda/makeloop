"""Copy-layout regression fixtures; no live agent, schedule or launch execution.

Run all checker tests: python3 -m unittest discover -s plugins/makeloop/validation -p 'test_*.py'
These authored fixtures check formatting, not independent model generation or pause behavior.
"""
import shlex
import unittest

from check_outputs import check
from test_check_outputs import sample


PROMPT = '.loop/example.md'
STATE = '.loop/example-state.md'


def package(host='codex', kind='closed', options=None):
    case, out = sample(kind, host)
    contract = out['files'][PROMPT]
    state = STATE if kind == 'closed' else '.loop/example.cursor.json'
    target = 'Codex CLI' if host == 'codex' else 'Claude Code'
    if options is None:
        options = [('text', f'Follow {PROMPT} for exactly one iteration; update {state}.',
                    f'A — Recommended: one iteration | {target} input')]
    out['chat'] = ('Loop brief: same accepted goal and limits; choose only one owner.\n'
                   'Codex run options: A is recommended; other modes are conditional.\n\n'
                   '```markdown\n' + contract + '\n```\n\n## Launch commands\n\n' +
                   '\n\n'.join(f'### {label}\n```{lang}\n{body}\n```'
                                for lang, body, label in options))
    return case, out


class CopyLayoutTests(unittest.TestCase):
    def test_two_host_specific_choices(self):
        for host in ('claude', 'codex'):
            with self.subTest(host=host):
                target = 'Claude Code' if host == 'claude' else 'Codex CLI'
                options = [
                    ('text', f'Follow {PROMPT} once; update {STATE}.',
                     f'A — Recommended: one iteration | {target} input'),
                    ('text', f'/goal Follow {PROMPT}; preserve {STATE} and its limits.',
                     f'B — Continue to the goal | {target} input')]
                self.assertEqual(check(*package(host, options=options)), [])

    def test_japanese_copy_labels(self):
        case, out = package()
        out['chat'] = out['chat'].replace('Launch commands', '起動コマンド').replace(
            'A — Recommended: one iteration | Codex CLI input',
            'A — おすすめ：まず1回 | Codex CLI 入力欄')
        self.assertEqual(check(case, out), [])

    def test_useful_single_option_is_valid(self):
        self.assertEqual(check(*package()), [])

    def test_duplicate_choices_are_rejected(self):
        case, out = package()
        block = out['chat'].split('### A')[1]
        out['chat'] += '\n\n### B' + block.replace('Recommended: ', '')
        self.assertIn('duplicate launch block', check(case, out))

    def test_labels_require_host_and_matching_destination(self):
        for label in ('A — Recommended: one iteration',
                      'A — Recommended | Claude Code input',
                      'A — Recommended | Codex CLI terminal'):
            with self.subTest(label=label):
                self.assertTrue(check(*package(options=[('text',
                    f'Follow {PROMPT}; update {STATE}.', label)])))

    def test_one_recommendation_must_be_first(self):
        for first, second in (('', ''), ('Recommended: ', 'Recommended: '),
                              ('', 'Recommended: ')):
            with self.subTest(first=first, second=second):
                options = [
                    ('text', f'Follow {PROMPT} once; update {STATE}.',
                     f'A — {first}one iteration | Codex CLI input'),
                    ('text', f'/goal Follow {PROMPT}; preserve {STATE}.',
                     f'B — {second}continue | Codex CLI input')]
                self.assertIn('recommend exactly one launch, first', check(*package(options=options)))

    def test_slash_launch_is_one_physical_line(self):
        for code in (f'/goal Follow {PROMPT};\nupdate {STATE}.',
                     f'/goal Follow {PROMPT}; update {STATE}.\n/goal pause'):
            with self.subTest(code=code):
                self.assertIn('slash launch must be one physical line', check(*package(
                    options=[('text', code, 'A — Recommended | Codex CLI input')])))

    def test_copy_payload_rejects_display_quotes_and_shell_wrapper(self):
        for code in (f'"Follow {PROMPT}; update {STATE}."',
                     f'「{PROMPT}に従い{STATE}を更新して」',
                     f'codex exec "Follow {PROMPT}; update {STATE}."'):
            with self.subTest(code=code):
                self.assertTrue(check(*package(options=[
                    ('text', code, 'A — Recommended | Codex CLI input')])))

    def test_shell_paste_is_distinct_and_quotes_are_preserved(self):
        prompt = f"Follow {PROMPT}; preserve {STATE} and the user's limits."
        cwd = "/tmp/user's project"
        command = f'cd {shlex.quote(cwd)} && codex exec resume session-42 {shlex.quote(prompt)}'
        case, out = package(options=[('sh', command,
                                     'A — Recommended: CI resume | Codex OS terminal')])
        self.assertEqual(check(case, out), [])
        self.assertEqual(shlex.split(command), ['cd', cwd, '&&', 'codex', 'exec',
                                               'resume', 'session-42', prompt])
        out['chat'] = out['chat'].replace(command, command + " '")
        self.assertIn('invalid shell quoting', check(case, out))

    def test_chat_slash_command_is_not_shell(self):
        self.assertIn('chat command in terminal block', check(*package(options=[
            ('sh', f'/goal Follow {PROMPT}; update {STATE}.',
             'A — Recommended | Codex OS terminal')])))

    def test_no_footer_or_extra_prose_between_copy_blocks(self):
        case, out = package()
        out['chat'] += '\nLet me know when done.'
        self.assertIn('prose follows the last launch block', check(case, out))
        case, out = package()
        out['chat'] = out['chat'].replace('### A', 'Extra instructions here.\n\n### A')
        self.assertIn('launch group must contain only heading, labels and blocks', check(case, out))

    def test_early_launch_and_missing_contract_fence_fail(self):
        case, out = package()
        out['chat'] = '```text\n/goal ' + PROMPT + ' ' + STATE + '\n```\n' + out['chat']
        self.assertIn('launch appears before the complete final Loop body', check(case, out))
        case, out = package()
        out['chat'] = out['chat'].replace('```markdown\n', '').replace('\n```\n\n## Launch', '\n\n## Launch', 1)
        self.assertIn('show the saved contract once in a markdown fence', check(case, out))

    def test_nested_contract_fences_are_not_launches(self):
        case, out = package()
        original = out['files'][PROMPT]
        contract = original + '\n\n```sh\npython3 -m unittest\n```'
        out['files'][PROMPT] = contract
        out['chat'] = out['chat'].replace('```markdown\n' + original + '\n```',
                                        '````markdown\n' + contract + '\n````')
        self.assertEqual(check(case, out), [])

    def test_raw_launch_in_explanation_is_rejected(self):
        case, out = package()
        out['chat'] = f'/goal Follow {PROMPT}; update {STATE}.\n' + out['chat']
        self.assertIn('launch outside the final copy blocks', check(case, out))

    def test_recorded_progress_must_not_leak_launches(self):
        case, out = package()
        out['progress'] = ['Checking the saved contract; /goal availability is not confirmed.']
        self.assertEqual(check(case, out), [])
        for message in (f'/goal Follow {PROMPT}; update {STATE}.',
                        f'```text\nFollow {PROMPT}; update {STATE}.\n```',
                        out['files'][PROMPT]):
            with self.subTest(message=message):
                out['progress'] = [message]
                self.assertIn('launch or full contract leaked into progress', check(case, out))

    def test_malformed_progress_is_rejected(self):
        case, out = package()
        out['progress'] = 'not a list of messages'
        self.assertIn('progress must be an array of strings', check(case, out))

    def test_choice_mode_cannot_hide_runnable_fences(self):
        for marker, lang in (('````', 'text'), ('~~~', 'sh'), ('```', 'bash')):
            with self.subTest(marker=marker, lang=lang):
                case = {'kind': 'choice', 'host': 'codex'}
                out = {'files': {}, 'chat': f'{marker}{lang}\n/goal {PROMPT}\n{marker}'}
                self.assertIn('unselected purpose has runnable block', check(case, out))

    def test_open_watcher_uses_its_cursor_for_every_choice(self):
        options = [
            ('text', 'Follow .loop/example.md for one tick; preserve .loop/example.cursor.json.',
             'A — Recommended: one tick | Claude Code input'),
            ('text', '/loop 5m Follow .loop/example.md for one tick; update .loop/example.cursor.json.',
             'B — Create a schedule | Claude Code input')]
        self.assertEqual(check(*package('claude', 'open', options)), [])
        options[1] = ('text', options[1][1].replace('example.cursor.json', 'other.cursor.json'), options[1][2])
        self.assertIn('launch missing exact state', check(*package('claude', 'open', options)))

    def test_foreign_host_commands_are_rejected_in_both_directions(self):
        for host, lang, code, label, error in (
            ('codex', 'text', f'/loop 5m Follow {PROMPT}; update {STATE}.',
             'A — Recommended | Codex CLI input', 'Claude launch on Codex'),
            ('claude', 'sh', f'codex exec resume session-42 "Follow {PROMPT}; update {STATE}."',
             'A — Recommended | Claude Code OS terminal', 'Codex launch on Claude Code')):
            with self.subTest(host=host):
                self.assertIn(error, check(*package(host, options=[(lang, code, label)])))

    def test_duplicate_contract_is_rejected(self):
        case, out = package()
        out['chat'] = out['files'][PROMPT] + '\n' + out['chat']
        self.assertIn('show the saved contract once in a markdown fence', check(case, out))

    def test_broken_fence_or_prose_then_slash_is_rejected(self):
        case, out = package()
        out['chat'] += '\n```text\naccidental extra block'
        self.assertIn('unclosed or malformed code fence', check(case, out))
        code = f'Follow {PROMPT}; update {STATE}.\n/goal pause'
        self.assertIn('slash launch must be one physical line', check(*package(options=[
            ('text', code, 'A — Recommended | Codex CLI input')])))

    def test_contracts_only_does_not_claim_presentation_checks(self):
        case, out = package()
        out['chat'] = out['chat'].replace('Codex CLI input', 'unknown place')
        self.assertTrue(check(case, out))
        self.assertEqual(check(case, out, presentation=False), [])


if __name__ == '__main__':
    unittest.main()
