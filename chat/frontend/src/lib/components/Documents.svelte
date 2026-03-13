<script>
    import { createEventDispatcher } from 'svelte';
    import { fade } from 'svelte/transition';
    import Document from './Document.svelte';
    import { sessionStore } from '$lib/stores/sessionStore';

    export let selectedDocuments = null;
    export let citationText = '';
    export let citationWords = [];
    export let isDocumentsPanelOpen = false;

    const dispatch = createEventDispatcher();

    function handleShowAllDocuments() {
        dispatch('showAllDocuments');
    }

    function togglePanel(event) {
        event.stopPropagation(); // Prevent click from bubbling to document
        dispatch('togglePanel');
    }

    function sortDocuments(docs) {
        if (!docs) return [];
        return [...docs].sort((a, b) => {
            const dateA = new Date(a.data.published || 0);
            const dateB = new Date(b.data.published || 0);
            return dateB - dateA; // Sort descending
        });
    }

    $: documents = $sessionStore.documents || [];
    $: sortedDocuments = documents ? sortDocuments(documents) : [];
    $: sortedSelectedDocuments = selectedDocuments ? sortDocuments(selectedDocuments) : null;

</script>

<div class="pt-10 pb-6 lg:pt-10 lg:pb-0 pl-4 lg:pl-6 lg:pr-2 flex flex-col h-full relative">
    <button
        class="absolute top-8 sm:top-10 -left-16 bg-gray-50 border border-gray-300 rounded-l-xl p-2 lg:p-2 rounded-l-lg flex items-center justify-center transition-colors duration-200 {isDocumentsPanelOpen ? 'hidden' : ''}"
        on:click={togglePanel}
    >
        {#if !isDocumentsPanelOpen}
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            <svg fill="currentColor" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
            class="w-6 h-6" viewBox="0 0 256.61 256.61"
            xml:space="preserve">
                <g>
                    <path d="M60.859,112.533c-6.853,0-6.853,10.646,0,10.646c27.294,0,54.583,0,81.875,0c6.865,0,6.865-10.646,0-10.646
                        C115.442,112.533,88.153,112.533,60.859,112.533z"/>
                    <path d="M142.734,137.704c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.634,0,10.634c27.294,0,54.583,0,81.875,0
                        C149.6,148.338,149.6,137.704,142.734,137.704z"/>
                    <path d="M142.734,161.018c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.633,0,10.633c27.294,0,54.583,0,81.875,0
                        C149.6,171.65,149.6,161.018,142.734,161.018z"/>
                    <path d="M142.734,186.184c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.629,0,10.629c27.294,0,54.583,0,81.875,0
                        C149.6,196.812,149.6,186.184,142.734,186.184z"/>
                    <path d="M141.17,209.934c-27.302,0-54.601,0-81.89,0c-6.848,0-6.848,10.633,0,10.633c27.289,0,54.588,0,81.89,0
                        C148.015,220.566,148.015,209.934,141.17,209.934z"/>
                    <path d="M25.362,58.087V256.61h152.877V85.63l-28.406-27.543H25.362z M165.026,243.393H38.585V71.305h104.443v20.97h21.988
                        v151.118H165.026z"/>
                    <polygon points="51.204,27.667 51.204,50.645 64.427,50.645 64.427,40.88 168.875,40.88 168.875,61.85 190.868,61.85 
                        190.868,212.971 185.059,212.971 185.059,226.188 204.086,226.188 204.086,55.205 175.68,27.667 			"/>
                    <polygon points="202.837,0 78.363,0 78.363,22.983 91.581,22.983 91.581,13.218 196.032,13.218 196.032,34.188 218.025,34.188 
                        218.025,185.306 212.221,185.306 212.221,198.523 231.248,198.523 231.248,27.543 			"/>
                </g>
            </svg>
        {/if}
    </button>

    <div class="flex justify-between items-center mb-4 align-middle lg:px-2">
        <div class="flex items-center justify-center w-full">
            
            {#if citationText}
                <div class="flex items-center flex-wrap pr-2">
                    <button
                        class="py-2 lg:pr-2 lg:pl-0 flex items-center show-all-documents-btn"
                        on:click={handleShowAllDocuments}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
                        </svg>

                        <svg fill="currentColor" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                            class="w-6 h-6 mr-2" viewBox="0 0 256.61 256.61"
                            xml:space="preserve">
                            <g>
                                <path d="M60.859,112.533c-6.853,0-6.853,10.646,0,10.646c27.294,0,54.583,0,81.875,0c6.865,0,6.865-10.646,0-10.646
                                    C115.442,112.533,88.153,112.533,60.859,112.533z"/>
                                <path d="M142.734,137.704c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.634,0,10.634c27.294,0,54.583,0,81.875,0
                                    C149.6,148.338,149.6,137.704,142.734,137.704z"/>
                                <path d="M142.734,161.018c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.633,0,10.633c27.294,0,54.583,0,81.875,0
                                    C149.6,171.65,149.6,161.018,142.734,161.018z"/>
                                <path d="M142.734,186.184c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.629,0,10.629c27.294,0,54.583,0,81.875,0
                                    C149.6,196.812,149.6,186.184,142.734,186.184z"/>
                                <path d="M141.17,209.934c-27.302,0-54.601,0-81.89,0c-6.848,0-6.848,10.633,0,10.633c27.289,0,54.588,0,81.89,0
                                    C148.015,220.566,148.015,209.934,141.17,209.934z"/>
                                <path d="M25.362,58.087V256.61h152.877V85.63l-28.406-27.543H25.362z M165.026,243.393H38.585V71.305h104.443v20.97h21.988
                                    v151.118H165.026z"/>
                                <polygon points="51.204,27.667 51.204,50.645 64.427,50.645 64.427,40.88 168.875,40.88 168.875,61.85 190.868,61.85 
                                    190.868,212.971 185.059,212.971 185.059,226.188 204.086,226.188 204.086,55.205 175.68,27.667 			"/>
                                <polygon points="202.837,0 78.363,0 78.363,22.983 91.581,22.983 91.581,13.218 196.032,13.218 196.032,34.188 218.025,34.188 
                                    218.025,185.306 212.221,185.306 212.221,198.523 231.248,198.523 231.248,27.543 			"/>
                            </g>
                        </svg>
                    
                    </button>
                </div>
            {:else}
                <div class="flex items-center justify-center ">
                    <svg fill="currentColor" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                        class="w-6 h-6 mr-2" viewBox="0 0 256.61 256.61"
                        xml:space="preserve">
                        <g>
                            <path d="M60.859,112.533c-6.853,0-6.853,10.646,0,10.646c27.294,0,54.583,0,81.875,0c6.865,0,6.865-10.646,0-10.646
                                C115.442,112.533,88.153,112.533,60.859,112.533z"/>
                            <path d="M142.734,137.704c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.634,0,10.634c27.294,0,54.583,0,81.875,0
                                C149.6,148.338,149.6,137.704,142.734,137.704z"/>
                            <path d="M142.734,161.018c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.633,0,10.633c27.294,0,54.583,0,81.875,0
                                C149.6,171.65,149.6,161.018,142.734,161.018z"/>
                            <path d="M142.734,186.184c-27.292,0-54.581,0-81.875,0c-6.853,0-6.853,10.629,0,10.629c27.294,0,54.583,0,81.875,0
                                C149.6,196.812,149.6,186.184,142.734,186.184z"/>
                            <path d="M141.17,209.934c-27.302,0-54.601,0-81.89,0c-6.848,0-6.848,10.633,0,10.633c27.289,0,54.588,0,81.89,0
                                C148.015,220.566,148.015,209.934,141.17,209.934z"/>
                            <path d="M25.362,58.087V256.61h152.877V85.63l-28.406-27.543H25.362z M165.026,243.393H38.585V71.305h104.443v20.97h21.988
                                v151.118H165.026z"/>
                            <polygon points="51.204,27.667 51.204,50.645 64.427,50.645 64.427,40.88 168.875,40.88 168.875,61.85 190.868,61.85 
                                190.868,212.971 185.059,212.971 185.059,226.188 204.086,226.188 204.086,55.205 175.68,27.667 			"/>
                            <polygon points="202.837,0 78.363,0 78.363,22.983 91.581,22.983 91.581,13.218 196.032,13.218 196.032,34.188 218.025,34.188 
                                218.025,185.306 212.221,185.306 212.221,198.523 231.248,198.523 231.248,27.543 			"/>
                        </g>
                    </svg>
                </div>
            {/if}  

            {#if citationText}
                <div class="text-sm lg:text-base leading-tight w-full mr-auto">"{citationText}"</div>
            {:else}
                <div class="text-lg font-semibold w-full mr-auto">Documenten</div>
            {/if}

            {#if isDocumentsPanelOpen}
                <div class="flex items-center justify-center mr-2">
                    <button
                        class="transition-colors duration-200"
                        on:click={togglePanel}
                    >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            {/if}
        </div>
    </div>
    
    <div class="flex-grow pr-4 overflow-y-auto overflow-x-hidden">
        <div class="space-y-6">
            {#if sortedSelectedDocuments && sortedSelectedDocuments.length > 0}
                {#each sortedSelectedDocuments as doc, index}
                    <div in:fade={{delay: index * 300, duration: 300}}>
                        <Document {doc} {citationWords} />
                    </div>
                {/each}
            {:else if sortedDocuments.length > 0}
                {#each sortedDocuments as doc, index}
                    <div in:fade={{delay: index * 300, duration: 300}}>
                        <Document {doc} {citationWords} />
                    </div>
                {/each}      
            {:else}
                <div class="space-y-6 hidden lg:block">
                    {#each Array(3) as _, i}
                        <div class="shadow rounded-lg p-4 border border-gray-400 border-dashed bg-gray-50 h-8 flex items-center justify-center opacity-50">
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    button {
        transition: transform 0.3s ease;
    }
    
    button:hover {
        transform: scale(1.1);
    }
</style>
