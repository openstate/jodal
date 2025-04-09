<script>
    export let message;
</script>

<div class="message-container mb-4 {message.role === 'assistant' ? 'bg-gray-50' : ''}">
    <div class="max-w-3xl mx-auto px-4 py-3">
        <div class="flex items-start">
            {#if message.role === 'assistant'}
                <div class="flex-shrink-0 mr-3">
                    <img src="/bron-logo-small.svg" alt="Bron AI" class="h-8 w-8">
                </div>
            {/if}
            <div class="flex-1 overflow-hidden">
                <p class="text-gray-900 whitespace-pre-wrap">{message.content}</p>
            </div>
        </div>
    </div>
</div> 