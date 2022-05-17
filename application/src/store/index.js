import create from 'zustand';
import axios from 'axios';
export const useStore =  create(set => ({
    windows: {},
    fetchWindows: async () => {
        const { data, error } = await axios.get('/windows');
        set({ windows: data })
    }
    // runTask: async (handle) => {
    //     const { data } 
    // }
}));
