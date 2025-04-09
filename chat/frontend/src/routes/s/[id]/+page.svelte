<script>
    import ChatLayout from '$lib/components/ChatLayout.svelte';
    import { sessionStore } from '$lib/stores/sessionStore';

    export let data;

    const MAINTENANCE_MODE = false; // You can toggle this to enable/disable maintenance mode
    const MAINTENANCE_MESSAGE = "Bron chat is momenteel niet beschikbaar wegens onderhoud. Wanneer we weer online zijn wordt zoeken nog beter en gemakkelijker! Probeer het later opnieuw.";

    $: sessionStore.set({
        sessionId: data.sessionId,
        messages: data.messages || [],
        documents: data.documents || [],
        sessionName: data.sessionName || 'Bron chat',
        locations: data.locations || []
    });
</script>

{#if MAINTENANCE_MODE}
    <div class="fixed inset-0 bg-gray-900 bg-opacity-90 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-lg p-8 max-w-md text-center shadow-xl">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 mx-auto mb-4 text-gray-500">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11.412 15.655 9.75 21.75l3.745-4.012M9.257 13.5H3.75l2.659-2.849m2.048-2.194L14.25 2.25 12 10.5h8.25l-4.707 5.043M8.457 8.457 3 3m5.457 5.457 7.086 7.086m0 0L21 21" />
            </svg>
            <h2 class="text-2xl font-bold mb-4">Onderhoud</h2>
            <p class="text-gray-600">{MAINTENANCE_MESSAGE}</p>
        </div>
    </div>
{/if}

<ChatLayout />

