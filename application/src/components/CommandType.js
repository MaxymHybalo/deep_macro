import React  from "react";
import { useState, useEffect } from "react";
import { useStore } from '../store/index';

export default function WindowRow(props) {

    const {settings, windows, updateCommand } = useStore(state => ({
        settings: state.settings,
        windows: state.windows,
        updateCommand: state.updateSettings
    }));

    if (!settings.types) return <></>
    let selected = Object.entries(windows[props.name]).find(([, value]) => value.value && value.value.active)?.[0] || settings.types[0];
    const optionsEl = settings.types.map(o => 
            <option value={o} key={o}>
                {o}
            </option>
        );
    
    const changePayload = e => ({
        handle: props.handle,
        value: { active: true },
        type: e.target.value
    });
    return (
        <>
            <select className="dropdown" value={selected} onChange={
                (e) => updateCommand(changePayload(e))}>
                {optionsEl}
            </select>
        </>
    )
}