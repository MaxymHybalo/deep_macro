import React  from "react";
import { useEffect, useState } from "react";
import WindowRow from "./WindowRow";
import { useStore } from './../store/index';

export default function WindowsList() {

    const fetchWindows = useStore(state => state.fetchWindows);
    const windows = useStore(state => state.windows);
    useEffect(() => {
        fetchWindows()
    },[]);
    
    const windowItem = Object.entries(windows).map(([key, value]) => {
        const handle = value.process_id
        return <li className="grid gap-4 grid-cols-4 grid-rows-1" key={handle}>
            <span className="flex p-1 justify-center items-center">{key} : {handle}</span>
            <WindowRow name={key} handle={handle}/>
        </li>
    })
    return (
        <ul className="bg-black">
            {windowItem} 
        </ul>
    )
}