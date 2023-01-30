import React from "react";
import WindowsList from "./components/WindowsList";
import Runner from './components/client/Runner';
import { useStore } from './store'
import { useEffect } from "react";
export default function App() {

        const fetchSettings = useStore(state => state.fetchSettings);
        useEffect(() => {
            fetchSettings();
        });

        return (
            <div className="container mx-auto">
                <Runner/>
                <WindowsList/>
            </div>
        )

}