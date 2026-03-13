<script>
    import { API_BASE_URL } from '$lib/config';
    import { sessionStore } from '$lib/stores/sessionStore';
    
    // Remove the messages prop
    // export let messages = [];
    $: messages = $sessionStore.messages;
    export let currentMessage = null;
    export let currentStatusMessage = null;
    export let autoScroll = true; 
    export let isLoading = false;

    import { createEventDispatcher, onMount, afterUpdate, tick } from 'svelte';
    import { slide } from 'svelte/transition';
    import { computePosition, flip, shift, offset } from '@floating-ui/dom';
    const dispatch = createEventDispatcher();

    let selectedCitation = null;
    let streamedContent = '';
    let streamedStatusContent = '';
    let copiedMessage = false;
    let sharedMessage = false;
    let feedbackPopupMessage = null;
    let feedbackNotes = '';
    let popupElement;
    let popupAnchor;

    $: if (currentMessage && currentMessage.content !== streamedContent) {
        streamedContent = currentMessage.content;
    }

    $: if (currentStatusMessage) {
        console.debug('currentStatusMessage', currentStatusMessage);
        streamedStatusContent = currentStatusMessage.content;
    }

    // Add a new reactive statement to track loading state
    $: isStatusLoading = currentStatusMessage && currentStatusMessage.content !== streamedStatusContent;

    function handleSubmit(event) {
        dispatch('newMessage', {
            role: 'user',
            content: event.detail.query
        });
    }

    function formatStatusMessage(content) {
        return content.split('\n');
    }

    function handleStop() {
        dispatch('stopMessageFlow');
    }

    function resetAllCitations() {
        if (typeof document !== 'undefined') {
            const allCitations = document.querySelectorAll('.citation-link');
            allCitations.forEach(citation => {
                citation.classList.remove('selected');
            });
        }
        selectedCitation = null;
    }

    function resetSelectedCitation() {
        if (selectedCitation) {
            selectedCitation.classList.remove('selected');
            selectedCitation = null;
        }
    }

    function insertClickableCitations(text_formatted, messageType) {
        if (messageType === 'status') {
            return text_formatted.split('\n').map(line => `<p>${line}</p>`).join('');
        }

        // Use a regex to find and replace spans with citation links
        const citationRegex = /<span class="citation-link" data-document-ids="([^"]+)">(.*?)<\/span>/g;
        const formattedText = text_formatted.replace(citationRegex, (match, documentIds, citationText) => {
            let formattedCitationText = citationText
                .trim()
                .replace(/[^a-zA-ZÀ-ÿ0-9\s$€%\-.,]/g, '') // Remove unwanted characters but keep letters with accents, dots and commas for now
                .replace(/[.,]/g, function(match, offset, string) {
                    // Check if the dot or comma is between digits
                    if (/\d/.test(string[offset - 1]) && /\d/.test(string[offset + 1])) {
                        return match; // Keep it
                    } else {
                        return ''; // Remove it
                    }
                })
                .trim();

            return `<a class="citation-link" onclick="handleCitationClick(event, ${documentIds}, '${formattedCitationText}')">${citationText}</a>`;
        });

        // Replace "Bron Gids" with a link to bron.live/gids
        const guideLinkRegex = /Bron Gids/g;
        const formattedWithGuideLink = formattedText.replace(guideLinkRegex, '<a class="external-link" href="https://site.bron.live/gids" target="_blank" rel="noopener noreferrer"><span>Bron Gids</span><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" class="s-64usSJ3OYh2K"></path><path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"></path></svg></a>');
        return formattedWithGuideLink;
    }

    function handleCitationClick(event, documentIds, citationText) {

        resetAllCitations();
        if (selectedCitation) {
            selectedCitation.classList.remove('selected');
        }
        dispatch('citationClick', { documentIds, citationText });
        selectedCitation = event.target;
        selectedCitation.classList.add('selected');
    }

    function getWaitingIcon() {
        return `
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-500 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
        `;
    }

    if (typeof window !== 'undefined') {
        window.handleCitationClick = handleCitationClick;
        window.resetSelectedCitation = resetSelectedCitation;
        window.resetAllCitations = resetAllCitations;
    }

    let chatContainer;

    function handleClickOutside(event) {
        if (popupElement && !popupElement.contains(event.target) && 
            popupAnchor && !popupAnchor.contains(event.target)) {
            closeFeedbackPopup();
        }
    }

    onMount(() => {
        scrollToBottom();
        
        // Add click outside listener
        document.addEventListener('click', handleClickOutside);
        
        const resizeObserver = new ResizeObserver(() => {
            if (feedbackPopupMessage) {
                updatePopupPosition();
            }
        });
        
        resizeObserver.observe(document.body);
        
        return () => {
            resizeObserver.disconnect();
            // Remove click outside listener
            document.removeEventListener('click', handleClickOutside);
        };
    });

    afterUpdate(() => {
        if (autoScroll && (currentMessage || messages[messages.length - 1]?.role === 'user')) {
            scrollToBottom();
        }
    });

    function scrollToBottom() {
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }

    // Add a new reactive variable for the notification
    let showNotification = false;
    let notificationMessage = '';

    // Function to show the notification
    function showClipboardNotification(message) {
        notificationMessage = message;
        showNotification = true;
        setTimeout(() => showNotification = false, 2000);
    }

    // Add new state variables for the copy popup
    let copyPopupMessage = null;
    let copyPopupAnchor;

    // Modify the copyToClipboard function
    function copyToClipboard(message, event) {
        if (navigator.clipboard) {
            const strippedText = message.content.replace(/<[^>]*>/g, '');
            navigator.clipboard.writeText(strippedText).then(() => {
                copyPopupAnchor = event.currentTarget;
                showCopyPopup(message.id, 'Tekst gekopieerd naar klembord');
                console.debug(`Text ${strippedText} copied to clipboard`);
            }).catch(err => {
                console.error('Could not copy text: ', err);
            });
        }
    }

    // Modify the shareLinkToClipboard function
    function shareLinkToClipboard(message, event) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(window.location.href).then(() => {
                copyPopupAnchor = event.currentTarget;
                showCopyPopup(message.id, 'Deelbare link gekopieerd naar klembord');
                console.debug(`Shared link ${window.location.href} copied to clipboard`);
            }).catch(err => {
                console.error('Could not copy text: ', err);
            });
        }
    }

    // Add messageId parameter to showCopyPopup function
    async function showCopyPopup(messageId, message) {
        // Close any existing popups first
        closeCopyPopup();
        closeFeedbackPopup();
        
        await tick();
        
        // Store both the message and its ID
        copyPopupMessage = { id: messageId, text: message };
        
        await tick();
        
        if (popupElement && copyPopupAnchor) {
            updateCopyPopupPosition();
        }
        
        // Auto-close after 2 seconds
        setTimeout(() => closeCopyPopup(), 2000);
    }

    // Add function to close copy popup
    function closeCopyPopup() {
        if (popupElement) {
            Object.assign(popupElement.style, {
                left: '',
                top: '',
                position: ''
            });
        }
        copyPopupMessage = null;
    }

    // Add function to update copy popup position
    async function updateCopyPopupPosition() {
        if (!popupElement || !copyPopupAnchor) return;
        
        const { x, y } = await computePosition(copyPopupAnchor, popupElement, {
            placement: 'top-start',
            middleware: [
                offset({ mainAxis: 30, crossAxis: 40 }), // Adjusted mainAxis to 30 to position 30px above
                flip({
                    fallbackPlacements: ['bottom-start'],
                    padding: 8
                }),
                shift({
                    padding: 8
                })
            ],
        });

        Object.assign(popupElement.style, {
            left: `${x}px`,
            top: `${y}px`,
            position: 'absolute',
            width: 'auto',
            whiteSpace: 'nowrap'
        });
    }

    async function submitFeedbackType(messageId, feedbackType) {
        try {
            const response = await fetch(`${API_BASE_URL}/feedback/messages/type/${messageId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    feedback_type: feedbackType,
                })
            });

            if (!response.ok) {
                const error = await response.json();
                console.error('Feedback submission error:', error);
                throw new Error(error.detail || 'Failed to submit feedback');
            }

            const feedback = await response.json();

            // Update the messages array by mapping over each message
            messages = messages.map(msg => {
                // If this is the message that received feedback
                if (msg.id === messageId) {
                    // Show the feedback popup for this message
                    showFeedbackPopup(msg);
                    // Return a new message object with the feedback data merged in
                    return { ...msg, feedback };
                }
                // Return unchanged messages as-is
                return msg;
            });
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    }

    async function submitFeedbackNotes(messageId, notes = '') {
        try {
            const response = await fetch(`${API_BASE_URL}/feedback/messages/notes/${messageId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    notes: notes || ''
                })
            });

            if (!response.ok) {
                const error = await response.json();
                console.error('Feedback submission error:', error);
                throw new Error(error.detail || 'Failed to submit feedback');
            }

            messages = messages.map(msg => {
                if (msg.id === messageId) {
                    return {
                        ...msg,
                        feedback: {
                            ...msg.feedback,
                            notes: notes
                        }
                    };
                }
                return msg;
            });

            closeFeedbackPopup();            

        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    }

    async function showFeedbackPopup(message) {
        // If clicking the same message's feedback, just close it
        if (feedbackPopupMessage?.id === message.id) {
            closeFeedbackPopup();
            return;
        }
        
        // Close any existing popup first
        closeFeedbackPopup();
        
        // Wait a tick to ensure previous popup is closed
        await tick();
        
        // Now open the new popup
        feedbackPopupMessage = message;
        feedbackNotes = '';
        
        // Wait another tick for the new popup to render
        await tick();
        
        if (popupElement && popupAnchor) {
            updatePopupPosition();
        }
    }

    function closeFeedbackPopup() {
        if (popupElement) {
            // Clear the positioning styles when closing
            Object.assign(popupElement.style, {
                left: '',
                top: '',
                position: ''
            });
        }
        feedbackPopupMessage = null;
        feedbackNotes = '';
    }

    async function updatePopupPosition() {
        if (!popupElement || !popupAnchor) return;
        
        const { x, y } = await computePosition(popupAnchor, popupElement, {
            placement: 'top-start',
            middleware: [
                offset({ mainAxis: 8, crossAxis: -8 }), // Adjust offset to align better with the button
                flip({
                    fallbackPlacements: ['bottom-start'],
                    padding: 8
                }),
                shift({
                    padding: 8
                })
            ],
        });

        Object.assign(popupElement.style, {
            left: `${x}px`,
            top: `${y}px`,
            position: 'absolute',
            width: '20rem',
            maxWidth: 'calc(100vw - 2rem)'
        });
    }

    // Add these new state variables at the top of the script
    let expandedStatusMessages = new Set();

    // Add this new function
    function toggleStatusMessage(messageId) {
        if (expandedStatusMessages.has(messageId)) {
            expandedStatusMessages.delete(messageId);
        } else {
            expandedStatusMessages.add(messageId);
        }
        expandedStatusMessages = expandedStatusMessages; // trigger reactivity
    }

