import React  from "react";
import { useState, useEffect } from "react";
import { useStore } from '../store/index';

export default function WindowRow(props) {

    const {settings, updateCommand } = useStore(state => ({
        settings: state.settings,
        updateCommand: state.updateSettings
    }));

    if (!settings.types) return <></>

    const optionsEl = settings.types.map(o => 
            <option value={o} key={o}>
                {o}
            </option>);

    return (
        <>
            <select className="dropdown" onChange={
                (e) => updateCommand({handle: props.handle, value: e.target.value, type: "type" })}>
                {optionsEl}
            </select>
        </>
    )
}