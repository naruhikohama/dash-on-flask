let tabs;

console.log("Teste");

let interval = setInterval(() => {
  if (document.readyState === "complete") {
    clearInterval(interval);
    tabs = document.querySelectorAll(".navlink-custom");
    console.log(tabs);
    addActiveClass();
  }
}, 1000);

function addActiveClass() {
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
    });
  });
}
