// Function to scroll to the top of the page for long tables
function scrollToTop() {
  document.body.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show or hide the "Back to Top" button based on scroll position
let backToTopButton = document.getElementById("back-to-top-button");

window.addEventListener("scroll", () => {
  if (window.scrollY > 300) { // over 300 pixels, show the button
     backToTopButton.style.display = "block";
  } else {
     backToTopButton.style.display = "none";
  }
});
