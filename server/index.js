const summarizeBtn = document.getElementById('summarise');
const copyBtn = document.getElementById('copy-btn');
const refreshBtn = document.getElementById('refresh-btn');
const output = document.getElementById('output');


async function fetchSummary(refresh=false) {
  // summarizeBtn.disabled = true;
  summarizeBtn.innerText = 'Summarizing...';
  output.innerText = 'Loading summary...';
  const tabs = await chrome.tabs.query({currentWindow: true, active: true});
  const url = tabs[0].url;
  fetch(`http://localhost:8000/transcript/?url=${url}&refresh=${refresh}`)
    .then(response => response.json())
    .then(data => {
      output.innerText = data.summary;
      // copyBtn.disabled = false;
      // refreshBtn.disabled = false;
      summarizeBtn.innerText = 'Summarize';
    })
    .catch(error => {
      output.innerText = `Error: ${error.message}`;
      // summarizeBtn.disabled = false;
      summarizeBtn.innerText = 'Summarize';
    });
}




function copySummary() {
    const textToCopy = output.innerText;
    navigator.clipboard.writeText(textToCopy);
  }

// function refreshSummary() {
//   output.innerText = '';
//   copyBtn.disabled = true;
//   refreshBtn.disabled = true;
//   fetchSummary();
// }


async function refreshSummary() {
  output.innerText = 'Refreshing Summary...';
  // copyBtn.disabled = true;
  // refreshBtn.disabled = true;
  try {
    await fetchSummary(refresh=false);
  } catch (error) {
    output.innerText = `Error: ${error.message}`;
    // summarizeBtn.disabled = false;
  }
}




function hardRefreshSummary() {
    output.innerText = '';
    copyBtn.disabled = true;
    refreshBtn.disabled = true;
    fetchSummary(refresh=true);
  }

summarizeBtn.addEventListener('click', refreshSummary);
copyBtn.addEventListener('click', copySummary);
refreshBtn.addEventListener('click', hardRefreshSummary);

// // Disable copy and refresh buttons initially
// copyBtn.disabled = true;
// refreshBtn.disabled = true;






