<script>
    import { page } from '$app/stores';
    import { API_BASE_URL } from '$lib/config';
    import { onMount } from 'svelte';
    import { sessionStore } from '$lib/stores/sessionStore';

    let showFeedbackModal = false;
    let showNoticeModal = false;
    let formData = {
        question: '',
        name: '',
        email: '',
        session_id: ''
    };
    let showThankYou = false;
    let isSubmitting = false;
    let feedbackModalContent;
    let noticeModalContent;

    $: formData.session_id = $sessionStore.sessionId;

    function handleClickOutsideFeedbackModal(event) {
        if (feedbackModalContent && !feedbackModalContent.contains(event.target)) {
            closeFeedbackModal();
        }
    }

    function handleClickOutsideNoticeModal(event) {
        if (noticeModalContent && !noticeModalContent.contains(event.target)) {
            closeNoticeModal();
        }
    }

    function closeFeedbackModal() {
        showFeedbackModal = false;
        showThankYou = false;
        formData = { question: '', name: '', email: '' };
    }

    function closeNoticeModal() {
        showNoticeModal = false;
    }

    function openNoticeModal() {
        console.log('openNoticeModal');
        showNoticeModal = true;
    }

    async function handleSubmitFeedbackModal() {
        isSubmitting = true;
        let feedbackEndpoint = `${API_BASE_URL}/feedback`;

        if (formData.session_id) {
            feedbackEndpoint = `${feedbackEndpoint}/${formData.session_id}`;
        }

        try {
            const response = await fetch(feedbackEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: formData.question,
                    name: formData.name || '',
                    email: formData.email || '',
                })
            });

            if (response.ok) {
                showThankYou = true;
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
        } finally {
            isSubmitting = false;
        }
    }
</script>

<header class="fixed w-full top-0 z-10 bg-gray-100">
    <div class="top-0 left-0 w-full h-10 bg-black z-50 text-center py-1 flex items-center justify-center" >
        <button
            on:click={openNoticeModal}
            class="text-blue-200 hover:underline" >
            🎉 Bron chat lanceert! Wordt ook VIP gast
        </button>
    </div>
    <div class="px-2 sm:px-6 lg:px-8">
        <div class="flex h-12 sm:h-16">
            <div class="flex-shrink-0 flex items-center">
                <a href="/" class="">
                    <img class="hidden sm:block h-8 w-auto ml-1" src="/bron-logo.svg" alt="Bron Logo" />
                    <img class="block sm:hidden h-6 w-auto ml-0.5" src="/bron-logo-small.svg" alt="Bron Logo" />
                </a>
                <a href="/" class="ml-2 sm:ml-0 sm:mt-1">
                    <span class="text-black text-3xl sm:text-4xl font-bold">chat</span>
                    <!-- <svg xmlns="http://www.w3.org/2000/svg" class="inline-block h-4 w-4 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg> -->
                </a>
                <img
                    class="h-4 sm:h-5 -mt-2 sm:-mt-2 ml-1"
                    src="/beta-badge.svg" 
                    alt="Beta"
                />
                <a href="/" target="_blank" class="hidden sm:flex ml-2 font-medium text-sm sm:text-base items-center mt-1 sm:mt-2 hover:underline">                      
                    <span class="pr-1 md:hidden">Nieuw</span>
                    <span class="pr-1 hidden md:inline">Nieuwe chat</span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 sm:w-4 h-3 sm:h-4">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                      </svg>
                </a>
            </div>
            <div class="flex items-center ml-auto pr-4 pl-8">
                <button
                    on:click={() => showFeedbackModal = true}
                    class="text-blue-600 hover:underline"
                >
                    <div class="flex items-center flex-wrap flex-col md:flex-row">                        
                        <svg xmlns="http://www.w3.org/2000/svg" class="block lg:hidden h-4 w-4 lg:h-5 lg:w-5 mr-1 mb-0 lg:mb-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                        </svg>
                        <span class="hidden lg:inline font-medium">
                            <svg xmlns="http://www.w3.org/2000/svg" class="inline-block h-4 w-4 lg:h-5 lg:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                            </svg>
                            Hebben wij je vraag <br>kunnen beantwoorden?
                        </span>
                        <span class="block lg:hidden font-medium text-sm leading-0">Feedback</span>
                </div>
                </button>
            </div>
            <div class="flex-shrink-0 flex items-center">
                <a href="https://svdj.nl" target="_blank">
                    <img class="hidden sm:block h-7 lg:h-12 w-auto" src="/incubator.png" alt="SvdJ Incubator Logo" />
                    <img class="block sm:hidden h-6 lg:h-10 w-auto" src="/incubator.png" alt="SvdJ Incubator Logo" />
                </a>
                <a href="https://openstate.eu" target="_blank">
                    <img class="hidden lg:block h-7 lg:h-11 w-auto" src="/open-state-foundation-logo.svg" alt="Open State Foundation Logo" />
                    <img class="block lg:hidden h-6 lg:h-9 w-auto ml-1" src="/open-state-foundation-logo-small.svg" alt="Open State Foundation Logo" />
                </a>
            </div>
        </div>
    </div>
