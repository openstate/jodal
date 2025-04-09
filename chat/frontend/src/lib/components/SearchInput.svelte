<script>
    import BaseInput from './BaseInput.svelte';
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    
    export let isLoading = false;
    export let value = '';

    function handleSubmit(event) {
        console.debug('search input handleSubmit', event);
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
    placeholder="Stel een vraag..."
    on:submit={handleSubmit}
>
    <div slot="button">
        <button 
            type="submit"
            class="cursor-pointer p-0.5 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 scale-110 rotate-90"
            disabled={!value.trim() || isLoading}
        >
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-2xl">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M15.1918 8.90615C15.6381 8.45983 16.3618 8.45983 16.8081 8.90615L21.9509 14.049C22.3972 14.4953 22.3972 15.2189 21.9509 15.6652C21.5046 16.1116 20.781 16.1116 20.3347 15.6652L17.1428 12.4734V22.2857C17.1428 22.9169 16.6311 23.4286 15.9999 23.4286C15.3688 23.4286 14.8571 22.9169 14.8571 22.2857V12.4734L11.6652 15.6652C11.2189 16.1116 10.4953 16.1116 10.049 15.6652C9.60265 15.2189 9.60265 14.4953 10.049 14.049L15.1918 8.90615Z" fill="currentColor"></path>
            </svg>
        </button>
    </div>
</BaseInput> 