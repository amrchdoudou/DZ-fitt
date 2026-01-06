const http = require('http');

const options = {
    hostname: 'localhost',
    port: 8000,
    path: '/api/salles/5/',
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
};

const req = http.request(options, (res) => {
    let data = '';

    console.log(`STATUS: ${res.statusCode}`);

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        try {
            console.log('BODY:', JSON.stringify(JSON.parse(data), null, 2));
        } catch (e) {
            console.log('BODY (raw):', data);
        }
    });
});

req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
});

req.end();
