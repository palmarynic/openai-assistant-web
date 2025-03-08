async function askAI() {
    let question = document.getElementById("question").value;

    try {  //test
        let response = await fetch('https://openai-assistant-web-sand.vercel.app/api/ask', {  
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' }, 
            body: JSON.stringify({ question })
        });

        let data = await response.json();
        document.getElementById("answer").innerText = "回答：" + (data.answer || data.error);
    } catch (error) {
        document.getElementById("answer").innerText = "發生錯誤：" + error.message;
    }
}
