<script>
    import BaseInput from './BaseInput.svelte';
    import { createEventDispatcher } from 'svelte';    
    const dispatch = createEventDispatcher();
    
    export let locations = [];
    export let isLoading = false;
    export let value = '';
    export let initialLocations = [];
    export let initialYearRange = [];

    function handleSubmit(event) {
        const searchParams = {
            ...event.detail,
            value
        };
        dispatch('submit', searchParams);
    }
</script>

<BaseInput
    bind:value
    {isLoading}
    {locations}            
    {initialLocations}
    {initialYearRange}
    placeholder="Stel een vervolg vraag..."
    on:submit={handleSubmit}
    on:stop
>
    <div slot="button" let:isLoading let:handleStop>
        {#if isLoading}
            <button 
                type="button" 
                on:click={handleStop}
                class="p-0.5 bg-blue-800 text-white rounded-full hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-700"
            >
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-2xl">
                    <rect x="8" y="8" width="16" height="16" fill="currentColor"></rect>
                </svg>
            </button>
        {:else}
            <button 
                type="submit" 
                class="cursor-pointer p-0.5 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={!value.trim()}
            >
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-2xl">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M15.1918 8.90615C15.6381 8.45983 16.3618 8.45983 16.8081 8.90615L21.9509 14.049C22.3972 14.4953 22.3972 15.2189 21.9509 15.6652C21.5046 16.1116 20.781 16.1116 20.3347 15.6652L17.1428 12.4734V22.2857C17.1428 22.9169 16.6311 23.4286 15.9999 23.4286C15.3688 23.4286 14.8571 22.9169 14.8571 22.2857V12.4734L11.6652 15.6652C11.2189 16.1116 10.4953 16.1116 10.049 15.6652C9.60265 15.2189 9.60265 14.4953 10.049 14.049L15.1918 8.90615Z" fill="currentColor"></path>
                </svg>
            </button>
        {/if}
    </div>
</BaseInput> 