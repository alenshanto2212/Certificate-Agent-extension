document.getElementById('scoutBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  const manualInput = document.getElementById('manualInterest').value.trim();
  const autoTrackEnabled = document.getElementById('trackHistory').checked;

  statusDiv.textContent = "Analyzing data...";
  
  let finalKeywords = manualInput;

  // If no manual entry is provided, check history
  if (!finalKeywords && autoTrackEnabled) {
    statusDiv.textContent = "Scanning local history profiles...";
    
    // Grab the last 15 items the user visited from Chrome's history API
    const historyItems = await new Promise((resolve) => {
      chrome.history.search({ text: '', maxResults: 15 }, resolve);
    });

    // Extract just the titles of the pages they visited
    const titles = historyItems.map(item => item.title).filter(Boolean);
    
    if (titles.length > 0) {
      finalKeywords = titles.join(" | "); // Pass raw page text blocks to backend
    }
  }

  if (!finalKeywords) {
    statusDiv.textContent = "❌ Please type an interest or enable tracking.";
    return;
  }

  statusDiv.textContent = "Contacting AI Engine...";

  // 🚀 Open the web dashboard tab IMMEDIATELY so the user can watch it load beautifully
  // We send the keywords right inside the URL parameters!
  const backendBaseUrl = "http://127.0.0.1:8000/generate"; // Our local FastAPI server address later
  const targetUrl = chrome.runtime.getURL(`dashboard.html?query=${encodeURIComponent(finalKeywords)}`);
  
  chrome.tabs.create({ url: targetUrl });
  statusDiv.textContent = "Blueprint opened in new tab!";
});