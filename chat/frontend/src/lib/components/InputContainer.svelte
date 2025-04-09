<script>
    import { createEventDispatcher } from 'svelte';
    
    export let disabled = false;
    export let loading = false;
    
    const dispatch = createEventDispatcher();
    let inputValue = '';
    
    function handleSubmit() {
        if (inputValue.trim() && !disabled) {
            dispatch('submit', inputValue.trim());
            inputValue = '';
        }
    }
    
    function handleKeydown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSubmit();
        }
    }
</script>

<div class="max-w-3xl mx-auto w-full">
    <form class="relative" on:submit|preventDefault={handleSubmit}>
        <textarea
            bind:value={inputValue}
            on:keydown={handleKeydown}
            placeholder="Stel een vraag..."
            rows="1"
            class="w-full resize-none rounded-lg border border-gray-300 bg-white px-4 py-2.5 pr-16 text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-black focus:ring-black sm:text-sm sm:leading-6 disabled:opacity-50"
            {disabled}
        ></textarea>
        <button
            type="submit"
            disabled={disabled || !inputValue.trim()}
            class="absolute bottom-2 right-2 rounded-lg p-2 text-gray-400 hover:text-gray-500 disabled:opacity-50"
        >
            {#if loading}
                <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-900"></div>
            {:else}
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
            {/if}
        </button>
    </form>
</div> 