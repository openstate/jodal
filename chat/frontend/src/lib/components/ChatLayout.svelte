<script>
    import { removeStopwords, nld } from 'stopword'
    import { onMount } from 'svelte';
    import Chat from './Chat.svelte';
    import Documents from './Documents.svelte';
    import { goto } from '$app/navigation';
    import { API_BASE_URL } from '$lib/config';
    import ChatInput from './ChatInput.svelte';
    import CloneSessionButton from './CloneSessionButton.svelte';
    import { sessionStore } from '$lib/stores/sessionStore';

    $: messages = $sessionStore.messages || [];
    $: documents = Array.isArray($sessionStore.documents) ? $sessionStore.documents : [];
    $: sessionId = $sessionStore.sessionId;
    $: sessionName = $sessionStore.sessionName;
    $: locations = $sessionStore.locations;

    let currentStatusMessage = null;
    let selectedDocuments = null;
    let currentMessage = null;
    let citationText = '';
    let citationWords = [];
    let streamedContent = '';
    let eventSource = null; // Store the EventSource instance  
    let autoScroll = true;
    let isLoading = false;
    let isDocumentsPanelOpen = false;
    let initialQuery = null;
    let replayQueue = [];
    let isReplaying = false;
    let selectedLocations = [];
    let selectedYearRange = [];

    function handleNewMessage(event) {
        addMessage(event.detail);
        if (event.detail.role === 'user') {
            autoScroll = true;
            sendMessage(event.detail);
        }
    }

    function handleNewDocuments(documents) {
        const newDocs = Array.isArray(documents) ? documents : [];
        sessionStore.update(store => ({
            ...store,
            documents: [...store.documents, ...newDocs].sort((a, b) => {
                const dateA = new Date(a.published);
                const dateB = new Date(b.published);
                return dateB - dateA;
            })
        }));
    }

    function handleCitationClick(event) {
        const documentIds = event.detail.documentIds;
        selectedDocuments = documents.filter(doc => documentIds.includes(doc.chunk_id));
        citationText = event.detail.citationText;        
        citationWords = removeStopwords(event.detail.citationText.split(' '), nld);
        autoScroll = false;
        isDocumentsPanelOpen = true;
    }

    function closeDocumentsPanel(event) {
        // If there's no documents panel, return early
        const documentsPanel = document.querySelector('.documents-panel');
        if (!documentsPanel) return;
        
        // Check if the click target is a citation link
        if (
            window.matchMedia('(min-width: 1024px)').matches ||
            event.target?.classList?.contains('citation-link') || 
            event.target?.parentElement?.classList?.contains('show-all-documents-btn')
        ) {
            return; // Don't close the panel if clicking on a citation
        }

        if (!documentsPanel.contains(event.target)) {
            isDocumentsPanelOpen = false;
        }
    }

    function handleCurrentStatusMessage(statusMessage) {
        currentStatusMessage = statusMessage;
    }
  
    function addMessage(message) {
        console.debug('Adding message:', message);
        sessionStore.update(store => ({
            ...store,
            messages: [...store.messages, message]
        }));
    }

    function updateCurrentMessage(message) {
        currentMessage = message;
    }
    
    function setSessionId(id) {
        sessionId = id;
        console.debug('Session ID set to:', sessionId);
        if (typeof window !== 'undefined') {
            try {
                goto(`/s/${sessionId}`, { replaceState: true });
                console.debug('URL updated successfully');
            } catch (error) {
                console.error('Error updating URL:', error);
            }
        } else {
            console.debug('Window object not available, skipping URL update');
        }
    }

    function handleStopMessageFlow() {
        if (eventSource) {
            eventSource.close();
            console.debug('EventSource connection closed by user');
            if (streamedContent) {
                addMessage({
                    role: 'assistant',
                    content: streamedContent
                });
            }
        }
        
        // Also stop message replay if active
        if (isReplaying) {
            isReplaying = false;
            replayQueue = [];
        }
        
        currentMessage = null;
        currentStatusMessage = null;
        streamedContent = '';
        autoScroll = false;
        isLoading = false;
    }

    function handleFollowUpQuestion(event) {
        console.debug('handleFollowUpQuestion', event);

        if (event.detail) {

            const urlSearchParams = event.detail.urlSearchParams;
            urlSearchParams.append('session_id', sessionId);
            handleQuery(urlSearchParams);
        }
    }

    function handleQuery(urlSearchParams) {
        console.debug('handleQuery', urlSearchParams);
        isLoading = true;
        addMessage({
            role: 'user',
            content: urlSearchParams.get('query'),
            filters: Object.fromEntries(urlSearchParams.entries())
        });

        try {
            // Start with basic query parameters
            const url = `${API_BASE_URL}/chat?${urlSearchParams.toString()}`;
            console.debug('Connecting to EventSource URL:', url);
            
            eventSource = new EventSource(url);
            
            eventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    handleStreamedResponse(data);
                } catch (error) {
                    console.error('Error parsing event data:', error);
                    isLoading = false;
                }
            };
            
            eventSource.onerror = (error) => {
                if (error.currentTarget.readyState === EventSource.CLOSED) {
                    console.debug('EventSource connection closed');
                } else if (error.currentTarget.readyState === EventSource.CONNECTING) {
                    console.debug('EventSource connection connecting');
                } else {
                    console.error('Unexpected EventSource error:', error, eventSource);
                    updateCurrentMessage({ 
                        role: 'assistant', 
                        content: 'An unexpected error occurred while processing your request.' 
                    });

                }
                isLoading = false;
                eventSource.close();
            };
            
            eventSource.onopen = () => {
                console.debug('EventSource connection opened');
            };
            
            eventSource.addEventListener('close', () => {
                console.debug('EventSource connection closed by server');
                eventSource.close();
                isLoading = false;
            });
        } catch (error) {
            console.error('Error sending message:', error);
            updateCurrentMessage({ 
                role: 'assistant', 
                content: 'An error occurred while processing your request.' 
            });
            isLoading = false;
        }
    }

    function handleStreamedResponse(data) {
        switch (data.type) {
            case 'session':
                console.debug('Received session event:', data);
                setSessionId(data.session_id);
                break;
            case 'status':
                handleCurrentStatusMessage({
                    role: data.role,
                    content: data.content,
                    type: data.type
                });
                break;
            case 'documents':
                if (Array.isArray(data.documents)) {
                    handleNewDocuments(data.documents);

                    if (window.matchMedia('(min-width: 1024px)').matches) {
                        isDocumentsPanelOpen = true;
                    }
                } 
                break;
            case 'partial':
                streamedContent += data.content;
                currentMessage = {
                    role: data.role,
                    content: streamedContent,
                    content_original: streamedContent
                };
                break;
            case 'citation':
                autoScroll = false;
                currentMessage = {
                    role: data.role,
                    content: data.content,
                    content_original: data.content_original,
                    citations: data.citations
                };
                break;
            case 'full':
                if (data.session?.messages?.length === 0) {
                    break;
                }

                // Get documents from the last message
                const messages = data.session.messages;
                const lastMessage = messages[messages.length - 1];
                const newDocuments = lastMessage?.documents || [];

                // Update session store with messages
                sessionStore.update(store => ({
                    ...store,
                    messages: messages
                        .map(msg => ({
                            id: msg.id,
                            role: msg.role,
                            type: msg.message_type,
                            sequence: msg.sequence,
                            content: msg.message_type === 'user_message' || msg.message_type === 'status' ? msg.content : msg.formatted_content,
                            content_original: msg.content,
                            feedback: msg.feedback,
                            citations: msg.citations
                        })),
                    sessionName: data.session.name
                }));

                currentMessage = null;
                currentStatusMessage = null;
                streamedContent = '';
                isLoading = false;

                // Update document IDs if new documents are present
                if (newDocuments.length > 0) {
                    addDatabaseIdsToDocuments(newDocuments);
                }
                break;
            case 'end':   
                console.debug('Received end event');
                isLoading = false;
                currentMessage = null;
                break;
            case 'error':
                console.error('Received error event:', data.content);
                handleCurrentStatusMessage({ 
                    role: 'system',
                    message_type: 'status',
                    content: `Er ging iets mis bij het versturen van je vraag. Probeer het opnieuw.` 
                });
                isLoading = false;
                currentMessage = null;
                break;
        }
    }

    function updateDocumentsFromFullSession(messages) {
        if (messages?.length > 0) {
            const lastMessage = messages[messages.length - 1];
            if (lastMessage.documents) {
                addDatabaseIdsToDocuments(lastMessage.documents);
            }
        }
    }

    function addDatabaseIdsToDocuments(newDocuments) {
        console.debug('Existing documents:', $sessionStore.documents);
        console.debug('Adding database IDs to documents:', newDocuments);
        
        // Update documents in the store
        sessionStore.update(store => {
            const updatedDocs = store.documents.map(existingDoc => {
                const matchingNewDoc = newDocuments.find(newDoc => newDoc.chunk_id === existingDoc.chunk_id);
                if (matchingNewDoc && matchingNewDoc.id) {
                    return {
                        ...existingDoc,
                        id: matchingNewDoc.id
                    };
                }
                return existingDoc;
            });
            
            return {
                ...store,
                documents: updatedDocs
            };
        });
    }

    function handleShowAllDocuments() {
        selectedDocuments = null;
        citationText = '';
        citationWords = [];
        window.resetAllCitations();
        autoScroll = true;
    }

    function openDocumentsPanel() {
        if (document.visibilityState === 'visible' && 
            documents.length > 0 && 
            window.matchMedia('(min-width: 1024px)').matches) {
            isDocumentsPanelOpen = true;
        }
    }

    async function handleMessageReplay(event) {
        if (event.data?.type === 'REPLAY_MESSAGES' && event.origin === window.location.origin) {
            replayQueue = event.data.messages;
            if (!isReplaying) {
                isReplaying = true;
                await replayNextMessage();
            }
        }
    }
    
    async function replayNextMessage() {
        if (replayQueue.length === 0) {
            isReplaying = false;
            return;
        }
        
        // Don't continue if replay was stopped
        if (!isReplaying) {
            replayQueue = [];
            return;
        }
        
        const nextMessage = replayQueue.shift();
        
        // Wait a moment before sending the next message
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Simulate the user sending a message
        handleQuery({
            detail: {
                query: nextMessage.content,
                searchFilters: nextMessage.filters
            }
        });
        
        // Wait for the response to complete before sending the next message
        const checkResponse = setInterval(() => {
            if (!isLoading && isReplaying) {
                clearInterval(checkResponse);
                replayNextMessage();
            } else if (!isReplaying) {
                clearInterval(checkResponse);
            }
        }, 500);
    }

    function handleInitialFilters() {
        const lastUserMessage = messages.findLast(m => m.role === 'user');
        if (lastUserMessage?.search_filters) {
            if (lastUserMessage.search_filters.locations) {
                selectedLocations = lastUserMessage.search_filters.locations;
            }
            
            if (lastUserMessage.search_filters.date_range) {
                const [startDate, endDate] = lastUserMessage.search_filters.date_range;

                // Parse dates to get years
                if (startDate && endDate) {
                    selectedYearRange = [
                        parseInt(startDate.split('-')[0]),
                        parseInt(endDate.split('-')[0])
                    ];
                }
                console.debug('handleInitialFilter selectedYearRange', selectedYearRange);
            }
        }
    }

    onMount(() => {
        if (sessionId) {
            openDocumentsPanel();
        }
        handleInitialFilters();
        
        // Listen for initial query from the home page
        const handleInitialQuery = (event) => {
            console.debug('handleInitialQuery', event);
            if (event.detail) {
                // Extract locations and year range from URL params
                const params = event.detail.urlSearchParams;
                const location_ids = params.getAll('locations');
                const startDate = params.get('start_date');
                const endDate = params.get('end_date');

                console.debug('handleInitialQuery locations', location_ids);
                console.debug('handleInitialQuery selectedLocations', event.detail.selectedLocations);
                console.debug('handleInitialQuery startDate', startDate);
                console.debug('handleInitialQuery endDate', endDate);

                // Parse dates to get years
                if (startDate && endDate) {
                    selectedYearRange = [
                        parseInt(startDate.split('-')[0]),
                        parseInt(endDate.split('-')[0])
                    ];
                    console.debug('handleInitialQuery selectedYearRange', selectedYearRange);
                }

                // Convert locations to the expected format
                if (event.detail.selectedLocations.length > 0) {
                    selectedLocations = event.detail.selectedLocations;
                }

                handleQuery(event.detail.urlSearchParams);
            }
        };

        window.addEventListener('initialQuery', handleInitialQuery);
        document.addEventListener('click', closeDocumentsPanel);
        document.addEventListener('visibilitychange', openDocumentsPanel);
        window.addEventListener('message', handleMessageReplay);

        return () => {
            window.removeEventListener('initialQuery', handleInitialQuery);
            document.removeEventListener('click', closeDocumentsPanel);
            document.removeEventListener('visibilitychange', openDocumentsPanel);
            window.removeEventListener('message', handleMessageReplay);
        };
    });
