const { app, BrowserWindow, webFrameMain } = require('electron');

const createWindow = () => {
    const win = new BrowserWindow({
        width: 400,
        height: 400
    });
    
    win.setMenu(null);
    win.loadFile('index.html')
}

app.whenReady().then(() => {
    createWindow()
})

app.on('window-all-closed', () => {
    app.quit()
})