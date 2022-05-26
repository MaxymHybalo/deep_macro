import create from 'zustand';
import axios from 'axios';
export const useStore =  create(set => ({
    windows: {},
    settings: {},
    postClient: async(type) => {
        await axios.post('/client', { type });
    },
    fetchWindows: async () => {
        const { data, error } = await axios.get('/windows');
        set({ windows: data });
    },
    fetchSettings: async () => {
        const { data, error } = await axios.get('/settings');
        set({ settings: data });

    },
    updateSettings: async ({handle, type, value}) => {
        const { data, error } = await axios.post('/settings', {
            handle, value, type
        });

        set(state => {
            const settings = {
                ...state.windows,
                ...data
            }
            return {windows: settings}
        })
    },
    // runTask: async (handle) => {
    //     const { data } 
    // }
}));
