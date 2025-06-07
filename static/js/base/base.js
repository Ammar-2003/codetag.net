document.addEventListener('DOMContentLoaded', function () {
  // Elements
  const mobileMenuButton = document.getElementById('mobile-menu-button');
  const mobileMenu = document.getElementById('mobile-menu');
  const searchButton = document.getElementById('search-button');
  const searchModal = document.getElementById('search-modal');
  const overlay = searchModal.querySelector('[class*="bg-gray-900/50"]');
  const modalContent = searchModal.querySelector('.transform');
  const searchInput = document.getElementById('search-input');
  const resultsContainer = document.getElementById('search-results');
  
  // State
  let debounceTimer;
  let currentRequest = null; // To track ongoing fetch requests

  // Modal functions
  function showModal() {
    searchModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden'; // Prevent scrolling
    setTimeout(() => {
      overlay.classList.remove('opacity-0');
      modalContent.classList.remove('scale-95', 'opacity-0');
      modalContent.style.setProperty('--tw-translate-y', '0');
      searchInput.focus();
    }, 10);
  }

    function toggleMobileMenu() {
    mobileMenu.classList.toggle('hidden');
  }

  function hideModal() {
    overlay.classList.add('opacity-0');
    modalContent.classList.add('scale-95', 'opacity-0');
    modalContent.style.setProperty('--tw-translate-y', '-20px');
    setTimeout(() => {
      searchModal.classList.add('hidden');
      document.body.style.overflow = ''; // Re-enable scrolling
    }, 300);
  }

  // Search functions
  function highlightText(text, query) {
    if (!query || !text) return text || '';
    const terms = query.split(/\s+/).filter(term => term.length > 0);
    return terms.reduce((result, term) => {
      const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
      return result.replace(regex, '<span class="bg-yellow-100 text-gray-900">$1</span>');
    }, text);
  }

  function debounceSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const query = searchInput.value.trim();
      if (query.length > 2) {
        performSearch(query);
      } else {
        showEmptyState();
      }
    }, 300);
  }

  function performSearch(query) {
    // Abort previous request if it exists
    if (currentRequest) {
      currentRequest.abort();
    }
    
    showLoadingState();
    
    const controller = new AbortController();
    currentRequest = controller;
    
    fetch(`blog/search/?q=${encodeURIComponent(query)}`, {
      signal: controller.signal
    })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        currentRequest = null;
        if (data.results && data.results.length > 0) {
          showResults(data.results, query);
        } else {
          showNoResults();
        }
      })
      .catch(error => {
        if (error.name !== 'AbortError') {
          console.error('Search error:', error);
          showNoResults("Error loading results");
          currentRequest = null;
        }
      });
  }

  function showLoadingState() {
    resultsContainer.innerHTML = `
      <div class="flex items-center justify-center py-10">
        <div class="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-500"></div>
        <span class="ml-2 text-gray-500">Searching...</span>
      </div>
    `;
  }

  function showResults(results, query) {
    let resultsHTML = `
      <div class="px-4 pb-2 pt-3">
        <h3 class="text-xs font-semibold text-gray-500">${results.length} RESULTS</h3>
      </div>
      <div class="space-y-1" role="list">
    `;

    results.forEach(result => {
      resultsHTML += `
        <a href="${result.url}" class="group flex items-center px-4 py-3 hover:bg-gray-50" role="listitem">
          <div class="mr-3 flex h-8 w-8 items-center justify-center rounded bg-blue-50 text-blue-600">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-700 group-hover:text-gray-900">
              ${highlightText(result.title, query)}
            </p>
            ${result.excerpt ? `<p class="text-xs text-gray-500">${highlightText(result.excerpt, query)}</p>` : ''}
          </div>
        </a>
      `;
    });

    resultsHTML += `</div>`;
    resultsContainer.innerHTML = resultsHTML;
  }

  function showNoResults(message = "No results found") {
    resultsContainer.innerHTML = `
      <div class="flex flex-col items-center justify-center py-10 px-4 text-center">
        <svg class="h-10 w-10 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="mt-4 text-sm font-medium text-gray-900">${message}</h3>
        <p class="mt-1 text-sm text-gray-500">Try different keywords</p>
      </div>
    `;
  }

  function showEmptyState() {
    resultsContainer.innerHTML = `
      <div class="flex flex-col items-center justify-center py-10 px-4 text-center text-gray-500">
        <svg class="h-10 w-10 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-4.35-4.35M17 10a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <h3 class="text-base font-medium text-gray-900">Search posts</h3>
        <p class="text-sm">Type to search by title or content</p>
      </div>
    `;
  }

  // Event Listeners
  searchButton?.addEventListener('click', showModal);
  
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      hideModal();
    }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      showModal();
    }
  });

  overlay?.addEventListener('click', hideModal);
  
  searchInput?.addEventListener('input', debounceSearch);
  
  // Prevent form submission if it exists
  searchInput?.closest('form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (query.length > 2) {
      performSearch(query);
    }
  });
    // Mobile menu toggle
  if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', toggleMobileMenu);
  }
});
