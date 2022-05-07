import React from "react";
import { createRoot } from "react-dom/client"
import App from "./src/App.js";
import "./src/styles/build.css";
import axios from "axios";

axios.defaults.baseURL = 'http://127.0.0.1:5000/';

const root = createRoot(document.querySelector('#app'));

root.render(<App/>);