// Function to convert the markdown README.md file into html and render it as one tab
fetch('README.md')
  .then(response => response.text())
  .then(text => {
    const md = window.markdownit();
    const result = md.render(text);
    document.querySelector('.markdown-body').innerHTML = result;
  });