</script>
<style lang="postcss">
    :global(.citation-link) {
        @apply bg-gray-200 text-blue-900 px-0.5 py-0.5 -mx-0.5 inline rounded cursor-pointer transition-colors duration-200 whitespace-normal text-left relative;
    }

    :global(.external-link) {
        @apply inline-flex items-center bg-gray-200 text-blue-900 px-0.5 py-0.5 -mx-0.5 inline rounded cursor-pointer transition-colors duration-200 whitespace-normal text-left relative;
    }

    :global(.citation-link:hover) {
        @apply bg-blue-200;
    }

    :global(.citation-link.selected) {
        @apply bg-yellow-200;
    }

    :global(.citation-link.selected:hover) {
        @apply bg-yellow-300;
    }

    :global(.message-content h1) {
        @apply text-xl font-bold mb-4 mt-6;
    }

    :global(.message-content h2) {
        @apply text-lg font-bold mb-3 mt-5;
    }

    :global(.message-content h3) {
        @apply text-base font-bold mb-2 mt-4;
    }

    :global(.message-content p) {
        @apply mb-4;
    }

    :global(.message-content p:last-child) {
        @apply mb-0;
    }

    :global(.message-content ul, .message-content ol) {
        @apply mb-4 pl-8;
    }

    :global(.message-content ul) {
        @apply list-disc;
    }

    :global(.message-content ol) {
        @apply list-decimal;
    }

    :global(.message-content li) {
        @apply mb-2;
    }

    :global(.message-content blockquote) {
        @apply border-l-4 border-gray-300 pl-4 italic my-4;
    }

    :global(.message-content code) {
        @apply rounded px-1 py-0.5 font-mono text-sm;
    }

    :global(.message-content pre) {
        @apply rounded p-4 overflow-x-auto mb-4;
    }

    :global(.message-content pre code) {
        @apply bg-transparent p-0;
    }

    :global(.message-content.status p) {
        @apply mb-1;
        transition: all 200ms ease-in-out;
    }

    :global(.message-content.status p:last-child) {
        @apply mb-0;
    }

    .chat-container {
        @apply flex flex-col h-full;
    }

    .messages-container {
        @apply flex-1 overflow-y-auto p-4 space-y-4;
    }

    :global(.chat-wrapper) {
        @apply flex flex-col h-full transition-all duration-300 ease-in-out;
    }

    .feedback-popup {
        @apply bg-white rounded-lg shadow-lg p-4;
        width: 20rem;
        max-width: calc(100vw - 2rem);
    }

    .notification {
        @apply fixed bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300;
        opacity: 0;
    }

    .notification.show {
        opacity: 1;
    }

    .copy-popup {
        @apply bg-white rounded-lg shadow-lg p-2;
        min-width: 12rem;
    }

