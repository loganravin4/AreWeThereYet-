import React, { useEffect, useState } from "react";

interface SongPlayerProps {
  previewUrl: string | null;
  playSong: boolean;
}

const SongPlayer: React.FC<SongPlayerProps> = ({ previewUrl, playSong }) => {
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (playSong && previewUrl) {
      const newAudio = new Audio(previewUrl);
      newAudio.play();
      setAudio(newAudio);

      return () => {
        newAudio.pause();
        setAudio(null);
      };
    }
  }, [playSong, previewUrl]);

  return (
    <>
      {audio && (
        <div>
          <p>Now Playing...</p>
          <audio controls>
            <source src={audio.src} type="audio/mp3" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </>
  );
};

export default SongPlayer;