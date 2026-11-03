const form = document.getElementById("commentForm");
const commentsEl = document.getElementById("comments");
const messageEl = document.getElementById("formMessage");

async function loadComments() {
  commentsEl.textContent = "Loading comments...";
  try {
    const response = await fetch("/api/comments");
    if (!response.ok) throw new Error("Could not load comments");
    const comments = await response.json();
    commentsEl.replaceChildren();
    if (!comments.length) {
      commentsEl.textContent = "No comments yet. Add the first one above.";
      return;
    }
    comments.forEach((comment) => {
      const card = document.createElement("article");
      card.className = "comment-card";

      const meta = document.createElement("div");
      meta.className = "comment-meta";
      const name = document.createElement("strong");
      name.textContent = comment.username;
      const id = document.createElement("span");
      id.textContent = `#${comment.id}`;
      meta.append(name, id);

      const paragraph = document.createElement("p");
      // MITIGATION: untrusted content is inserted as text, never parsed as HTML.
      paragraph.textContent = comment.comment;

      const date = document.createElement("small");
      date.textContent = new Date(comment.created_at).toLocaleString();

      card.append(meta, paragraph, date);
      commentsEl.appendChild(card);
    });
  } catch (error) {
    commentsEl.textContent = error.message;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  messageEl.textContent = "Saving...";
  try {
    const response = await fetch("/api/comments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: document.getElementById("username").value,
        comment: document.getElementById("comment").value
      })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Could not save comment");
    form.reset();
    await loadComments();
    messageEl.textContent = "Comment saved and rendered safely.";
  } catch (error) {
    messageEl.textContent = error.message;
  }
});

document.getElementById("refresh").addEventListener("click", loadComments);
document.getElementById("copyPayload").addEventListener("click", async () => {
  await navigator.clipboard.writeText(`<img src=x onerror="alert('Stored XSS executed!')">`);
  messageEl.textContent = "Payload copied.";
});
loadComments();
