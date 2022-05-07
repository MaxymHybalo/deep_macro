import React  from "react";
import { useEffect, useState } from "react";
import axios from "axios";

export default function WindowsList() {

    const [windows, setWindows] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get('windows')
            .then((response) => { setWindows(response.data) })
            .catch(setError)
    },[]);
    const windowItem = Object.entries(windows).map(([key, value]) => {
        return <li key={value}>{key} : {value} </li>
    })
    return (
        <ul className="bg-black">
            {windowItem} 
        </ul>
    )
}