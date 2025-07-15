document.addEventListener("DOMContentLoaded", () => {
  const elements = document.getElementsByClassName("choices__autocomplete");
  for (element of elements) {
    new Choices(element);
  }
});
