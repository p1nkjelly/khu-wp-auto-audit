const express = require('express');
const basicAuth = require('basic-auth-connect');
const fs = require('fs');
const child_process = require('child_process');
const path = require('path');

const app = express();
const PORT = 8000;

// Basic Auth 설정
app.use(basicAuth('username', 'password'));
app.use(express.static(path.join(__dirname, './')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/run', (req, res) => {
    child_process.spawn('python3', ['/app/progpilot_wp/progpilot.py', req.query.update1, req.query.update2, req.query.active1, req.query.active2, req.query.download1, req.query.download2], {shell: true, uid: 0, detached: true, stdio: 'pipe', cwd: '/app/progpilot_wp'});
    return res.redirect("/");
});

app.get('/get-json', (req, res) => {
    let time = req.query.file;
    const files = fs.readdirSync(`../results/${time}`);
    let jsonData = [];

    for (let file of files) {
        if (file.endsWith('.json')) {
            let content = fs.readFileSync(`../results/${time}/${file}`);
            let name = file.split('_')[1].split('.')[0];
            jsonData.push(`{"name":"${name}","file":"${time}/${file}","result":`+JSON.parse(content).length+'}');
        }
    }

    res.json(jsonData);
});

app.get('/get-results', (req, res) => {
    const files = fs.readdirSync('../results');
    var count = 0;
    let jsonData = [];

    for (let file of files) {
	const results = fs.readdirSync(`../results/${file}`);
	count = 0;
	for (let result of results) {
            if (result.endsWith('.json')) {
                let content = fs.readFileSync(`../results/${file}/${result}`);
	        let name = file.split('_')[1].split('.')[0];
		count = count + JSON.parse(content).length;
            }
	}
        jsonData.push(`{"name":"${file}","file":"${file}","result":`+count+'}');
    }

    res.json(jsonData);
});

app.get('/get-result', (req, res) => {
    let time = req.query.file;
    const files = fs.readdirSync(`../results/${time}`);
    let vulnData = {};
    let jsonData = [];

    for (let file of files) {
        if (file.endsWith('.json')) {
            let content = fs.readFileSync(`../results/${time}/${file}`);
            let results = JSON.parse(content);

            for (i in results) {
                if (results[i].vuln_name in vulnData) {
                    vulnData[results[i].vuln_name] += 1; 
                } else {
                    vulnData[results[i].vuln_name] = 1;
                }
            }
        }
    }
    for (const [key, value] of Object.entries(vulnData)) {
        jsonData.push(`{"name":"${key}","count":"${value}"}`);
    }
    res.json(jsonData);
});

app.get('/get-filter', (req, res) => {
    let time = req.query.file;
    const filters = fs.readFileSync(`../results/${time}/filter.txt`, 'utf8');
    let filter = filters.split(" ");
    let jsonData = [];

    jsonData.push(`{"update1":${filter[0]}, "update2":${filter[1]}, "active1":${filter[2]}, "active2":${filter[3]}, "download1":${filter[4]}, "download2":${filter[5]}}`);
    
    res.json(jsonData);
});

app.get('/get-result1', (req, res) => {
    let path = req.query.file;
    const file = fs.readFileSync(`../results/${path}`);
    let vulnData = {};
    let jsonData = [];
    
    let results = JSON.parse(file);  

    for (i in results) {
        if (results[i].vuln_name in vulnData) {
            vulnData[results[i].vuln_name] += 1; 
        } else {
            vulnData[results[i].vuln_name] = 1;
        }
    }
    for (const [key, value] of Object.entries(vulnData)) {
        jsonData.push(`{"name":"${key}","count":"${value}"}`);
    }
    res.json(jsonData);
});

app.get('/get-json1', (req, res) => {
    let path = req.query.file;
    const file = fs.readFileSync(`../results/${path}`);
    let jsonData = [];
    let results = JSON.parse(file);  

    for (i in results) {
        let code = fs.readFileSync(results[i].sink_file, 'utf8');
        let lines = code.split("\n");
        let final_code = lines.slice(results[i].sink_line-50, results[i].sink_line+50).join('\\n')
        final_code = final_code.replaceAll('\t', '\\t');
        final_code = final_code.replaceAll('"', '\\"');
        //final_code = final_code.replaceAll("'", "\\'");
        jsonData.push(`{"name":"${results[i].sink_file.split('plugins/')[1]}","code":"${final_code}","vuln":"${results[i].vuln_name}"}`);
    }
    res.json(jsonData);
});

app.get('/result', (req, res) => {
    res.sendFile(path.join(__dirname, 'result.html'));
});

app.get('/detail', (req, res) => {
    res.sendFile(path.join(__dirname, 'detail.html'));
});

app.get('/raw', (req, res) => {
    let path = req.query.file;
    if (path) {
        const file = fs.readFileSync(`../results/${path}`);
        res.json(JSON.parse(file));
    }
    else {
        res.json({"result":"none"})
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

