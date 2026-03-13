<script>
    import { API_BASE_URL } from '$lib/config';
    
    export let sessionId;
    export let className = '';
    
    async function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    async function handleCloneSession() {
        try {
            const newTab = window.open('/chat', '_blank');
            
            const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/clone`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to clone session');
            }

            const { session_id, messages } = await response.json();
            
            if (newTab) {
                newTab.location.href = `/s/${session_id}`;
            }
            
            await sleep(2000);
            
            newTab.postMessage({
                type: 'REPLAY_MESSAGES',
                messages: messages
            }, window.location.origin);
            
        } catch (error) {
            console.error('Error cloning session:', error);
            // You might want to add error handling UI here
        }
    }
</script>

<button
    on:click={handleCloneSession}
    class={`px-2 py-1 bg-gray-200 text-gray-800 rounded rounded-md hover:bg-gray-300 transition-colors ${className}`}
    title="Creeer deze chat opnieuw"
>
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-4 w-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
    </svg>  
</button> 