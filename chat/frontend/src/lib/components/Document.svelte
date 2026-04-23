<script>
    import { onMount, afterUpdate } from 'svelte';
    import { marked } from 'marked';
    import DOMPurify from 'dompurify';
    import { API_BASE_URL } from '$lib/config';
    import { showAllScores } from '$lib/stores/documentStore';

    export let doc;
    export let citationWords = [];

    let parsedContent = '';
    let contentElement;
    let parsedTitle = '';
    let titleElement;
    let publishedDateElement;
    let sourceElement;
    let locationNameElement;
    let typeElement;

    let feedbackPopupVisible = false;
    let feedbackNotes = '';

    $: feedbackType = doc.feedback?.feedback_type;

    function toggleScores() {
        showAllScores.update(value => !value);
    }

    onMount(() => {
        updateContent();
        updateTitle();
    });

    afterUpdate(() => {
        updateContent();
        updateTitle();
        updatePublishedDate();
        updateSource();
        updateLocationName();
        updateType();
    });


    function highlightCitationWords(text, citationWords) {        
        citationWords.forEach(word => {
            const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const regex = new RegExp(escapedWord, 'gi');
            text = text.replace(regex, match => `<mark>${match}</mark>`);
        });
        return text;
    }

    function updateTitle() {
        let title = doc.data.title || "Naamloos document";
        parsedTitle = highlightCitationWords(title, citationWords);

        if (titleElement) {
            titleElement.innerHTML = parsedTitle;
        }
    }

    function updateContent() {

        // Reset any previous extensions
        marked.setOptions({
            highlight: null,
            pedantic: false,
            gfm: true,
            breaks: false,
            sanitize: false,
            smartypants: false,
            xhtml: false
        });

        // Add extension to handle code blocks and spans
        marked.use({
            extensions: [{
                name: 'code',
                renderer(token) {
                    return token.text;
                }
            }, {
                name: 'codespan',
                renderer(token) {
                    return token.text;
                }
            }]
        });

        let content = marked.parse(doc.data.content || '');
        content = highlightCitationWords(content, citationWords);
        parsedContent = DOMPurify.sanitize(content);
        
        if (contentElement) {
            contentElement.innerHTML = marked.parse(parsedContent);
        }
    }

    function updatePublishedDate() {        
        let formattadPublishedDate = formatDate(doc.data.published)
        let highlightedPublishedDate = highlightCitationWords(formattadPublishedDate, citationWords);
        let parsedHighlightedPublishedDate = DOMPurify.sanitize(highlightedPublishedDate);
        
        if (publishedDateElement) {
            publishedDateElement.innerHTML = parsedHighlightedPublishedDate;
        }        
    }

    function updateSource() {
        let formattedSource = formatSource(doc.data.source)
        let highlightedSource = highlightCitationWords(formattedSource, citationWords);
        let parsedHighlightedSource = DOMPurify.sanitize(highlightedSource);
        
        if (sourceElement) {
            sourceElement.innerHTML = parsedHighlightedSource;
        }
    }

    function updateLocationName() {
        let formattedLocationName = doc.data.location_name || 'Onbekend';
        let highlightedLocationName = highlightCitationWords(formattedLocationName, citationWords);
        let parsedHighlightedLocationName = DOMPurify.sanitize(highlightedLocationName);
        
        if (locationNameElement) {
            locationNameElement.innerHTML = parsedHighlightedLocationName;
        }
    }

    function updateType() {
        let formattedType = doc.data.type || 'Onbekend';
        let highlightedType = highlightCitationWords(formattedType, citationWords);
        let parsedHighlightedType = DOMPurify.sanitize(highlightedType);
        
        if (typeElement) {
            typeElement.innerHTML = parsedHighlightedType;
        }
    }

    function formatSource(source) {
        const human_readable_sources = {
            "openbesluitvorming": "Raadsstuk of bijlage",
            "poliflw": "Politiek nieuwsbericht",
            "openspending": "Begrotingsdata",
            "woogle": "Woo-verzoek",
            "obk": "Officiële bekendmaking",
            "cvdr": "Lokale wet- en regelgeving",
            "oor": "Rapport",
        }
        return human_readable_sources[source] || source;
    }

    function formatDate(dateString) {
        if (!dateString) return 'Onbekend';
        return new Date(dateString).toLocaleDateString('nl-NL', { day: '2-digit', month: '2-digit', year: 'numeric' });
    }

    async function submitFeedbackType(documentId, feedbackType) {
        try {
            const response = await fetch(`${API_BASE_URL}/feedback/documents/type/${documentId}`, {
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

            doc.feedback = {
                ...doc.feedback,
                feedback_type: feedbackType,
            }            
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    }

    async function submitFeedbackNotes(documentId, notes = '') {
        try {
            const response = await fetch(`${API_BASE_URL}/feedback/documents/notes/${documentId}`, {
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

            if (doc.feedback) {
                doc.feedback.notes = notes;
            }
            feedbackPopupVisible = false;
            feedbackNotes = '';

        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    }
</script>
<style lang="postcss">
    :global(mark) {
        @apply bg-yellow-200 px-0.5 py-0.5 -mx-0.5 inline rounded transition-colors duration-200 whitespace-normal ;
    }

    :global(.document-content h2) {
        @apply mt-3 font-medium;
    }

    :global(.document-content h2:first-child) {
        @apply mt-0;
    }
    :global(.document-content p) {
        @apply break-words mb-3;
    }

    :global(.document-content p:has(+ h2)) {
        @apply mb-0;
    }

    :global(.document-content p:last-child) {
        @apply mb-0;
    }

</style>

<div class="shadow rounded-lg p-4 border border-gray-200 bg-gray-50 {doc.feedback != null && doc.feedback.feedback_type === 'irrelevant' ? 'opacity-50' : ''}" data-doc-id="{doc.chunk_id}">
    <header class="mb-4">
        <h3 class="font-title text-black text-sm sm:text-base font-semibold !leading-snug {doc.feedback && doc.feedback.feedback_type === 'irrelevant' ? 'line-through': ''}" bind:this={titleElement}>
            <!-- Content will be inserted here by the updateTitle function -->
        </h3>
        <div class="flex flex-col sm:flex-row items-start sm:items-center text-gray-500 text-sm mt-1 flex-wrap space-y-2 sm:space-y-0">
            <div class="flex items-center mb-1 sm:mb-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                </svg>
                <time bind:this={publishedDateElement}>{formatDate(doc.data.published)}</time>
            </div>
            <span class="hidden sm:inline mx-2">•</span>
            <div class="flex items-center mb-1 sm:mb-0">
                <svg class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7.82141 2.35718C8.35378 2.35718 8.7857 2.7889 8.7857 3.32146V9.74602C8.01829 10.1759 7.49998 10.9956 7.49998 11.9378C7.49998 12.1969 7.5723 12.438 7.69887 12.6429H5.89284V11.0357C5.89284 10.5034 5.46092 10.0715 4.92855 10.0715C4.39619 10.0715 3.96427 10.5034 3.96427 11.0357V12.6429H2.0357C1.50313 12.6429 1.07141 12.211 1.07141 11.6786V3.32146C1.07141 2.7889 1.50313 2.35718 2.0357 2.35718H7.82141ZM2.35713 7.82146C2.35713 7.99825 2.50096 8.14289 2.67855 8.14289H3.32141C3.4982 8.14289 3.64284 7.99825 3.64284 7.82146V7.17861C3.64284 7.00182 3.4982 6.85718 3.32141 6.85718H2.67855C2.50096 6.85718 2.35713 7.00182 2.35713 7.17861V7.82146ZM4.60713 6.85718C4.43034 6.85718 4.2857 7.00182 4.2857 7.17861V7.82146C4.2857 7.99825 4.43034 8.14289 4.60713 8.14289H5.24998C5.42677 8.14289 5.57141 7.99825 5.57141 7.82146V7.17861C5.57141 7.00182 5.42677 6.85718 5.24998 6.85718H4.60713ZM6.21427 7.82146C6.21427 7.99825 6.35891 8.14289 6.5357 8.14289H7.17855C7.35534 8.14289 7.49998 7.99825 7.49998 7.82146V7.17861C7.49998 7.00182 7.35534 6.85718 7.17855 6.85718H6.5357C6.35891 6.85718 6.21427 7.00182 6.21427 7.17861V7.82146ZM2.67855 4.28575C2.50096 4.28575 2.35713 4.43039 2.35713 4.60718V5.25004C2.35713 5.42682 2.50096 5.57146 2.67855 5.57146H3.32141C3.4982 5.57146 3.64284 5.42682 3.64284 5.25004V4.60718C3.64284 4.43039 3.4982 4.28575 3.32141 4.28575H2.67855ZM4.2857 5.25004C4.2857 5.42682 4.43034 5.57146 4.60713 5.57146H5.24998C5.42677 5.57146 5.57141 5.42682 5.57141 5.25004V4.60718C5.57141 4.43039 5.42677 4.28575 5.24998 4.28575H4.60713C4.43034 4.28575 4.2857 4.43039 4.2857 4.60718V5.25004ZM6.5357 4.28575C6.35891 4.28575 6.21427 4.43039 6.21427 4.60718V5.25004C6.21427 5.42682 6.35891 5.57146 6.5357 5.57146H7.17855C7.35534 5.57146 7.49998 5.42682 7.49998 5.25004V4.60718C7.49998 4.43039 7.35534 4.28575 7.17855 4.28575H6.5357ZM12.6428 7.82146C12.6428 8.70941 11.9236 9.42861 11.0357 9.42861C10.1478 9.42861 9.42855 8.70941 9.42855 7.82146C9.42855 6.93352 10.1478 6.21432 11.0357 6.21432C11.9236 6.21432 12.6428 6.93352 12.6428 7.82146ZM8.14284 11.9418C8.14284 10.9092 8.98056 10.0715 10.0132 10.0715H12.0582C13.0908 10.0715 13.9286 10.9092 13.9286 11.9418C13.9286 12.3295 13.6152 12.6429 13.2274 12.6429H8.84396C8.45623 12.6429 8.14284 12.3295 8.14284 11.9418Z" fill="#858585"/>
                </svg>                                            
                <span bind:this={locationNameElement}>{doc.data.location_name || 'Onbekend'}</span>
            </div>
            <span class="hidden sm:inline mx-2">•</span>
            <div class="flex items-center mb-1 sm:mb-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                </svg>
                <time bind:this={typeElement}>{doc.data.type || 'Onbekend'}</time>
            </div>
            <span class="hidden sm:inline mx-2">•</span>
            <div class="flex items-center mb-1 sm:mb-0">
                <svg class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 9 11" fill="none" xmlns="http://www.w3.org/2000/svg" >
                    <path d="M9 1.96432V2.92861C9 3.81655 6.98504 4.53575 4.5 4.53575C2.01496 4.53575 0 3.81655 0 2.92861V1.96432C0 1.07678 2.01496 0.357178 4.5 0.357178C6.98504 0.357178 9 1.07678 9 1.96432ZM7.89911 4.67035C8.29888 4.52169 8.70067 4.33084 9 4.09579V6.14289C9 7.03084 6.98504 7.75004 4.5 7.75004C2.01496 7.75004 0 7.03084 0 6.14289V4.09579C0.299933 4.33084 0.683437 4.52169 1.1019 4.67035C2.0021 4.99178 3.20424 5.17861 4.5 5.17861C5.79576 5.17861 6.9971 4.99178 7.89911 4.67035ZM1.1019 7.88463C2.0021 8.20606 3.20424 8.39289 4.5 8.39289C5.79576 8.39289 6.9971 8.20606 7.89911 7.88463C8.29888 7.73597 8.70067 7.54513 9 7.31008V9.03575C9 9.9237 6.98504 10.6429 4.5 10.6429C2.01496 10.6429 0 9.9237 0 9.03575V7.31008C0.299933 7.54513 0.683437 7.73597 1.1019 7.88463Z" fill="#858585"/>
                </svg>                                        
                <span bind:this={sourceElement}>{formatSource(doc.data.source)}</span>       
            </div>
            <span class="hidden sm:inline mx-2 cursor-pointer hover:text-gray-700" on:click={toggleScores}>•</span>   
            {#if $showAllScores}
                <div class="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" clip-rule="evenodd" />
                    </svg>
                    {doc.score ? `${(doc.score * 100).toFixed(1)}%` : 'Onbekend'}
                </div>
                <span class="hidden sm:inline mx-2">•</span>   
                <div class="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" clip-rule="evenodd" />
                    </svg>
                    {doc.rerank_score ? `${(doc.rerank_score * 100).toFixed(1)}%` : 'Onbekend'}
                </div>
            {/if}
        </div>
    </header>
    
    <div class="document-content text-gray-600 text-sm break-words" bind:this={contentElement}>
        <!-- Content will be inserted here by the updateContent function -->
    </div>
    
    <div class="flex items-end mt-2 justify-between">
        <div class="flex items-end mt-1">
            {#if doc.id}
                <button 
                    class="text-sm text-blue-800 hover:text-blue-900 cursor-pointer transition-colors duration-200 {doc.feedback && doc.feedback.feedback_type === 'relevant' ? 'selected' : ''}"
                    on:click={() => {
                        submitFeedbackType(doc.id, 'relevant');
                    }}
                >
                    {#if doc.feedback != null && doc.feedback.feedback_type === 'relevant'}
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
                    class="ml-2 text-sm text-blue-800 hover:text-blue-900 cursor-pointer transition-colors duration-200 {doc.feedback && doc.feedback.feedback_type === 'irrelevant' ? 'selected' : ''}"
                    on:click={() => {
                        submitFeedbackType(doc.id, 'irrelevant');
                    }}
                >
                    {#if doc.feedback != null  && doc.feedback.feedback_type === 'irrelevant'}
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
                    Is dit document relevant?
                </span>
            {/if}
        </div>

        {#if feedbackPopupVisible}
            <div class="feedback-popup absolute bg-white rounded-lg shadow-lg p-4 z-50 mt-2">
                <div class="flex justify-between items-start mb-2">
                    <h4 class="text-sm sm:text-base font-semibold">Bedankt voor je feedback!</h4>
                    <button 
                        on:click={() => feedbackPopupVisible = false}
                        class="text-gray-500 hover:text-gray-700"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                    </button>
                </div>
                <p class="text-sm mb-2">
                    {#if feedbackType === 'relevant'}
                        Wat vond je vooral relevant aan dit document?
                    {:else}
                        Waarom vond je dit document niet relevant?
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
                    on:click={() => submitFeedbackNotes(doc.id, feedbackNotes)}
                >
                    Verstuur feedback
                </button>
            </div>
        {/if}

        <div class="flex mt-3">
            {#if doc.data.url}
                <a class="ml-auto border border-black text-black px-4 py-1 rounded-md flex items-center" 
                    href={doc.data.url} 
                    target="_blank" 
                    rel="noopener noreferrer">
                    <span>{doc.data.type || 'Onbekend'}</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                        <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
                    </svg>
                </a>
            {/if}
        </div>
    </div>
</div>
