import React  from "react";
import { useState } from "react";
import { useStore } from '../store/index';
import axios from "axios";
import CommandType from './CommandType';

export default function WindowRow(props) {

    const { windows, getActiveProp } = useStore(state => ({
        windows: state.windows,
        getActiveProp: state.getActiveProp
    }));
    if (!windows) return <></>
    const operation = getActiveProp(props.name);
    const status = windows[props.name]?.[operation]?.value;
    const [title, setTitle] = useState(status.run ? 'Runned!' : 'Run!');
    const [runned, setRunned] = useState(status);
    const run = () => {
        // if (status.run) return;
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
            <CommandType handle={props.handle} name={props.name}/>
            <button className="btn" onClick={run}>{title}</button>
            <button className="btn" onClick={stop}>Stop</button>
        </>
    )
}