import React  from "react";
import { useStore } from '../../store/index';

export default function Runner(props) {
    const exec = useStore(state => state.postClient)
    return (
        <>
            <button className="btn" onClick={() => exec('run')}>Run</button>
            <button className="btn" onClick={() => exec('justify')}>Justify</button>
            <button className="btn" onClick={() => exec('login')}>Login</button>
        </>
    )
}