</script>

<svelte:head>
    <title>{sessionName}</title>
</svelte:head>

<div class="flex flex-col lg:flex-row min-h-screen {messages.length === 0 ? '' : 'pt-28 sm:pt-20' } bg-gray-100 justify-center items-center overflow-x-hidden">
    <!-- Chat Panel Container -->
    <div class="max-w-[768px] {messages.length === 0 ? '' : 'h-[93vh]'} lg:px-4 transition-all duration-300 ease-in-out w-full
            {isDocumentsPanelOpen ? 'lg:-translate-x-[calc(50%)] lg:w-1/2' : 'translate-x-0'}">
        <div class="order-2 lg:order-1 h-full flex flex-col transition-all duration-300 pt-4 sm:pt-8 md:pt-5">
            <Chat 
                {currentMessage} 
                {currentStatusMessage} 
                {autoScroll}
                isLoading={isLoading}
                on:citationClick={handleCitationClick} 
            />
            <div class="mt-4 px-4 pb-4 sm:pb-6">
                <ChatInput
                    {isLoading}
                    locations={locations}
                    initialLocations={selectedLocations}
                    initialYearRange={selectedYearRange}
                    on:submit={handleFollowUpQuestion}
                    on:stop={handleStopMessageFlow}
                />
            </div>
        </div>
    </div>

    <!-- Documents Panel -->
    {#if documents.length > 0}
        <div class="documents-panel fixed lg:block bottom-[71px] lg:right-0 lg:top-16 lg:bottom-0 h-[calc(100vh-8rem)] lg:h-[90vh] w-full lg:w-1/2 bg-gray-100 transform transition-transform duration-300
            {isDocumentsPanelOpen ? 'translate-x-0' : 'translate-x-full'}">
            <div class="h-full">
                <Documents 
                    {selectedDocuments}
                    {citationText}
                    {citationWords}
                    {isDocumentsPanelOpen}
                    on:showAllDocuments={handleShowAllDocuments}
                    on:togglePanel={() => isDocumentsPanelOpen = !isDocumentsPanelOpen}
                />
            </div>
        </div>
    {/if}
</div>

<!-- {#if messages.length > 0 && !isReplaying && !isLoading}
    <div class="fixed top-12 lg:top-16 left-2 lg:left-8 z-50">
        <CloneSessionButton {sessionId} />
    </div>
{/if} -->

<style lang="postcss">    
    @tailwind base;
    @tailwind components;
    @tailwind utilities;

    :global(html, body) {
        @apply h-full;
    }

    /* Make both panels scrollable */
    /* main > div {
        @apply overflow-y-auto;
    } */
</style>
