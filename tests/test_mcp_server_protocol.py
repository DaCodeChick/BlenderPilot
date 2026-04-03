"""Protocol-level checks for local MCP JSON-RPC server."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


class TestMCPServerProtocol(unittest.TestCase):
    def setUp(self):
        server = Path(__file__).resolve().parents[1] / "mcp_server" / "main.py"
        self.proc = subprocess.Popen(
            [sys.executable, str(server)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def tearDown(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=2)
        if self.proc.stdin:
            self.proc.stdin.close()
        if self.proc.stdout:
            self.proc.stdout.close()
        if self.proc.stderr:
            self.proc.stderr.close()

    def _rpc(self, payload):
        self.proc.stdin.write(json.dumps(payload) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        self.assertTrue(line)
        return json.loads(line)

    def test_initialize_and_list_tools(self):
        init = self._rpc(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"clientInfo": {"name": "test", "version": "0.0.0"}},
            }
        )
        self.assertIn("result", init)
        self.assertEqual(init["result"]["protocolVersion"], "2024-11-05")

        tools = self._rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        self.assertIn("result", tools)
        self.assertGreater(len(tools["result"]["tools"]), 0)

    def test_unknown_method(self):
        res = self._rpc({"jsonrpc": "2.0", "id": 3, "method": "unknown/method"})
        self.assertIn("error", res)
        self.assertEqual(res["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()
