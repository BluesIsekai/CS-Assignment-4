# Cyber Security (IT-30001) - Web Server Security Assignment

## PRASHANT KUMAR  IIT2024122  

## Variant Documentation: OS Command Injection (In-band)

### (a) Vulnerable Implementation
The vulnerability resides in `server.js` within the `POST /ping-vuln` endpoint. The route extracts raw input from `req.body.host` and directly concatenates it into a shell command string:

```javascript
app.post('/ping-vuln', (req, res) => {
  const host = req.body.host;
  const command = `ping -c 1 ${host}`;

  exec(command, (error, stdout, stderr) => {
    res.send(`<pre>Executed: ${command}\n\nOutput:\n${stdout || stderr || error}</pre><a href="/">Back</a>`);
  });
});
```

---

### (b) Working Exploit
* **Target Endpoint:** `POST /ping-vuln`
* **Exploit Payloads:**
  * Primary: `127.0.0.1; whoami`
  * System enumeration: `127.0.0.1; id; uname -a`
  * Arbitrary file read: `127.0.0.1; cat /etc/passwd`
* **Evidence of Execution (In-band):**
  The command output is sent straight back across the active HTTP connection and displayed inside the `<pre>` tag of the HTTP response. The browser displays both the standard ping transmission statistics and the execution output of `whoami` (the system user running the Node.js process).

---

### (c) Root Cause
Untrusted user input (`req.body.host`) is concatenated directly into a shell command string passed to Node's `child_process.exec()` API. 

Under the hood, `exec()` invokes a system shell wrapper (`/bin/sh` on Unix or `cmd.exe` on Windows). Because the application fails to separate code from data or sanitize special characters, the shell interprets metacharacters such as `;`, `&`, `|`, and newline as command separators. Consequently, the shell terminates the original `ping` command and immediately spawns the injected secondary command under the security context of the Node.js server process.

---

### (d) Mitigation Implemented
* **Selected Fix:** Parameterized Execution using an Argument Vector (Safe API).
* **Mitigated Code Path (`POST /ping-secure`):**

```javascript
app.post('/ping-secure', (req, res) => {
  const host = req.body.host;


  execFile('ping', ['-c', '1', host], (error, stdout, stderr) => {
    if (error) {
      return res.send(`<pre>Execution failed or blocked safely:\n${stderr || error.message}</pre><a href="/">Back</a>`);
    }
    res.send(`<pre>Output:\n${stdout}</pre><a href="/">Back</a>`);
  });
});
```

* **Why the Fix Works:**
  `child_process.execFile()` calls the binary (`ping`) directly via system-level execution routines (e.g., `execve(2)`), bypassing the shell interpreter completely. 
* **Verification / Evidence of Blocking:**
  When testing the exact same payload (`127.0.0.1; whoami`) against `/ping-secure`:
  * The shell metacharacter `;` is not interpreted.
  * The entire payload string is passed as a single literal hostname argument to the `ping` executable.
  * The ping utility fails safely with a lookup error (`ping: cannot resolve 127.0.0.1; whoami: Unknown host`), completely neutralizing arbitrary command execution.

---

### (e) Other Mitigations (Theory from Lecture Slides)
In addition to parameterized execution with argument vectors, the following defenses mitigate OS command injection:

1. **Avoid the Shell Entirely (Native APIs):**
   Instead of delegating functionality to external operating system binaries, applications should rely on built-in runtime modules or native libraries (e.g., Node's native `net.Socket` or `dns.lookup()` to test host connectivity rather than spawning a system `ping` subprocess).
2. **Allow-list Input Validation:**
   Enforce strict syntactical verification on all user inputs before they reach process boundaries. For a ping utility, an allow-list regular expression (e.g., `^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$` for strict IPv4 addresses) rejects any input containing whitespace, quotes, or metacharacters (`;`, `&`, `|`, `` ` ``, `$`).
3. **Principle of Least Privilege:**
   The web server process should run under an isolated, unprivileged service account (e.g., `www-data` or `nobody`) rather than `root` or an administrative user. Combining this with containerization (Docker) or `chroot`/jails ensures that even if arbitrary command execution is achieved, attacker capabilities are strictly contained.

---

## How to Run the Demonstration

1. Install dependencies:
   ```bash
   npm init -y
   npm install express
   ```
2. Start the server:
   ```bash
   node server.js
   ```
3. Access the portal at: `http://localhost:3000`