// Fetch News
fetch("data/news.json")
  .then(res => res.json())
  .then(news => {
    const container = document.getElementById("news-container");
    news.forEach(item => {
      const div = document.createElement("div");
      div.classList.add("news-item");
      div.innerHTML = `<h3>${item.title}</h3><p>${item.content}</p>`;
      container.appendChild(div);
    });
  });

// Fetch Scores
fetch("data/scores.json")
  .then(res => res.json())
  .then(scores => {
    const container = document.getElementById("scores-container");
    scores.forEach(student => {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${student.name}</td><td>${student.subject}</td><td>${student.score}</td>`;
      container.appendChild(row);
    });
  });

// Fetch Events
fetch("data/events.json")
  .then(res => res.json())
  .then(events => {
    const container = document.getElementById("events-container");
    events.forEach(event => {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${event.date}</td><td>${event.event}</td>`;
      container.appendChild(row);
    });
  });

