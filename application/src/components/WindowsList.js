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
        return <li key={value}>
            {key} : {value} <WindowRow handle={value}/>
        </li>
    })
    return (
        <ul className="bg-black">
            {windowItem} 
        </ul>
    )
}