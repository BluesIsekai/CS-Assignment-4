const form = document.getElementById("commentForm");
const commentsEl = document.getElementById("comments");
const messageEl = document.getElementById("formMessage");

async function loadComments() {
  commentsEl.textContent = "Loading comments...";
  try {
    const response = await fetch("/api/comments");
    if (!response.ok) throw new Error("Could not load comments");
    const comments = await response.json();
    commentsEl.innerHTML = "";
    if (!comments.length) {
      commentsEl.textContent = "No comments yet. Add the first one above.";
      return;
    }
    comments.forEach((comment) => {
      const card = document.createElement("article");
      card.className = "comment-card";
      // INTENTIONAL LAB FLAW: database values are interpreted as HTML.
      card.innerHTML = `
        <div class="comment-meta"><strong>${comment.username}</strong><span>#${comment.id}</span></div>
        <p>${comment.comment}</p>
        <small>${new Date(comment.created_at).toLocaleString()}</small>
      `;
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
    messageEl.textContent = "Saved. Reloading comments...";
    await loadComments();
    messageEl.textContent = "Comment saved.";
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
