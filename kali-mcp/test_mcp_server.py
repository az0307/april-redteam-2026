#!/usr/bin/env python3
"""
Unit tests for the Kali MCP server.

These tests exercise the command-construction logic of every tool WITHOUT
touching a real Kali host: ``run_ssh_command`` is patched to capture the
command string that each tool would execute. This lets CI verify behaviour
with no SSH target, credentials, or network access.
"""
import unittest
from unittest import mock

import mcp_server as s


class ToolCommandTests(unittest.TestCase):
    def setUp(self):
        # Patch the single choke-point every tool routes through.
        patcher = mock.patch.object(s, "run_ssh_command", return_value="OK")
        self.run = patcher.start()
        self.addCleanup(patcher.stop)

    def last_cmd(self) -> str:
        """The command string passed to the most recent run_ssh_command call."""
        self.assertTrue(self.run.called, "run_ssh_command was not called")
        return self.run.call_args.args[0]

    # ── kali_exec ────────────────────────────────────────────
    def test_exec_passes_command_and_timeout(self):
        s.kali_exec("id", timeout=42)
        self.run.assert_called_once_with("id", timeout=42)

    # ── kali_nmap ────────────────────────────────────────────
    def test_nmap_default_flags_no_ports(self):
        s.kali_nmap("10.0.0.1")
        cmd = self.last_cmd()
        self.assertIn("nmap", cmd)
        self.assertIn("-sV -sC --open", cmd)
        self.assertIn("10.0.0.1", cmd)
        self.assertNotIn("-p ", cmd)  # no port arg when ports empty

    def test_nmap_with_ports(self):
        s.kali_nmap("10.0.0.1", flags="-sS", ports="80,443")
        cmd = self.last_cmd()
        self.assertIn("-p 80,443", cmd)
        self.assertIn("-sS", cmd)

    # ── metasploit ───────────────────────────────────────────
    def test_msf_run_uses_resource_script(self):
        s.kali_msf_run("/tmp/x.rc")
        self.assertIn("msfconsole -q -r /tmp/x.rc", self.last_cmd())

    def test_msf_search_quotes_query(self):
        s.kali_msf_search("eternalblue")
        self.assertIn("search eternalblue", self.last_cmd())

    # ── sqlmap ───────────────────────────────────────────────
    def test_sqlmap_quotes_url_and_defaults(self):
        s.kali_sqlmap("http://t/x?id=1")
        cmd = self.last_cmd()
        self.assertIn("sqlmap -u 'http://t/x?id=1'", cmd)
        self.assertIn("--batch", cmd)

    # ── gobuster ─────────────────────────────────────────────
    def test_gobuster_builds_dir_scan(self):
        s.kali_gobuster("http://t", wordlist="/wl.txt")
        cmd = self.last_cmd()
        self.assertIn("gobuster dir -u http://t", cmd)
        self.assertIn("-w /wl.txt", cmd)

    # ── hydra: single vs list variants ───────────────────────
    def test_hydra_single_user_single_pass(self):
        s.kali_hydra("10.0.0.1", "ssh", username="root", password="toor")
        cmd = self.last_cmd()
        self.assertIn("-l root", cmd)
        self.assertIn("-p toor", cmd)
        self.assertNotIn("-L ", cmd)
        self.assertNotIn("-P ", cmd)

    def test_hydra_userlist_passlist(self):
        s.kali_hydra("10.0.0.1", "ssh", userlist="/u.txt", passlist="/p.txt")
        cmd = self.last_cmd()
        self.assertIn("-L /u.txt", cmd)
        self.assertIn("-P /p.txt", cmd)

    # ── tmux helpers ─────────────────────────────────────────
    def test_tmux_new(self):
        s.kali_tmux_new("sess1")
        self.assertIn("tmux new-session -d -s sess1", self.last_cmd())

    def test_tmux_send_appends_enter(self):
        s.kali_tmux_send("sess1", "whoami")
        cmd = self.last_cmd()
        self.assertIn("tmux send-keys -t sess1 'whoami' Enter", cmd)

    def test_tmux_read_tails_lines(self):
        s.kali_tmux_read("sess1", lines=10)
        cmd = self.last_cmd()
        self.assertIn("capture-pane -t sess1", cmd)
        self.assertIn("tail -10", cmd)

    # ── file I/O ─────────────────────────────────────────────
    def test_write_file_uses_quoted_heredoc(self):
        s.kali_write_file("/tmp/a.rc", "use exploit/x\nrun\n")
        cmd = self.last_cmd()
        self.assertIn("cat > '/tmp/a.rc'", cmd)
        self.assertIn("<< 'KALI_MCP_EOF'", cmd)
        self.assertIn("use exploit/x", cmd)

    def test_read_file_head_limits(self):
        s.kali_read_file("/etc/hosts", lines=5)
        cmd = self.last_cmd()
        self.assertIn("cat '/etc/hosts'", cmd)
        self.assertIn("head -5", cmd)

    # ── introspection helpers ────────────────────────────────
    def test_which_tools_includes_core_tools(self):
        s.kali_which_tools()
        cmd = self.last_cmd()
        self.assertIn("which", cmd)
        self.assertIn("nmap", cmd)
        self.assertIn("sqlmap", cmd)

    def test_health_reports_disk_and_memory(self):
        s.kali_health()
        cmd = self.last_cmd()
        self.assertIn("df -h", cmd)
        self.assertIn("free -h", cmd)


class SshHelperTests(unittest.TestCase):
    """run_ssh_command formats stdout/stderr/exit-code without a real host."""

    def _fake_ssh(self, out=b"", err=b"", code=0):
        chan = mock.Mock()
        chan.recv_exit_status.return_value = code
        stdout = mock.Mock()
        stdout.read.return_value = out
        stdout.channel = chan
        stderr = mock.Mock()
        stderr.read.return_value = err
        ssh = mock.Mock()
        ssh.exec_command.return_value = (None, stdout, stderr)
        return ssh

    def test_stdout_only(self):
        with mock.patch.object(s, "get_ssh", return_value=self._fake_ssh(out=b"hello\n")):
            self.assertEqual(s.run_ssh_command("echo hello"), "hello")

    def test_stderr_appended(self):
        with mock.patch.object(s, "get_ssh", return_value=self._fake_ssh(out=b"", err=b"boom")):
            result = s.run_ssh_command("bad")
            self.assertIn("[STDERR]", result)
            self.assertIn("boom", result)

    def test_nonzero_exit_code_reported(self):
        with mock.patch.object(s, "get_ssh", return_value=self._fake_ssh(out=b"x", code=2)):
            self.assertIn("[EXIT CODE: 2]", s.run_ssh_command("false"))


if __name__ == "__main__":
    unittest.main()
