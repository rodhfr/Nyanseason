const express = require('express');
const { exec } = require('child_process'); 
const app = express();
const port = 3000;
const cors = require('cors');

app.use(cors());
app.use(express.static('public')); // serve frontend from the public folder

app.get('/run-python', (req, res) => {
  exec('python /home/rodhfr/Code/Nyanseason/nyaa-webserver/python_example/simple_script.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send('Error executing Python script');
    }
    if (stderr) {
      console.error(`Python stderr: ${stderr}`);
      return res.status(500).send('Python error occurred');
    }

    // send python output as response
    res.send(`Python Output: ${stdout}`);
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
})
