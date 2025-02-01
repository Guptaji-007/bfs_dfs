const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require('path');
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '..')));

// Serve index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'index.html'));
});

// Handle path finding requests
app.post('/api/path', (req, res) => {
    try {
        const { strategy, grid } = req.body;
        console.log('Received request:', { strategy, grid });

        const pythonProcess = spawn('python3', [
            path.join(__dirname, '..', 'logic.py'),
            JSON.stringify(grid),
            strategy
        ]);

        let dataString = '';

        pythonProcess.stdout.on('data', (data) => {
            dataString += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error('Python error:', data.toString());
        });

        pythonProcess.on('close', (code) => {
            console.log('Python process exited with code:', code);
            if (code === 0) {
                try {
                    const result = JSON.parse(dataString);
                    res.json({ path: result });
                } catch (error) {
                    console.error('JSON parse error:', error);
                    res.status(500).json({ error: 'Invalid response from Python script' });
                }
            } else {
                res.status(500).json({ error: 'Python script execution failed' });
            }
        });

    } catch (error) {
        console.error('Server error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something broke!' });
});

module.exports = app;