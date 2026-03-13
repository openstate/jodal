import { writable } from 'svelte/store';

function createSessionStore() {
    const { subscribe, set, update } = writable({
        sessionId: null,
        messages: [],
        documents: [],
        sessionName: '',
        locations: []
    });

    return {
        subscribe,
        set,
        update,
        reset: () => set({
            sessionId: null,
            messages: [],
            documents: [],
            sessionName: 'Bron chat - Doorzoek 3.5 miljoen overheidsdocumenten met AI',
            locations: []
        })
    };
}

export const sessionStore = createSessionStore();