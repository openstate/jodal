import { error } from '@sveltejs/kit';
import { API_BASE_URL } from '$lib/config';

export async function load({ params, fetch }) {
    const sessionId = params.id;

    try {
        const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`);

        if (!response.ok) {
            if (response.status === 404) {
                throw error(404, {
                    message: 'Chat sessie niet gevonden'
                });
            }
            throw error(response.status || 500, {
                message: 'Er is iets fout gegaan bij het ophalen van de chat sessie'
            });
        }

        const sessionData = await response.json();
        return {
            sessionId,
            messages: sessionData.messages || [],
            documents: sessionData.documents || [],
            sessionName: sessionData.name || 'Bron chat - Doorzoek 3.5 miljoen overheidsdocumenten met AI',
            locations: sessionData.locations || []
        };
    } catch (err) {
        if (err.status) throw err;
        
        throw error(500, {
            message: 'Er is iets fout gegaan bij het ophalen van de chat sessie'
        });
    }
}
