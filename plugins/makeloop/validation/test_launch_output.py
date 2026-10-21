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
    def blocked_continuation(self):
        case, out = package()
        contract = ('GOAL: Finish all UI residual work, not just dependency diagnosis.\n'
                    'SUCCESS CRITERIA: C1 diagnose; C2 implement and apply; C3 consult and review.\n'
                    'VERIFY: retain all original checks; FINAL only with all proof.\n'
                    'If already satisfied, report honestly.\n'
                    'REQUESTED MODE: continuous completion; Goal blocked, resume unavailable.\n'
                    'BUDGET: 7/8 consumed, 1 remaining; no reset or increase.\n'
                    'AUTHORITY: src/ui edits approved; no other changes or external effects.\n'
                    'STATE FILE: .loop/example-state.md; reconcile same owner before resume.')
        state = 'Attempts used: 7\nCap: 8\nRemaining: 1\nGoal: blocked\n'
        out['files'][PROMPT], out['files'][STATE] = contract, state
        case.update(execution_unconfigured=True, preserve={PROMPT: contract, STATE: state})
        case.pop('show_body', None)
        out['chat'] = ('Loop brief: Finish every original UI criterion, consultation and review.\n'
                       'Codex run options: requested continuation is unconfigured; Goal cannot resume.\n'
                       '7/8 consumed, only one attempt remains; completion is not promised.\n'
                       'A single pass is a different unselected mode, not continuous completion.\n'
                       'Saved contract: .loop/example.md; state and authority preserved.')
        return case, out

    def test_blocked_continuation_preserves_contract_and_seven_of_eight(self):
        self.assertEqual(check(*self.blocked_continuation()), [])

    def test_blocked_continuation_cannot_be_replaced_by_a_runnable_tick(self):
        for launch in (f'{PROMPT} に従い1回進めて。', f'/goal Follow {PROMPT}.'):
            case, out = self.blocked_continuation()
            out['chat'] += ('\n## Launch commands\n### A — Recommended | Codex CLI input\n'
                            '```text\n' + launch + '\n```')
            self.assertIn('unconfigured execution has a runnable replacement', check(case, out))

    def test_blocked_continuation_cannot_reset_budget_or_drop_residual_work(self):
        for path, replacement in ((STATE, 'Attempts used: 0\nCap: 8\nRemaining: 8'),
                                   (PROMPT, 'GOAL: Only diagnose C1 for one iteration.')):
            case, out = self.blocked_continuation()
            out['files'][path] = replacement
            self.assertIn('existing state overwritten: ' + path, check(case, out))

    def test_exhausted_continuation_never_emits_command_then_unusable_caveat(self):
        case, out = self.blocked_continuation()
        for path in (PROMPT, STATE):
            text = out['files'][path].replace('7/8 consumed, 1 remaining', '8/8 consumed, 0 remaining')
            text = text.replace('Attempts used: 7', 'Attempts used: 8').replace('Remaining: 1', 'Remaining: 0')
            out['files'][path] = text
            case['preserve'][path] = text
        out['chat'] = ('Loop brief: Keep every UI residual requirement, consultation and review.\n'
                       'Codex run options: requested continuous completion is unconfigured.\n'
                       '8/8 consumed, 0 remaining; blocked Goal has no resume operation.\n'
                       'No executable launch for the requested mode has been generated.\n'
                       'Saved contract and current state preserved; no new project work or budget reset.')
        self.assertEqual(check(case, out), [])
        for candidate in (f'{PROMPT} に従い完遂まで継続して。',
                          f'/goal Follow {PROMPT} until complete.',
                          f'{PROMPT} に従い1回進めて。'):
            with self.subTest(candidate=candidate):
                bad = dict(out, chat=out['chat'] +
                    '\n## Launch commands\n### A — Recommended | Codex CLI input\n```text\n' +
                    candidate + '\n```\nBut this will not run until budget and resume are fixed.')
                self.assertIn('unconfigured execution has a runnable replacement', check(case, bad))

    def compact(self, host='codex', kind='closed'):
        code = f'{PROMPT} に従い1回進めて。'
        target = 'Claude Code' if host == 'claude' else 'Codex CLI'
        case, out = package(host, kind, [('text', code,
                                       f'A — Recommended: one tick | {target} input')])
        case.pop('show_body', None)  # Default: no full body requested.
        original = out['files'][PROMPT]
        state = STATE if kind == 'closed' else '.loop/example.cursor.json'
        field = 'STATE FILE' if kind == 'closed' else 'CURSOR FILE'
        out['files'][PROMPT] = original + f'\n{field}: {state}'
        out['chat'] = out['chat'].replace('```markdown\n' + original + '\n```',
                                        f'Saved contract: {PROMPT}')
        return case, out

    def test_compact_default_uses_saved_state_on_both_hosts_and_kinds(self):
        for host in ('claude', 'codex'):
            for kind in ('closed', 'open'):
                with self.subTest(host=host, kind=kind):
                    self.assertEqual(check(*self.compact(host, kind)), [])

    def test_compact_requires_state_binding_not_a_guessed_path(self):
        case, out = self.compact()
        out['files'][PROMPT] = out['files'][PROMPT].split('\nSTATE FILE:')[0]
        self.assertIn('launch missing exact state', check(case, out))
        case, out = self.compact()
        out['chat'] = out['chat'].replace('1回進めて。', '1回進めて。.loop/other-state.md')
        self.assertIn('launch missing exact state', check(case, out))

    def test_compact_full_body_needs_explicit_request(self):
        case, out = package()
        case.pop('show_body', None)
        self.assertIn('unrequested full Loop body', check(case, out))

    def test_compact_path_internal_newline_is_rejected(self):
        case, out = self.compact()
        out['chat'] = out['chat'].replace(PROMPT + ' に従い', '.loop/exam\nple.md に従い')
        self.assertIn('newline inside saved path', check(case, out))

    def test_compact_launch_is_not_allowed_in_progress(self):
        case, out = self.compact()
        out['progress'] = [PROMPT + ' に従い1回進めて。']
        self.assertIn('launch or full contract leaked into progress', check(case, out))

    def test_compact_shell_quoted_argument_cannot_contain_newline(self):
        case, out = package(options=[('sh',
            f'cd "/tmp/long\npath" && codex exec resume session-42 "Follow {PROMPT}; update {STATE}."',
            'A — Recommended: CI resume | Codex OS terminal')])
        self.assertIn('newline inside quoted argument or identifier', check(case, out))

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
