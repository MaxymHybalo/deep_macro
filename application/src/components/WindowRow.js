import React  from "react";
import { useState } from "react";
import { useStore } from '../store/index';
import axios from "axios";
import CommandType from './CommandType';

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
            <CommandType handle={props.handle}/>
            <button className="btn" onClick={run}>{title}</button>
            <button className="btn" onClick={stop}>Stop</button>
        </>
    )
}