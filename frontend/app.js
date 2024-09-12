document.getElementById('query-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const query = document.getElementById('query').value;
    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;

    const response = await fetch('http://localhost:5000/submit_query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, email, otp })
    });
    const data = await response.json();
    document.getElementById('response').innerText = data.response;
});

document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);

    const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    document.getElementById('document-response').innerText = `Summary: ${data.summary}\nKeywords: ${data.keywords.join(', ')}`;
});
