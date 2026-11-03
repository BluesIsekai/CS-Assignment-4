const express = require("express");
const router = express.Router();
const db = require("../database");

// The server uses parameterized SQL in BOTH modes. The intentional teaching
// vulnerability is in the vulnerable page's browser-side rendering sink.
router.get("/", async (req, res, next) => {
  try {
    const [rows] = await db.execute(
      "SELECT id, username, comment, created_at FROM comments ORDER BY id DESC"
    );
    res.json(rows);
  } catch (error) {
    next(error);
  }
});

router.post("/", async (req, res, next) => {
  try {
    const username = String(req.body.username || "").trim();
    const comment = String(req.body.comment || "").trim();

    if (!username || !comment) {
      return res.status(400).json({ error: "Please enter both a name and a comment." });
    }
    if (username.length > 100 || comment.length > 2000) {
      return res.status(400).json({ error: "Name or comment is too long." });
    }

    const [result] = await db.execute(
      "INSERT INTO comments (username, comment) VALUES (?, ?)",
      [username, comment]
    );

    res.status(201).json({
      id: result.insertId,
      username,
      comment,
      message: "Comment saved."
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
