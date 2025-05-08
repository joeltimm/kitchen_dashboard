// Load data from backend API
function fetchCalendar() {
  fetch('/api/calendar')
    .then(response => response.json())
    .then(data => {
      const calendarContainer = document.getElementById("calendar");
      calendarContainer.innerHTML = "<ul>" + data.map(event => `<li>${event.summary} at ${event.start.dateTime}</li>`).join('') + "</ul>";
    });
}

function fetchWeather() {
  fetch('/api/weather')
    .then(response => response.json())
    .then(data => {
      const weatherContainer = document.getElementById("weather");
      weatherContainer.innerHTML = `<p>${data.temperature}°C</p><p>${data.condition}</p>`;
    });
}

function fetchPhotos() {
  fetch('/api/photos')
    .then(response => response.json())
    .then(data => {
      const photosContainer = document.getElementById("photos");
      photosContainer.innerHTML = data.map(photo => `<img src="${photo.url}" alt="photo" style="width: 100%; height: 100%; object-fit: cover;">`).join('');
    });
}

function updateClock() {
  const clockElement = document.getElementById("clock");
  const now = new Date();

  const hours = now.getHours().toString().padStart(2, '0');
  const minutes = now.getMinutes().toString().padStart(2, '0');
  const seconds = now.getSeconds().toString().padStart(2, '0');

  clockElement.innerHTML = `${hours}:${minutes}:${seconds}`;
}

// Initialize draggable and resizable widgets
function initDragAndResize() {
  // Make widgets draggable using Interact.js
  interact('.widget')
    .draggable({
      onmove(event) {
        const { target } = event;
        target.style.transform = `translate(${event.dx}px, ${event.dy}px)`;
      }
    })
    .resizable({
      onresize(event) {
        const { target, width, height } = event;
        target.style.width = `${width}px`;
        target.style.height = `${height}px`;
      }
    });
}

// Initialize the clock
function initClock() {
  updateClock(); // set initial time
  setInterval(updateClock, 1000); // Update every second
}

document.addEventListener('DOMContentLoaded', () => {
  fetchCalendar();
  fetchWeather();
  fetchPhotos();
  initDragAndResize();
  intiClock();
});
