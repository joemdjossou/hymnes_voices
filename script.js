// Global variables
let hymnesData = [];
let currentAudio = null;
let currentHymne = null;
let isPlaying = false;
let currentTime = 0;
let duration = 0;

// DOM elements
const hymnesGrid = document.getElementById('hymnesGrid');
const loadingIndicator = document.getElementById('loadingIndicator');
const noResults = document.getElementById('noResults');
const searchInput = document.getElementById('searchInput');
const sortSelect = document.getElementById('sortSelect');
const totalHymnes = document.getElementById('totalHymnes');
const totalChannels = document.getElementById('totalChannels');
const currentlyPlaying = document.getElementById('currentlyPlaying');
const playerModal = document.getElementById('playerModal');
const closeModal = document.getElementById('closeModal');
const modalTitle = document.getElementById('modalTitle');
const currentHymne = document.getElementById('currentHymne');
const channelCount = document.getElementById('channelCount');
const channelsList = document.getElementById('channelsList');
const globalPlayer = document.getElementById('globalPlayer');
const globalPlayBtn = document.getElementById('globalPlayBtn');
const globalStopBtn = document.getElementById('globalStopBtn');
const globalTrackName = document.getElementById('globalTrackName');
const globalProgress = document.getElementById('globalProgress');
const volumeSlider = document.getElementById('volumeSlider');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadHymnesData();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    searchInput.addEventListener('input', filterHymnes);
    sortSelect.addEventListener('change', sortHymnes);
    closeModal.addEventListener('click', closePlayerModal);
    globalPlayBtn.addEventListener('click', toggleGlobalPlayback);
    globalStopBtn.addEventListener('click', stopGlobalPlayback);
    volumeSlider.addEventListener('input', updateVolume);
    
    // Close modal when clicking outside
    playerModal.addEventListener('click', function(e) {
        if (e.target === playerModal) {
            closePlayerModal();
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.code === 'Space' && currentAudio) {
            e.preventDefault();
            toggleGlobalPlayback();
        }
        if (e.code === 'Escape') {
            closePlayerModal();
        }
    });
}

