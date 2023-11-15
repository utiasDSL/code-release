// Function to convert JSON data to HTML table
function convert() {
  // reinitialize the table every time
  let container = document.getElementById("container");
  if (container.hasChildNodes()) {
    container.removeChild(container.firstChild);
  }

  let conferenceSelect = document.getElementById("conference-select");
  let conference = conferenceSelect.options[conferenceSelect.selectedIndex].value;
  let yearSelect = document.getElementById("year-select");
  let year = yearSelect.options[yearSelect.selectedIndex].value;
  let jsonFile = conference + "/" + year + "_DATA.json";

  // Ignore these columns to render the table
  let coltoIgnore = ["Keywords or Approach", "Conference", "Year", "Benchmark Setup", "Experimental Results", "Keywords", "Benchmarks", "Number", "Unnamed: 11", "First and Last Author Affiliations", "Authors"];

  // Fetch the JSON data from the file
  fetch(jsonFile)
    .then(response => response.json())
    .then(data => {
      // Create the table element
      let table = document.createElement("table");

      let jsonData = JSON.parse(data);

      // Get the keys (column names) of the first object in the JSON data
      let cols = Object.keys(jsonData);

      // Create the header element
      let thead = document.createElement("thead");
      let tr = document.createElement("tr");

      // Loop through the column names and create header cells
      for (let i = 0; i < cols.length; i++) {
        if (coltoIgnore.includes(cols[i])) {
          continue;
        }
        let th = document.createElement("th");
        th.innerText = cols[i]; // Set the column name as the text of the header cell
        tr.appendChild(th); // Append the header cell to the header row
      };

      thead.appendChild(tr); // Append the header row to the header
      table.appendChild(thead); // Append the header to the table

      // Loop through the JSON data and create table rows
      col0 = jsonData[cols[0]];
      len = Object.keys(col0).length;

      // add the data to the table
      for (let i = 0; i < len; i++) {
        let tr = document.createElement("tr"); // Create a new row
        for (let j = 1; j < cols.length; j++) { // number of columns
          if (coltoIgnore.includes(cols[j])) {
            continue;
          }
          let td = document.createElement("td"); // Create a new data cell
          let th = document.createElement("th");
          let value = jsonData[cols[j]][i];

          if (cols[j] == "Code Link" || cols[j] == "Github") {   
            if (value == -1) {
              value = "N/A";
            } else if (typeof value === 'string') {
              value = value.replace(/['"]+/g, ''); // Remove quotation marks from strings

              if (cols[j] == "Github") { // for NeurIPS github links
                const regex = /\[(.*?)\]/; // Remove [] around github links
                const match = value.match(regex);
                if (match) {
                  value = match[1]; // Extract the link without the square brackets
                }
              }
              const githubRegex = /(https?:\/\/(?:www\.)?github\.com\/[^\s]+)/g; // Extract GitHub links
              const githubMatches = value.match(githubRegex);
              if (githubMatches) {
                value = githubMatches.join(", "); // Join multiple GitHub links with a comma
              } else {
                value = "N/A"; // If no GitHub links found, set to "N/A"
              }
            }
  
            // Create a container element to hold both the button and the code link
            let container = document.createElement("div");
            
            // Button for PR
            const button = document.createElement("button");
            button.innerText = "Edit";
            button.classList.add("pr-button");
            button.addEventListener("click", () => {
              // Open a Pull Request for adding/correcting the code link
              const repoUrl = "https://github.com/utiasDSL/code-release";
              const pullRequestUrl = `${repoUrl}/pull/new`;
              const title = encodeURIComponent("Code Link Correction");
              const body = encodeURIComponent(`Please add/correct the code link for paper: ${jsonData[cols[0]][i]}`);
              const link = encodeURIComponent(value);
              const url = `${pullRequestUrl}?title=${title}&body=${body}&link=${link}`;
              window.open(url, "_blank");
            });

            container.appendChild(button); // Add the button to the container
            container.appendChild(document.createElement("br")); // Add a line break

            if (value != null && value.includes("github")) {
              const githubLinks = value.split(", ");
              for (let i = 0; i < githubLinks.length; i++) {
                // Remove trailing punctuationas or signs from the github link, if present
                githubLinks[i] = githubLinks[i].replace(/()[.,!?;]+$/, '');
              }

              const uniqueLinks = new Set(githubLinks); // remove repetitve links
              uniqueLinks.forEach(link => {
                const codeLink = document.createElement("a");
                if (link.includes("github")) {
                  codeLink.href = link;
                  codeLink.textContent = link;
                } else {
                  codeLink.textContent = "N/A";
                }
                codeLink.target = "_blank";
                container.appendChild(codeLink); // Add the code link to the container
                container.appendChild(document.createTextNode(" ")); // Add a space between the links
              });

            }

            td.appendChild(container); // Add the container to the cell

          } else if (cols[j] == "Authors") { // remove quotation marks around authors and separate them with a comma
            if (value == -1) {  
              value = "N/A";
            }
            value = value.replace(/'/g, ',');
            value = value.replace(/(^,)|(,$)/g, '');
            value = value.replace(/^,\s*/gm, '');
            td.textContent = value;
           
          } else {
            if (value == -1) {
              value = "N/A";
            } 
            td.textContent = value;
          }

          tr.appendChild(td); // Add the cell to the row
        }
        table.appendChild(tr); // Add the row to the table
      }
      table.style.textAlign = "center";
      container.appendChild(table) // Append the table to the container element
    });
}
