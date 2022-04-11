let { PythonShell } = require('python-shell')

const RUN_CLIENTS = '[data-run-clients]';
const SCRIPTS = './../backend';

function runClients({ target }) {
    console.log(target.dataset.command);
    const options = {
        scriptPath: SCRIPTS,
        args: [target.dataset.command]
    };

    PythonShell.run('clients_utils.py', options, (error, results) => {
        console.log('results: %j', results);
    });
}

function listenEvents() {
    Array.from(document.querySelectorAll(RUN_CLIENTS), el => {
        el.addEventListener('click', runClients);
    });
}

document.addEventListener('DOMContentLoaded', listenEvents);
