const express = require("express");
const app = express();
const spawn = require("child_process").spawn;
const bodyParser = require('body-parser');

// pip install -r requirements.txt
// node app.js

// Middleware
app.use(express.static('public'))
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.get('/', (req, res) => {
	res.sendFile(__dirname + '/index.html');
})

app.post('/api/download', (req, res) => {
	// These two lines of code download the YouTube Video based on the user-provided link

	const pythonProcess = spawn('python3', [`${process.cwd()}\\app\\download-and-process-video.py`, req.body.videoUrl]);
	let sent = false;

	pythonProcess.stdout.on('data', data => {
		data = data.toString();
		if (data.startsWith('DONE') && !sent)
			res.send(data.toString());
	});
	pythonProcess.stderr.on('data', data => {
		console.log(data.toString());
		lines = data.toString().split('\n');
		res.send('ERROR ' + lines[lines.length - 2]);
		sent = true;
	});
	pythonProcess.on('close', code => {});
});

app.get('/error', (req, res) => {
	res.sendFile('404.html', { root: __dirname + '/public'});
});

let port = process.env.PORT || 3000;
app.listen(port, () => {
	console.log(`server running on port ${port}`);
});