</header>

{#if showFeedbackModal}
    <div 
        class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
        on:click={handleClickOutsideFeedbackModal}
    >
        <div 
            bind:this={feedbackModalContent}
            class="bg-white rounded-lg p-8 max-w-md w-full mx-4"
        >
            {#if showThankYou}
                <div class="text-center relative">
                    <button 
                        on:click={closeFeedbackModal}
                        class="absolute -top-4 -right-4 text-gray-500 hover:text-gray-700"
                    >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                    <h2 class="text-2xl font-bold mb-4">Bedankt voor je feedback!</h2>
                    <p>We waarderen je input.</p>

                    <p class="mt-4">
                        Wil je een verhaal maken met behulp van Bron chat, of
                        heb je meer vragen over deze tool?
                    </p>

                    <h3 class="text-lg font-bold mt-4">Neem dan contact met ons op</h3>
                    <p>Joost van de Loo</p>
                    <p>tel: 06-50733904</p>
                    <p><a href="mailto:joostvandeloo@svdjincubator.nl" class="text-blue-600 hover:underline">joostvandeloo@svdjincubator.nl</a></p>
                </div>
            {:else}
                <div class="flex justify-between items-start mb-4">
                    <h2 class="text-xl font-bold">Hebben wij je vraag kunnen beantwoorden?</h2>
                    <button 
                        on:click={closeFeedbackModal}
                        class="text-gray-500 hover:text-gray-700"
                    >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <form on:submit|preventDefault={handleSubmitFeedbackModal} class="space-y-4">
                    <div>
                        <textarea
                            id="question"
                            name="question"
                            bind:value={formData.question}
                            required
                            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                            rows="3"
                            placeholder="Vraag, opmerking, suggestie"
                        ></textarea>
                    </div>
                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
                            Naam
                        </label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            bind:value={formData.name}
                            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                            E-mail
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            bind:value={formData.email}
                            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <input 
                        type="hidden"
                        id="session_id" 
                        name="session_id" 
                        bind:value={formData.session_id}
                    />
                    <button
                        type="submit"
                        disabled={isSubmitting}
                        class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
                    >
                        {isSubmitting ? 'Verzenden...' : 'Verstuur feedback'}
                    </button>
                </form>
            {/if}
        </div>
    </div>
{/if} 


{#if showNoticeModal}
    <div 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        on:click={handleClickOutsideNoticeModal}
    >
        <div class="bg-white rounded-lg p-6 max-w-2xl max-h-[90vh] overflow-y-auto"
            bind:this={noticeModalContent}>
            <div class="flex justify-between items-start mb-4 w-full">
                <h2 class="text-xl font-bold">Wil je onze VIP gast zijn?</h2>
                <button
                    on:click={closeNoticeModal}
                    class="text-gray-500 hover:text-gray-700"
                >
                    ✕
                </button>
            </div>
            
            <div class="space-y-4">
                <p class="">Op dinsdag 18 februari 2025 lanceren we Bron chat. Bij Open State Foundation, met een avond en programma speciaal voor nuchtere onderzoekers:</p>
                
                <div>
                    <ul class="list-disc pl-5 space-y-1">
                        <li><strong>Bron chat demo:</strong> met voorbeeld uit de praktijk</li>
                        <li><strong>Kritische Reviewer Carrousel:</strong> met 10 lokale en landelijke journalisten</li>
                        <li><strong>Q&A:</strong> met makers van Bron chat</li>
                    </ul>
                </div>

                <div class="mt-4">
                    <p>
                        <span class="font-bold" >Locatie en tijd:</span> Marineterrein in Amsterdam, 19:30 - 21:00 (inloop vanaf 19:00).
                    </p>
                </div>
                <div class="mt-4">
                    <p>Wil je erbij zijn? Wil je iets delen, heb je een idee of een vraag? Neem contact op met </p>
                    <p>Joost van de Loo, <a href="tel:06-50733904" class="text-blue-600 hover:underline">06-50733904</a>, <a href="mailto:joostvandeloo@svdjincubator.nl" class="text-blue-600 hover:underline">joostvandeloo@svdjincubator.nl</a></p>
                </div>
            </div>
        </div>
    </div>
{/if}