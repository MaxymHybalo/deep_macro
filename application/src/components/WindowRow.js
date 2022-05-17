import React  from "react";
import { useEffect, useState } from "react";
import axios from "axios";

export default function WindowRow(props) {
    const [title, setTitle] = useState('Run!');
    const [runned, setRunned] = useState(false);

    const run = () => {
        if (runned) return;
        axios.post(`/run/${props.handle}`)
            .then(({data}) => {
                if (data.name) {
                    setTitle('Runned!');
                    setRunned(true);
                }
            })
            .catch(console.error)
    }

    const stop = () => {
        axios.post(`/stop/${props.handle}`)
        .then(({data}) => {
            if (!data.name) {
                setTitle('Run!');
                setRunned(false);
            }
        })
        .catch(console.error)
    }
    
    return (
        <>
            <button className="btn" onClick={run}>{title}</button>
            <button className="btn" onClick={stop}>Stop</button>
        </>
    )
}