import React from "react";
import WindowsList from "./components/WindowsList";
import { useStore } from './store'
import { useEffect } from "react";
export default function App() {

        const fetchSettings = useStore(state => state.fetchSettings);
        useEffect(() => {
            fetchSettings();
        })
        return (
            <div>
                <h1>New react controll center</h1>
                <WindowsList/>
            </div>
        )

}