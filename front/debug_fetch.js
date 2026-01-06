const https = require('http');

function fetch(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    console.log("Raw data:", data);
                    reject(e);
                }
            });
        }).on('error', reject);
    });
}

async function run() {
    try {
        console.log("Fetching search results...");
        const searchResults = await fetch('http://localhost:8000/api/salles/search/');
        console.log("Search Results (first item):", JSON.stringify(searchResults[0] || searchResults, null, 2));

        let id;
        if (Array.isArray(searchResults) && searchResults.length > 0) {
            id = searchResults[0].id;
        } else if (searchResults.results && searchResults.results.length > 0) {
            id = searchResults.results[0].id; // Pagination?
        }

        if (!id) {
            console.log("No ID found in search results.");
            return;
        }

        console.log(`Fetching details for gym ID: ${id}...`);
        const details = await fetch(`http://localhost:8000/api/salles/${id}/`);
        console.log("Gym Details:", JSON.stringify(details, null, 2));

    } catch (err) {
        console.error("Error:", err.message);
    }
}

run();
