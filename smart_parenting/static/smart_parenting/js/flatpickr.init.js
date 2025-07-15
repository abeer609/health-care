document.addEventListener("DOMContentLoaded", () => {
  const elements = document.getElementsByClassName("flatpickr__datepicker");
  for (let i = 0; i < elements.length; i++) {
    const dateFormat = elements[i].dataset["format"];
    flatpickr(elements[i], {
      dateFormat,
      disable: [
        function (date) {
          return date.getDay() == 5;
        },
      ],
    });
  }
});
