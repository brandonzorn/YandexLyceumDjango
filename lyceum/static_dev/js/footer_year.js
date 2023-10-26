document.addEventListener("DOMContentLoaded", function() {
  var year = new Date().getFullYear();
  var footer = document.getElementById("footer_content");
  footer.innerHTML = year;
});
