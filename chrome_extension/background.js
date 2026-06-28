// Background service worker for Gmail Spam Detector AI

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "predictSpam") {
    console.log("Received check request for text length:", request.text ? request.text.length : 0);
    
    fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: request.text || "",
        subject: request.subject || ""
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log("Prediction result:", data);
      sendResponse({ success: true, data: data });
    })
    .catch(error => {
      console.error("Error fetching spam prediction:", error);
      sendResponse({ 
        success: false, 
        error: "Không thể kết nối đến Flask API (http://localhost:5000). Hãy chắc chắn rằng Flask server đang chạy (python app.py) và không bị chặn bởi tường lửa." 
      });
    });

    // Return true to indicate we wish to send a response asynchronously
    return true;
  }
});
