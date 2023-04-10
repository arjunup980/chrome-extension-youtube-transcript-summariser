// const btn = document.getElementById("summarise");
// btn.addEventListener("click", function(){
//     btn.disabled = true;
//     btn.innerHTML = "Summarising...";
//     chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
//         var url = tabs[0].url;
//         fetch("http://127.0.0.1:5000/summary?url=" + url)
//             .then(response => response.text())
//             .then(text => {
//                 const p = document.getElementById("output");
//                 p.innerHTML = text;
//                 btn.disabled = false;
//                 btn.innerHTML = "summarise";
//             });
//     });
// });



const btn = document.getElementById("summarise");
btn.addEventListener("click", async function(){
    btn.disabled = true;
    btn.innerHTML = "Summarising...";
    try {
        const tabs = await chrome.tabs.query({currentWindow: true, active: true});
        const url = tabs[0].url;
        const response = await fetch("http://127.0.0.1:8000/transcript?url=" + url);
        if (!response.ok) {
            throw new Error('Unable to fetch summary');
        }
        const text = await response.text();
        const p = document.getElementById("output");
        p.innerHTML = text;
    } catch (err) {
        const p = document.getElementById("output");
        p.innerHTML = "Error: " + err.message;
    } finally {
        btn.disabled = false;
        btn.innerHTML = "summarise";
    }
});