// Load hymnes data
async function loadHymnesData() {
    try {
        showLoading(true);
        
        // Try to load hymnes data from JSON file
        const response = await fetch('hymnes_data.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        hymnesData = await response.json();
        
        // Validate that we have data
        if (!hymnesData || !Array.isArray(hymnesData) || hymnesData.length === 0) {
            throw new Error('No hymnes data found in JSON file');
        }
        
        console.log(`Loaded ${hymnesData.length} hymnes from JSON file`);
        displayHymnes(hymnesData);
        updateStats();
        showLoading(false);
        
    } catch (error) {
        console.error('Error loading hymnes data:', error);
        console.log('Falling back to generated hymnes data...');
        
        // Fallback: generate hymnes data dynamically
        try {
            hymnesData = await generateFallbackHymnesData();
            displayHymnes(hymnesData);
            updateStats();
            showLoading(false);
            showError('Using fallback hymnes data. Some features may be limited.');
        } catch (fallbackError) {
            console.error('Fallback also failed:', fallbackError);
            showLoading(false);
            showError('Failed to load hymnes data. Please check the console for details.');
        }
    }
}

// Generate fallback hymnes data when JSON file is not available
async function generateFallbackHymnesData() {
    console.log('Generating fallback hymnes data...');
    const hymnes = [];
    
    // Generate hymnes from h1 to h654
    for (let i = 1; i <= 654; i++) {
        const hymneName = `h${i}`;
        // Simulate channel count (you can adjust this based on your actual data)
        const channelCount = Math.min(8, Math.max(1, Math.floor(Math.random() * 6) + 2));
        const channels = [];
        
        for (let j = 0; j < channelCount; j++) {
            channels.push({
                number: j,
                name: `Channel ${j.toString().padStart(2, '0')}`,
                filename: `channel_${j.toString().padStart(2, '0')}.mp3`,
                url: `output/${hymneName}/channel_${j.toString().padStart(2, '0')}.mp3`
            });
        }
        
        hymnes.push({
            name: hymneName,
            number: i,
            channels: channelCount,
            channelFiles: channels
        });
    }
    
    console.log(`Generated fallback data for ${hymnes.length} hymnes`);
    return hymnes;
}

// These functions are no longer needed as we load real data from JSON

// Display hymnes in the grid
function displayHymnes(hymnes) {
    hymnesGrid.innerHTML = '';
    
    if (hymnes.length === 0) {
        noResults.style.display = 'block';
        return;
    }
    
    noResults.style.display = 'none';
    
    hymnes.forEach(hymne => {
        const hymneCard = createHymneCard(hymne);
        hymnesGrid.appendChild(hymneCard);
    });
}

// Create hymne card element
function createHymneCard(hymne) {
    const card = document.createElement('div');
    card.className = 'hymne-card';
    card.onclick = () => openPlayerModal(hymne);
    
    const channelBadges = hymne.channelFiles.map(file => 
        `<span class="channel-badge">${file.name}</span>`
    ).join('');
    
    card.innerHTML = `
        <h3>Hymne ${hymne.name}</h3>
        <p>${hymne.channels} channel${hymne.channels !== 1 ? 's' : ''} available</p>
        <div class="channel-preview">
            ${channelBadges}
        </div>
        <button class="play-button">
            <i class="fas fa-play"></i> Play Channels
        </button>
    `;
    
    return card;
}

// Open player modal
function openPlayerModal(hymne) {
    currentHymne = hymne;
    modalTitle.textContent = `Hymne ${hymne.name} - Channel Player`;
    currentHymne.textContent = `Hymne ${hymne.name}`;
    channelCount.textContent = `${hymne.channels} channels available`;
    
    displayChannels(hymne.channelFiles);
    playerModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

// Close player modal
function closePlayerModal() {
    playerModal.style.display = 'none';
    document.body.style.overflow = 'auto';
    stopGlobalPlayback();
}

// Display channels in modal
function displayChannels(channels) {
    channelsList.innerHTML = '';
    
    channels.forEach(channel => {
        const channelItem = createChannelItem(channel);
        channelsList.appendChild(channelItem);
    });
}

// Create channel item element
function createChannelItem(channel) {
    const item = document.createElement('div');
    item.className = 'channel-item';
    item.onclick = () => playChannel(channel);
    
    item.innerHTML = `
        <div class="channel-info">
            <h4>${channel.name}</h4>
            <p>Click to play this channel</p>
        </div>
        <div class="channel-controls">
            <button class="channel-play-btn">
                <i class="fas fa-play"></i>
            </button>
        </div>
    `;
    
    return item;
}

// Play a specific channel
function playChannel(channel) {
    // Stop current audio if playing
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }
    
    // Create new audio element
    currentAudio = new Audio();
    const audioUrl = `output/${currentHymne.name}/${channel.filename}`;
    currentAudio.src = audioUrl;
    currentAudio.volume = volumeSlider.value / 100;
    
    console.log(`Attempting to play: ${audioUrl}`);
    
    // Update UI
    globalTrackName.textContent = `Hymne ${currentHymne.name} - ${channel.name}`;
    currentlyPlaying.textContent = `${currentHymne.name} - ${channel.name}`;
    
    // Update channel buttons
    updateChannelButtons(channel);
    
    // Show global player
    globalPlayer.classList.add('active');
    
    // Audio event listeners
    currentAudio.addEventListener('loadedmetadata', () => {
        duration = currentAudio.duration;
        console.log(`Audio loaded successfully: ${audioUrl}`);
    });
    
    currentAudio.addEventListener('timeupdate', updateProgress);
    
    currentAudio.addEventListener('ended', () => {
        isPlaying = false;
        updateGlobalPlayButton();
        updateChannelButtons();
    });
    
    currentAudio.addEventListener('error', (e) => {
        console.error('Audio error:', e);
        console.error('Failed to load audio file:', audioUrl);
        showError(`Failed to load audio file: ${channel.filename}`);
    });
    
    // Start playing
    currentAudio.play().then(() => {
        isPlaying = true;
        updateGlobalPlayButton();
        console.log(`Successfully started playing: ${audioUrl}`);
    }).catch(error => {
        console.error('Error playing audio:', error);
        console.error('Audio URL:', audioUrl);
        showError(`Error playing audio file: ${channel.filename}. Check console for details.`);
    });
}

// Update channel buttons
function updateChannelButtons(activeChannel = null) {
    const channelItems = channelsList.querySelectorAll('.channel-item');
    
    channelItems.forEach(item => {
        const button = item.querySelector('.channel-play-btn');
        const icon = button.querySelector('i');
        
        if (activeChannel && item.querySelector('h4').textContent === activeChannel.name) {
            item.classList.add('playing');
            icon.className = 'fas fa-pause';
        } else {
            item.classList.remove('playing');
            icon.className = 'fas fa-play';
        }
    });
}

// Toggle global playback
function toggleGlobalPlayback() {
    if (!currentAudio) return;
    
    if (isPlaying) {
        currentAudio.pause();
        isPlaying = false;
    } else {
        currentAudio.play().then(() => {
            isPlaying = true;
        }).catch(error => {
            console.error('Error resuming audio:', error);
        });
    }
    
    updateGlobalPlayButton();
}

// Stop global playback
function stopGlobalPlayback() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
    
    isPlaying = false;
    updateGlobalPlayButton();
    updateChannelButtons();
    
    globalPlayer.classList.remove('active');
    globalTrackName.textContent = 'No track selected';
    currentlyPlaying.textContent = 'None';
    globalProgress.style.width = '0%';
}

// Update global play button
function updateGlobalPlayButton() {
    const icon = globalPlayBtn.querySelector('i');
    icon.className = isPlaying ? 'fas fa-pause' : 'fas fa-play';
}

// Update progress bar
function updateProgress() {
    if (currentAudio && duration > 0) {
        const progress = (currentAudio.currentTime / duration) * 100;
        globalProgress.style.width = `${progress}%`;
    }
}

// Update volume
function updateVolume() {
    if (currentAudio) {
        currentAudio.volume = volumeSlider.value / 100;
    }
}

// Filter hymnes based on search
function filterHymnes() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    if (searchTerm === '') {
        displayHymnes(hymnesData);
        return;
    }
    
    const filtered = hymnesData.filter(hymne => 
        hymne.name.toLowerCase().includes(searchTerm) ||
        hymne.number.toString().includes(searchTerm)
    );
    
    displayHymnes(filtered);
}

// Sort hymnes
function sortHymnes() {
    const sortBy = sortSelect.value;
    
    let sorted = [...hymnesData];
    
    if (sortBy === 'name') {
        sorted.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'number') {
        sorted.sort((a, b) => a.number - b.number);
    }
    
    displayHymnes(sorted);
}

// Update statistics
function updateStats() {
    totalHymnes.textContent = hymnesData.length;
    
    const totalChannelsCount = hymnesData.reduce((sum, hymne) => sum + hymne.channels, 0);
    totalChannels.textContent = totalChannelsCount;
}

// Show/hide loading indicator
function showLoading(show) {
    loadingIndicator.style.display = show ? 'block' : 'none';
}

// Show error message
function showError(message) {
    // Create a simple error notification
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ff4757;
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1001;
        animation: slideIn 0.3s ease;
    `;
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Add CSS animation for error messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
