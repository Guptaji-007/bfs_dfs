const { spawn } = require('child_process');

module.exports = (req, res) => {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    try {
        const { strategy, grid } = req.body;
        console.log('Received request:', { strategy, grid });

        const pythonProcess = spawn('python3', ['logic.py', JSON.stringify(grid), strategy]);

        let dataString = '';

        pythonProcess.stdout.on('data', (data) => {
            dataString += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error('Python error:', data.toString());
        });

        pythonProcess.on('close', (code) => {
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
};
