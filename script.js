document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("guests");
    const popup = document.getElementById("popup");
    const overlay = document.getElementById("overlay");
    const yesButton = document.getElementById("yesButton");
    const noButton = document.getElementById("noButton");
    const counts = {
      adults: 1,
      children: 0,
      pets: 0
    };
  
    inputField.addEventListener("click", () => {
        popup.style.display = "block";
        overlay.style.display = "block";
    });
  
    overlay.addEventListener("click", () => closePopup());
  
    document.querySelectorAll(".increment").forEach(button => {
      button.addEventListener("click", () => {
        const target = button.dataset.target;
        counts[target]++;
        document.getElementById(target).textContent = counts[target];
      });
    });
  
    document.querySelectorAll(".decrement").forEach(button => {
      button.addEventListener("click", () => {
        const target = button.dataset.target;
        if (counts[target] > 0) {
          counts[target]--;
          document.getElementById(target).textContent = counts[target];
        }
      });
    });
  
    yesButton.addEventListener("click", () => {
      yesButton.classList.add("bg-green-500");
      noButton.classList.remove("bg-green-500");
      closePopup();
    });
  
    noButton.addEventListener("click", () => {
      noButton.classList.add("bg-green-500");
      yesButton.classList.remove("bg-green-500");
      closePopup();
    });
  
    function closePopup() {
      setTimeout(() => {
        popup.style.display = "none";
        overlay.style.display = "none";
        inputField.value = `${counts.adults} Adults, ${counts.children} Children, ${counts.pets} Pets`;
      }, 200);
    }
  });
  