import { Provider } from "@/components/ui/provider";
import React, { useEffect, useState } from "react";
import axios from "axios";

const App: React.FC = () => {
  const [message, setMessage] = useState("");
  const [actualSong, setActualSong] = useState<string | null>(null);
  const [guessResult, setGuessResult] = useState<string | null>(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/random-song")
      .then(response => {
        setActualSong(response.data.name);
        console.log(`Correct song: ${response.data.name}`);
      })
      .catch(error => console.error("Error fetching song:", error));
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
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

      // Display match result
      if (response.data.match) {
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
        <h1>Are we there yet?</h1>
        <h2>Guess the song! </h2>
        <label>
          Text input: <input name="userInput" />
        </label>
        
        <button type="submit">Guess!</button>

        {guessResult && <p>{guessResult}</p>}
      </form>
    </div>
  );
};

export default App;
