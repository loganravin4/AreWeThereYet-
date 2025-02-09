// import React, { useEffect, useState } from "react";
// import { HStack } from "@chakra-ui/react";
// import { IoIosMusicalNote } from "react-icons/io";
// import { BsMusicPlayerFill } from "react-icons/bs";
// import axios from "axios";
// import SongPlayer from "./play_song";
// import './App.css';

// const App: React.FC = () => {
//   const [actualSong, setActualSong] = useState<string | null>(null);
//   const [guessResult, setGuessResult] = useState<string | null>(null);
//   const [songPreviewUrl, setSongPreviewUrl] = useState<string | null>(null); // State to store preview URL
//   const [playSong, setPlaySong] = useState<boolean>(false); 
//   //const [song, setSong] = useState<SongData | null>(null);
//   const [audio, setAudio] = useState<HTMLAudioElement | null>(null);
//   const [isPlaying, setIsPlaying] = useState(false);
//   useEffect(() => {
//     axios.get("http://127.0.0.1:5000/api/random-song")
//       .then(response => {
//         const { name, preview } = response.data;
//         setActualSong(response.data.name);
//         console.log(`Correct song: ${response.data.name}`);
//         setActualSong(name);
//         setSongPreviewUrl(preview); // Store the preview URL
//       })
//       .catch(error => console.error("Error fetching song:", error));
//   }, []);

//   const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
//     // Prevent the browser from reloading the page
//     e.preventDefault();

//     // Read the form data
//     const form = e.currentTarget;
//     const formData = new FormData(form);
//     const userGuess = formData.get("userInput") as string;

//     if (!actualSong) {
//       console.error("No actual song fetched yet.");
//       return;
//     }

//     try {
//       const response = await axios.post("http://127.0.0.1:5000/api/validate-song", {
//         user_input: userGuess,
//         correct_song: actualSong
//       });

//       // Display match result
//       console.log("API Response:", response.data);
//       if (response.data.is_match) {
//         console.log(userGuess);
//         console.log(actualSong);
//         setGuessResult("Correct! You guessed the song!");

//       } else {
//         console.log(userGuess);
//         console.log(actualSong);
//         setGuessResult("Incorrect! Try again.");
//       }

//     } catch (error) {
//       console.error("Error validating song:", error);
//     }
//   };

//   return (
//     <div>
//       <form method="post" onSubmit={handleSubmit}>
//         <div id="toprightimg">
//           <img  src="/images/toprightcorner.png"/>
//         </div>

//         <div id = "header">
//         <HStack>
//           <IoIosMusicalNote style={{ fontSize: "3rem" }}/>
//           <h1>Are we there yet?</h1>
//         </HStack>
//         </div>
        
//         <div>
//           <HStack>
//             <BsMusicPlayerFill style={{ fontSize: "2rem" }}/>
//             <h2>Guess the song! </h2>
//           </HStack>
//         </div>
      
//         <label>
//           Text input: <input name="userInput" />
//         </label>
//         <button type="submit">Guess!</button>

//         {<p>{guessResult}</p>}
//       </form>
//       {songPreviewUrl && (
//         <SongPlayer previewUrl={songPreviewUrl} playSong={playSong} />
//       )}
//     </div>
//   );
// };

// export default App;

import React, { useEffect, useState } from "react";
import { HStack } from "@chakra-ui/react";
import { IoIosMusicalNote } from "react-icons/io";
import { BsMusicPlayerFill } from "react-icons/bs";
import axios from "axios";
import SongPlayer from "./play_song";
import './App.css';


const App: React.FC = () => {
  
  const [actualSong, setActualSong] = useState<string | null>(null);
  const [guessResult, setGuessResult] = useState<string | null>(null);
  const [songPreviewUrl, setSongPreviewUrl] = useState<string | null>(null);
  const [playSong, setPlaySong] = useState<boolean>(false);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/random-song")
      .then(response => {
        const { name, preview } = response.data;
        setActualSong(response.data.name);
        setSongPreviewUrl(preview);
      })
      .catch(error => console.error("Error fetching song:", error));

    // Spotify Web Playback SDK integration
    if (typeof window !== "undefined" && (window as any).Spotify) {
      const player = new (window as any).Spotify.Player({
        name: 'Web Playback SDK',
        getOAuthToken: (cb: Function) => {
          cb('BQBcd_EveqJn-J0KOoHXY3Be8KbN_f_wMnOVdjdM1ut6peNBe3Ico0Z9lK20tJvZVrOpEIX-s0_YJktQl4VKKxyc3KnYv6umP8pF0Gpe3Ind_VabmkUoCdEIdigw3vXnBmibu4tv7Eo'); // Replace with actual access token
        },
        volume: 0.5
      });

      player.addListener('ready', ({ device_id }: { device_id: string }) => {
        console.log('Player is ready with device ID:', device_id);
      });

      player.connect().then((success: boolean) => {
        if (success) {
          console.log('The Web Playback SDK successfully connected to Spotify!');
        } else {
          console.error('Failed to connect to the Web Playback SDK');
        }
      });

      // Handle song preview logic
      if (songPreviewUrl) {
        const audioPlayer = document.getElementById("audioPlayer") as HTMLAudioElement;
        if (audioPlayer) {
          audioPlayer.src = songPreviewUrl;
          audioPlayer.play();
        }
      }
    } else {
      console.error("Spotify Web Playback SDK not found.");
    }
  }, [songPreviewUrl]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const form = e.currentTarget;
    const formData = new FormData(form);
    const userGuess = formData.get("userInput") as string;

    if (!actualSong) {
      console.error("No actual song fetched yet.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/validate-song", {
        user_input: userGuess,
        correct_song: actualSong
      });

      console.log("API Response:", response.data);
      if (response.data.is_match) {
        setGuessResult("Correct! You guessed the song!");
      } else {
        setGuessResult("Incorrect! Try again.");
      }
    } catch (error) {
      console.error("Error validating song:", error);
    }
  };

  return (
    <div>
      <form method="post" onSubmit={handleSubmit}>
        <div id="toprightimg">
          <img src="/images/toprightcorner.png" alt="Top Right Corner" />
        </div>

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

        <label>
          Text input: <input name="userInput" />
        </label>
        <button type="submit">Guess!</button>

        {<p>{guessResult}</p>}
      </form>
      {songPreviewUrl && (
        <SongPlayer previewUrl={songPreviewUrl} playSong={playSong} />
      )}
    </div>
  );
};

export default App;
