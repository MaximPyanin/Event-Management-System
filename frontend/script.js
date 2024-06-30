document.getElementById('healthButton').addEventListener('click', () => {
    fetch('http://localhost:8080/api/v1/health', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Health Check Success:', data);
    })
    .catch((error) => {
        console.error('Health Check Error:', error);
    });
});
