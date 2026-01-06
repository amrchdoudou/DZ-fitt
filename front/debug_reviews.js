
const api = require('./src/api');

async function checkReviews() {
    try {
        // Assuming gym ID 1 or the one from the screenshot
        // We will try ID 12 as seen in screenshot "gym12"
        // Wait, screenshot says "gym12" but we don't know the ID.
        // Let's try fetching public gym for ID 2 (from previous context).

        console.log("Fetching reviews for Gym ID 2...");
        // API client might need axios configuration or just use fetch if in node
        // Since we are in node, we can't easily use the src/api.js if it relies on browser specific things.
        // Let's just use fetch directly.

        const response = await fetch('http://localhost:8000/api/salles/2/avis/');
        const data = await response.json();

        console.log("Reviews Data:");
        console.log(JSON.stringify(data, null, 2));

    } catch (e) {
        console.error("Error:", e);
    }
}

checkReviews();
