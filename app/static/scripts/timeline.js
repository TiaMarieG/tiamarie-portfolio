async function fetchPosts() {
   const res = await fetch("/api/timeline_post");
   const data = await res.json();
   const container = document.getElementById("timeline-posts");
   container.innerHTML = "";
   data.timeline_posts.forEach((post) => {
      const postElement = document.createElement("div");
      postElement.className = "timeline-post";
      postElement.innerHTML = `
        <p><strong>${post.name}</strong> (${post.email})</p>
        <p>${post.content}</p>
    `;
      container.appendChild(postElement);
   });
}

async function submitPost(event) {
   event.preventDefault();
   const form = event.target;
   const formData = new FormData(form);

   await fetch("/api/timeline_post", {
      method: "POST",
      body: formData,
   });

   form.reset();
   fetchPosts();
}

window.onload = fetchPosts;
