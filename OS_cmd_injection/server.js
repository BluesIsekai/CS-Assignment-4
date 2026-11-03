const express = require('express');
const { exec, execFile } = require('child_process');
const app = express();

app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.send(`
    <h2>Server Diagnostic Tool (Ping Utility)</h2>
    
    <h3>1. Vulnerable Endpoint (/ping-vuln)</h3>
    <form action="/ping-vuln" method="POST">
      <input type="text" name="host" placeholder="8.8.8.8" required style="width: 300px;" />
      <button type="submit">Ping (Vulnerable)</button>
    </form>

    <hr/>

    <h3>2. Mitigated Endpoint (/ping-secure)</h3>
    <form action="/ping-secure" method="POST">
      <input type="text" name="host" placeholder="8.8.8.8" required style="width: 300px;" />
      <button type="submit">Ping (Secured)</button>
    </form>
  `);
});

// (a) Vulnerable Implementation
// Root cause: user input is concatenated directly into a shell command string.
app.post('/ping-vuln', (req, res) => {
  const host = req.body.host;
  const command = `ping -c 1 ${host}`;

  exec(command, (error, stdout, stderr) => {
    res.send(`<pre>Executed: ${command}\n\nOutput:\n${stdout || stderr || error}</pre><a href="/">Back</a>`);
  });
});

// (d) Mitigated Implementation
// Fix: Bypass system shell execution entirely using execFile with an argument vector/array.
app.post('/ping-secure', (req, res) => {
  const host = req.body.host;

  // Passing arguments as an array ensures user input is treated strictly as a single data parameter,
  // never parsed by /bin/sh for shell operators like ;, &&, or |.
  execFile('ping', ['-c', '1', host], (error, stdout, stderr) => {
    if (error) {
      return res.send(`<pre>Execution failed or blocked safely:\n${stderr || error.message}</pre><a href="/">Back</a>`);
    }
    res.send(`<pre>Output:\n${stdout}</pre><a href="/">Back</a>`);
  });
});

app.listen(3000, () => console.log('Diagnostic app running at http://localhost:3000'));