import React, { useEffect, useState } from "react";
import { HStack, Input, Button, Text } from "@chakra-ui/react";
import { IoIosMusicalNote } from "react-icons/io";
import { BsMusicPlayerFill } from "react-icons/bs";
import axios from "axios";
import "./App.css";

const App: React.FC = () => {
  const [actualSong, setActualSong] = useState<string | null>(null);
  const [spotifyUri, setSpotifyUri] = useState<string | null>(null);
  const [deviceId, setDeviceId] = useState<string | null>(null);
  const [player, setPlayer] = useState<any>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [guess, setGuess] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    // Get access token from backend
    axios.get("http://127.0.0.1:5000/get_token").then((response) => {
      setAccessToken(response.data.access_token);
    });

    // Fetch random song from backend
    axios
      .get("http://127.0.0.1:5000/api/random-song")
      .then((response) => {
        const { name, uri } = response.data;
        setActualSong(name);
        setSpotifyUri(uri); // Store the Spotify URI
      })
      .catch((error) => console.error("Error fetching song:", error));

    // Load Spotify Web Playback SDK
    window.onSpotifyWebPlaybackSDKReady = () => {
      const spotifyPlayer = new window.Spotify.Player({
        name: "Web Playback SDK",
        getOAuthToken: (cb) => cb(accessToken || ""),
        volume: 0.5,
      });

      setPlayer(spotifyPlayer);

      spotifyPlayer.addListener("ready", ({ device_id }) => {
        console.log("Ready with Device ID", device_id);
        setDeviceId(device_id);
      });

      spotifyPlayer.connect();
    };

    const script = document.createElement("script");
    script.src = "https://sdk.scdn.co/spotify-player.js";
    script.async = true;
    document.body.appendChild(script);

    return () => {
      if (player) player.disconnect();
    };
  }, [accessToken]);

  // Play the song on Spotify Player
  const playSong = () => {
    if (deviceId && spotifyUri) {
      axios
        .put(
          "https://api.spotify.com/v1/me/player/play",
          { uris: [spotifyUri] },
          { headers: { Authorization: `Bearer ${accessToken}` } }
        )
        .catch((error) => console.error("Error playing song:", error));
    }
  };

  // Check if guess is correct
  const checkGuess = () => {
    if (!actualSong) return;
    if (guess.toLowerCase().trim() === actualSong.toLowerCase().trim()) {
      setMessage("Correct! Well done!");
    } else {
      setMessage("Incorrect! Try again.");
    }
  };

  return (
    <div>
      <form>
        <div id="header">
          <HStack>
            <IoIosMusicalNote style={{ fontSize: "3rem" }} />
            <h1>Are we there yet?</h1>
          </HStack>
        </div>

        <div>
          <HStack>
            <BsMusicPlayerFill style={{ fontSize: "2rem" }} />
            <h2>Guess the song!</h2>
          </HStack>
        </div>

        <Button colorScheme="green" onClick={playSong}>
          Play on Spotify
        </Button>

        <div style={{ marginTop: "1rem" }}>
          <Input
            placeholder="Enter song title"
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
          />
          <Button colorScheme="blue" onClick={checkGuess} style={{ marginLeft: "1rem" }}>
            Submit Guess
          </Button>
        </div>

        {message && <Text fontSize="xl" style={{ marginTop: "1rem" }}>{message}</Text>}
      </form>
    </div>
  );
};

export default App;
