document.addEventListener("DOMContentLoaded", () => {
  const episodesList = document.getElementById("episodes-list");
  const guestsList = document.getElementById("guests-list");
  const form = document.getElementById("appearance-form");
  const msg = document.getElementById("appearance-msg");

  // Fetch Episodes
  fetch("/episodes")
    .then((res) => res.json())
    .then((episodes) => {
      episodes.forEach((ep) => {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between";
        li.innerHTML = `
            <span>Ep#${ep.number} - ${ep.date}</span>
            <button class="btn btn-sm btn-danger" onclick="deleteEpisode(${ep.id})">Delete</button>
          `;
        episodesList.appendChild(li);
      });
    });

  // Fetch Guests
  fetch("/guests")
    .then((res) => res.json())
    .then((guests) => {
      guests.forEach((g) => {
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.textContent = `${g.name} - ${g.occupation}`;
        guestsList.appendChild(li);
      });
    });

  // Handle appearance form
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const episodeId = document.getElementById("episode-id").value;
    const guestId = document.getElementById("guest-id").value;
    const rating = document.getElementById("rating").value;

    fetch("/appearances", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        episode_id: parseInt(episodeId),
        guest_id: parseInt(guestId),
        rating: parseFloat(rating),
      }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to add appearance");
        return res.json();
      })
      .then((data) => {
        msg.textContent = `✅ Appearance added for ${data.guest.name} in episode ${data.episode.number}`;
        msg.className = "text-success";
        form.reset();
      })
      .catch(() => {
        msg.textContent = "❌ Error adding appearance";
        msg.className = "text-danger";
      });
  });
});

function deleteEpisode(id) {
  fetch(`/episodes/${id}`, {
    method: "DELETE",
  }).then((res) => {
    if (res.ok) {
      alert("Episode deleted!");
      location.reload();
    } else {
      alert("Failed to delete episode.");
    }
  });
}