</style>

<div class="flex flex-col h-full transition-all duration-300 ease-in-out">
    <div class="flex flex-col h-full">
        {#if messages && messages.length > 0}
            <div bind:this={chatContainer} class="flex-1 overflow-y-auto p-4 space-y-4">

                {#each messages as message}
                    <div class="flex {message.role === 'user' ? 'justify-end' : 'justify-start'}">
                        <div class="message-content p-3 rounded-lg relative {message.role === 'user' ? 'bg-blue-500 text-white' : ''} {message.role === 'system' ? 'transition-all duration-200 ease-in-out cursor-pointer w-full bg-gray-200 text-gray-600 hover:bg-gray-200' : ''}  {message.role === 'assistant' ? 'bg-gray-200 text-gray-800' : ''} ">
                            {#if message.role === 'user'}
                                <p>{message.content}</p>
                            {:else if message.role === 'system'}
                                <div 
                                    class="cursor-pointer flex justify-between items-start"
                                    on:click={() => toggleStatusMessage(message.id)}
                                >
                                    <ul class="!list-none pl-4 flex-1 !mb-0 !pl-2">
                                        {#if expandedStatusMessages.has(message.id)}
                                            {#each formatStatusMessage(message.content) as line}
                                                <li transition:slide={{ duration: 500 }} class="!mb-0">{line}</li>
                                            {/each}
                                        {:else}
                                            <li class="!mb-0">{formatStatusMessage(message.content).pop()}</li>
                                        {/if}
                                    </ul>
                                    <svg 
                                        xmlns="http://www.w3.org/2000/svg" 
                                        class="h-5 w-5 transition-transform duration-200 ml-1 flex-shrink-0 rotate-90"
                                        viewBox="0 0 20 20" 
                                        fill="currentColor"
                                        class:-rotate-90={!expandedStatusMessages.has(message.id)}
                                    >
                                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                                    </svg>
                                </div>
                            {:else if message.role === 'assistant'}
                                {@html insertClickableCitations(message.content, message.type)}
                                        
                                <div class="flex items-center mt-4 relative">
                                    <div class="relative flex items-center">
                                        <button on:click={(event) => copyToClipboard(message, event)} class="ml-0 text-sm text-blue-800 hover:text-blue-900">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 7.5V6.108c0-1.135.845-2.098 1.976-2.192.373-.03.748-.057 1.123-.08M15.75 18H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08M15.75 18.75v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5A3.375 3.375 0 0 0 6.375 7.5H5.25m11.9-3.664A2.251 2.251 0 0 0 15 2.25h-1.5a2.251 2.251 0 0 0-2.15 1.586m5.8 0c.065.21.1.433.1.664v.75h-6V4.5c0-.231.035-.454.1-.664M6.75 7.5H4.875c-.621 0-1.125.504-1.125 1.125v12c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V16.5a9 9 0 0 0-9-9Z" />
                                            </svg>
                                        </button>

                                        <button on:click={(event) => shareLinkToClipboard(message, event)} class="ml-2 text-sm text-blue-800 hover:text-blue-900">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.251 2.251 0 0 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
                                            </svg>
                                        </button>

                                        {#if copyPopupMessage != null && copyPopupMessage.id === message.id}
                                            <div 
                                                bind:this={popupElement}
                                                class="copy-popup absolute -top-16 bg-white rounded-lg shadow-lg p-2 z-50 text-sm"
                                                on:click|stopPropagation
                                            >
                                                {copyPopupMessage.text}
                                            </div>
                                        {/if}
                                    </div>  

                                    <div class="relative">
                                        <div class="flex items-center">
                                            <button 
                                                class="ml-2 text-sm text-blue-800 hover:text-blue-900 cursor-pointer transition-colors duration-200 {message.feedback != null && message.feedback.feedback_type === 'positive' ? 'selected' : ''}"
                                                on:click={(event) => {
                                                    event.stopPropagation();
                                                    popupAnchor = event.currentTarget;
                                                    submitFeedbackType(message.id, 'positive');
                                                }}
                                            >
                                                {#if message.feedback != null && message.feedback.feedback_type === 'positive'}
                                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                                                        <path d="M7.493 18.5c-.425 0-.82-.236-.975-.632A7.48 7.48 0 0 1 6 15.125c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V2.75A.75.75 0 0 1 15 2a2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23h-.777ZM2.331 10.727a11.969 11.969 0 0 0-.831 4.398 12 12 0 0 0 .52 3.507C2.28 19.482 3.105 20 3.994 20H4.9c.445 0 .72-.498.523-.898a8.963 8.963 0 0 1-.924-3.977c0-1.708.476-3.305 1.302-4.666.245-.403-.028-.959-.5-.959H4.25c-.832 0-1.612.453-1.918 1.227Z" />
                                                    </svg>                                                                                                   
                                                {:else}
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                                        <path stroke-linecap="round" stroke-linejoin="round" d="M6.633 10.25c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V2.75a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282m0 0h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23H5.904m10.598-9.75H14.25M5.904 18.5c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 0 1-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 9.953 4.167 9.5 5 9.5h1.053c.472 0 .745.556.5.96a8.958 8.958 0 0 0-1.302 4.665c0 1.194.232 2.333.654 3.375Z" />
                                                    </svg>
                                                {/if}
                                            </button>
                                            <button 
                                                class="ml-2 text-sm text-blue-800 hover:text-blue-900 cursor-pointer transition-colors duration-200 {message.feedback != null && message.feedback.feedback_type === 'negative' ? 'selected' : ''}"
                                                on:click={(event) => {
                                                    event.stopPropagation();
                                                    popupAnchor = event.currentTarget;
                                                    submitFeedbackType(message.id, 'negative');
                                                }}
                                            >
                                                {#if message.feedback != null && message.feedback.feedback_type === 'negative'}
                                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                                                        <path d="M15.73 5.5h1.035A7.465 7.465 0 0 1 18 9.625a7.465 7.465 0 0 1-1.235 4.125h-.148c-.806 0-1.534.446-2.031 1.08a9.04 9.04 0 0 1-2.861 2.4c-.723.384-1.35.956-1.653 1.715a4.499 4.499 0 0 0-.322 1.672v.633A.75.75 0 0 1 9 22a2.25 2.25 0 0 1-2.25-2.25c0-1.152.26-2.243.723-3.218.266-.558-.107-1.282-.725-1.282H3.622c-1.026 0-1.945-.694-2.054-1.715A12.137 12.137 0 0 1 1.5 12.25c0-2.848.992-5.464 2.649-7.521C4.537 4.247 5.136 4 5.754 4H9.77a4.5 4.5 0 0 1 1.423.23l3.114 1.04a4.5 4.5 0 0 0 1.423.23ZM21.669 14.023c.536-1.362.831-2.845.831-4.398 0-1.22-.182-2.398-.52-3.507-.26-.85-1.084-1.368-1.973-1.368H19.1c-.445 0-.72.498-.523.898.591 1.2.924 2.55.924 3.977a8.958 8.958 0 0 1-1.302 4.666c-.245.403.028.959.5.959h1.053c.832 0 1.612-.453 1.918-1.227Z" />
                                                    </svg>
                                                {:else}                                                  
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                                        <path stroke-linecap="round" stroke-linejoin="round" d="M7.498 15.25H4.372c-1.026 0-1.945-.694-2.054-1.715a12.137 12.137 0 0 1-.068-1.285c0-2.848.992-5.464 2.649-7.521C5.287 4.247 5.886 4 6.504 4h4.016a4.5 4.5 0 0 1 1.423.23l3.114 1.04a4.5 4.5 0 0 0 1.423.23h1.294M7.498 15.25c.618 0 .991.724.725 1.282A7.471 7.471 0 0 0 7.5 19.75 2.25 2.25 0 0 0 9.75 22a.75.75 0 0 0 .75-.75v-.633c0-.573.11-1.14.322-1.672.304-.76.93-1.33 1.653-1.715a9.04 9.04 0 0 0 2.86-2.4c.498-.634 1.226-1.08 2.032-1.08h.384m-10.253 1.5H9.7m8.075-9.75c.01.05.027.1.05.148.593 1.2.925 2.55.925 3.977 0 1.487-.36 2.89-.999 4.125m.023-8.25c-.076-.365.183-.75.575-.75h.908c.889 0 1.713.518 1.972 1.368.339 1.11.521 2.287.521 3.507 0 1.553-.295 3.036-.831 4.398-.306.774-1.086 1.227-1.918 1.227h-1.053c-.472 0-.745-.556-.5-.96a8.95 8.95 0 0 0 .303-.54" />
                                                    </svg>
                                                {/if}
                                            </button>
                                            <span class="ml-2 text-sm text-gray-500">
                                                Wat vond je van dit antwoord?
                                            </span>
                                        </div>

                                        {#if feedbackPopupMessage != null && feedbackPopupMessage.id === message.id}
                                            <div 
                                                bind:this={popupElement}
                                                class="feedback-popup absolute bg-white rounded-lg shadow-lg p-4 z-50"
                                                style="min-width: 20rem;"
                                                on:click|stopPropagation
                                            >
                                                <div class="flex justify-between items-start mb-2">
                                                    <h4 class="text-sm sm:text-base font-semibold">Bedankt voor je feedback!</h4>
                                                    <button 
                                                        on:click={closeFeedbackPopup}
                                                        class="text-gray-500 hover:text-gray-700"
                                                    >
                                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                                                        </svg>
                                                    </button>
                                                </div>
                                                <p class="text-sm mb-2">
                                                    {#if message.feedback.feedback_type === 'positive'}
                                                        Wat vond je vooral goed aan dit antwoord?
                                                    {:else}
                                                        Wat zouden we kunnen verbeteren aan dit antwoord?
                                                    {/if}
                                                </p>
                                                <textarea
                                                    bind:value={feedbackNotes}
                                                    placeholder="Jouw toelichting (optioneel)"
                                                    class="w-full p-2 border rounded-md text-sm mb-2"
                                                    rows="3"
                                                ></textarea>
                                                <button 
                                                    class="bg-blue-500 text-white px-3 py-1 rounded-md text-sm hover:bg-blue-600 transition-colors duration-200"
                                                    on:click={() => submitFeedbackNotes(message.id, feedbackNotes)}
                                                >
                                                    Verstuur feedback
                                                </button>
                                            </div>
                                        {/if}
                                    </div>

                                </div>
                            {/if}
                        </div>
                    </div>
                {/each}
                
                {#if currentStatusMessage}
                    <div class="flex justify-start">
                        <div class="message-content p-3 rounded-lg status bg-gray-200 text-gray-900 w-full">
                            <div class="flex justify-between items-start">
                                {#if isLoading}
                                    <div class="flex items-center text-gray-600 pt-0.5">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 animate-spin">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                                        </svg>  
                                    </div>
                                {/if}
                                <ul class="!list-none pl-4 flex-1 !mb-0 !pl-2">
                                    {#each formatStatusMessage(streamedStatusContent) as line}
                                        <li class="{isLoading ? 'animate-pulse' : ''} !mb-0">{line}...</li>
                                    {/each}
                                </ul>
                            </div>
                        </div>
                    </div>
                {/if}

                {#if currentMessage}
                    <div class="flex justify-start">
                        <div class="message-content current-message p-3 rounded-lg bg-gray-200 text-gray-800">
                            {@html insertClickableCitations(streamedContent)}
                        </div>
                    </div>
                {/if}
            </div>
        {/if}
    </div>

    <!-- Notification popup -->
    {#if showNotification}
        <div class="notification show">
            {notificationMessage}
        </div>
    {/if}

</div>

