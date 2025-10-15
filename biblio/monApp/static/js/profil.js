  document.getElementById("edit-btn").addEventListener("click", function() {
    const elements = document.querySelectorAll(".editable");
    const isEditing = this.textContent === "Enregistrer";

    if (!isEditing) {
      elements.forEach(el => {
        const currentValue = el.textContent.trim();
        const input = document.createElement("input");
        input.type = "text";
        input.className = "profile-input";
        input.name = el.dataset.label;
        input.value = currentValue;
        el.replaceWith(input);
      });
      this.textContent = "Enregistrer";
    } else {

      const inputs = document.querySelectorAll(".profile-input");
      inputs.forEach(input => {
        const span = document.createElement("span");
        span.className = "editable";
        span.dataset.label = input.name;
        span.textContent = input.value;
        input.replaceWith(span);
      });
      this.textContent = "Modifier";
    }
  });