const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const port = 3000;

app.use(cors()); // Enable CORS for frontend requests

// Map strings to image filenames
const imageMap = {
    "apple": "apple.png",
    "banana": "banana.png",
    "cherry": "cherry.png"
};

// Serve images
app.get('/image/:name', (req, res) => {
    const name = req.params.name;
    const imageFilename = imageMap[name];

    if (imageFilename) {
        // Send the image from the 'images' folder
        res.sendFile(path.join(__dirname, 'images', imageFilename));
    } else {
        res.status(404).send('Image not found');
    }
});

// Start the Express server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

