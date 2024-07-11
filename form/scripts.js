document.addEventListener("DOMContentLoaded", () => {
  const updateTimeAndDay = () => {
    const now = new Date();
    document.querySelector('[data-testid="currentTimeUTC"]').textContent =
      now.toUTCString();
    document.querySelector('[data-testid="currentDay"]').textContent =
      now.toLocaleString("en-US", { weekday: "long" });
  };

  updateTimeAndDay();
  setInterval(updateTimeAndDay, 1000); // Update every second
});
