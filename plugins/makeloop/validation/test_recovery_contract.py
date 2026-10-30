"""Real-template recovery proposals and negative output checks; no live Goal is started."""
import copy
import unittest

from check_outputs import check
from test_handoff_contract import rendered_output, CONTRACT_PATH, STATE_PATH


def recovery_output(host):
    case, out = rendered_output(host, handoff=False)
    case.update(goal_launch_required=True, completion_pair_required=True, remediation_required=True)
    target = 'Claude Code' if host == 'claude' else 'Codex CLI'
    goal = ('/goal Follow ' + CONTRACT_PATH + ' including its REMEDIATION SCOPE to prove '
            'every original requirement. Preserve ' + STATE_PATH + '. ')
    if host == 'claude':
        goal += ('End incompletely only at an actual user/platform limit or after a surfaced '
                 'remediation assessment proves no productive authorized repair/alternative '
                 'or independent work remains, including only approval/other-owner waits such '
                 'as required human review with party and condition surfaced after independent '
                 'authorized work is exhausted. FINAL only for verified original success.')
    else:
        goal += ('An incomplete checkpoint is not achievement. Apply the saved native '
                 'block/pause rules only after the remediation assessment; never reset state.')
    ordinary = ('Follow ' + CONTRACT_PATH + ' through completion in the current execution, '
                'including necessary authorized prerequisite repair. Preserve ' + STATE_PATH + '.')
    brief = ('Loop brief: repair the auth result; restore declared dependencies only under '
             'the saved authorization and verify the repair before returning to original work.\n'
             'How it stops: original verified success, actual limit or evidenced lack of '
             'authorized productive recovery and independent work; required review stays unmet.\n'
             + ('Codex run options: ' if host == 'codex' else 'Run options: ') +
             'A Goal continuation (recommended), B current-execution completion.\n'
             'One owner only; generated, not configured and not started.\n')
    out['chat'] = (brief + '\n```markdown\n' + out['files'][CONTRACT_PATH] + '```\n\n'
        '## Launch commands\n### A — Recommended: finish the repair | ' + target + ' input\n'
        '```text\n' + goal + '\n```\n\n'
        '### B — Finish now without native continuation | ' + target + ' input\n'
        '```text\n' + ordinary + '\n```')
    return case, out


class RecoveryProposalTests(unittest.TestCase):
    def test_recovery_pair_and_actual_boundaries_survive_rendering(self):
        for host in ('claude', 'codex'):
            with self.subTest(host=host):
                case, out = recovery_output(host)
                self.assertEqual(check(case, out), [])
                bad = copy.deepcopy(out)
                bad['chat'] = bad['chat'].split('### B —')[0].rstrip()
                self.assertIn('ordinary completion alternative missing or bounded to one tick',
                              check(case, bad))
                bad = copy.deepcopy(out)
                old = bad['files'][CONTRACT_PATH]
                bad['files'][CONTRACT_PATH] = old.replace('REMEDIATION SCOPE:', 'REPAIRS:')
                bad['chat'] = bad['chat'].replace(old, bad['files'][CONTRACT_PATH])
                self.assertIn('missing project-bound remediation scope', check(case, bad))
                bad = copy.deepcopy(out)
                bad['chat'] = bad['chat'].replace('through completion in the current execution',
                                                'for exactly one iteration')
                self.assertIn('ordinary completion alternative missing or bounded to one tick',
                              check(case, bad))
                if host == 'claude':
                    for exit_clause in ('only blockers remain', 'only actual blockers remain',
                                        '阻害要因だけが残ったら終了',
                                        'only blockers remain. Record a remediation assessment'):
                        bad = copy.deepcopy(out)
                        bad['chat'] = bad['chat'].replace(
                            'after a surfaced remediation assessment proves no productive authorized '
                            'repair/alternative or independent work remains', exit_clause)
                        self.assertIn('unqualified blocker exit in Claude Goal launch', check(case, bad))
                # Existing state/authority remains untouched, rather than resetting after repair.
                self.assertEqual(out['files'][STATE_PATH], '# Repair state\nStatus: not started\nIterations used: 0\n')
                self.assertIn('Human review remains required', out['files'][CONTRACT_PATH])
                self.assertIn('no global installs', out['files'][CONTRACT_PATH])
