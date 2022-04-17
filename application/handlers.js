let { PythonShell } = require('python-shell')

const RUN_CLIENTS = '[data-run-clients]';
const SEND = '[data-send]';
const INPUT = '[data-input]';
const OUTPUT = '[data-output]';
const STOP = '[data-stop]';
const SCRIPTS = './../backend';

const DEFAULT_PYTHON_OPTIONS = {
    scriptPath: SCRIPTS
};
function runClients({ target }) {
    console.log(target.dataset.command);
    const options = {
        ...DEFAULT_PYTHON_OPTIONS,
        args: [target.dataset.command]
    };

    PythonShell.run('clients_utils.py', options, (error, results) => {
        console.log('results: %j', results);
    });
}
const py = new PythonShell('io.py', DEFAULT_PYTHON_OPTIONS);

function handleInputCommand() {
    const input = document.querySelector(INPUT);
    const output = document.querySelector(OUTPUT);

    py.send(input.value);

    py.on('message', name => {
        output.innerText = name;
    });
}

function stopCommand() {
    py.end((error, code, signal) => {
        console.log(error, code, signal);
    });
} 
function listenEvents() {
    Array.from(document.querySelectorAll(RUN_CLIENTS), el => {
        el.addEventListener('click', runClients);
    });

    document.querySelector(SEND).addEventListener('click', handleInputCommand);
    document.querySelector(STOP).addEventListener('click', stopCommand);
}

document.addEventListener('DOMContentLoaded', listenEvents);
