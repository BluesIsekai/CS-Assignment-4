require("dotenv").config();
const express = require("express");
const path = require("path");
const commentsRouter = require("./routes/comments");

const app = express();
const PORT = Number(process.env.PORT || 3000);

app.use(express.json({ limit: "20kb" }));
app.use(express.urlencoded({ extended: false }));
app.use("/api/comments", commentsRouter);
app.use(express.static(path.join(__dirname, "..", "frontend")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "..", "frontend", "index.html"));
});

app.use((err, req, res, next) => {
  console.error(err.message);
  res.status(500).json({ error: "Server/database error. Check your MySQL configuration." });
});

// Bind to loopback only: this deliberately vulnerable lab must remain local.
app.listen(PORT, "127.0.0.1", () => {
  console.log(`CommentHub running at http://127.0.0.1:${PORT}`);
});
