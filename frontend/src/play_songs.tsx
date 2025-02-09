// index.ts
interface Song {
    name: string;
    artist: string;
    album: string;
    release_date: string;
    image: string;
    preview: string | null;
}



// Function to fetch a random song from the backend
async function fetchRandomSong(): Promise<Song | null> {
    try {
        const response = await fetch("/api/random-song"); // Adjust the endpoint to match your backend
        if (!response.ok) throw new Error("Failed to fetch song");

        const song: Song = await response.json();
        return song;
    } catch (error) {
        console.error("Error fetching song:", error);
        return null;
    }
}

// Function to play the song preview
async function playRandomSong(): Promise<void> {
    const song = await fetchRandomSong();
    if (!song) {
        alert("Failed to get a random song. Try again.");
        return;
    }

    const songTitle = document.getElementById("songTitle") as HTMLParagraphElement;
    const songArtist = document.getElementById("songArtist") as HTMLParagraphElement;
    const albumCover = document.getElementById("albumCover") as HTMLImageElement;
    const audioPlayer = document.getElementById("audioPlayer") as HTMLAudioElement;

    songTitle.innerText = `${song.name}`;
    songArtist.innerText = `${song.artist} | ${song.album} (${song.release_date})`;
    albumCover.src = song.image;
    albumCover.style.display = "block"; // Show image

    if (song.preview) {
        audioPlayer.src = song.preview;
        audioPlayer.play();
    } else {
        alert("No preview available for this song. Try again.");
    }
}

// Event Listener for Button
document.addEventListener("DOMContentLoaded", () => {
    const playButton = document.getElementById("playButton") as HTMLButtonElement;
    playButton.addEventListener("click", playRandomSong);
});