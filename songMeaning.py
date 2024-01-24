TOKEN_GOOGLE_STUDIO = [GENERATED_API_TOKEN_IN_GOOGLE_STUDIO_AI]
TOKEN_GENIUS = [GENERATED_TOKEN_IN_GENIUS_API]

import streamlit as st
import google.generativeai as genai
genai.configure(api_key=TOKEN_GOOGLE_STUDIO)

from lyricsgenius import Genius
genius = Genius(TOKEN_GENIUS)


st.set_page_config(layout="wide")


def inputs():
    st.sidebar.header("Song Meaning")

    song_artist = st.sidebar.text_input("Artist Name", placeholder =   "Ex: The Killers", )
    song_title = st.sidebar.text_input("Song Name", placeholder =   "Ex: Human", )
    
    button = st.sidebar.button("Get song meaning")

    return song_title, song_artist, button


def lyricFindr(song, artist):
    
    """
    Function that seachr the lyrics for a song.
    
    Args:
    
    song: Song Name
    artist: Artist Name
    """

    search = f"{song}, {artist}"

    song_search = genius.search_songs(search)

    data = song_search["hits"][0]
    song_metadata = data["result"]
    song_id = song_metadata["id"]
    embed_count = song_metadata["pyongs_count"]
    title = song_metadata["full_title"].split(" by")[0]
    artist_name = song_metadata["artist_names"]
    
    song_metadata2 = genius.song(song_id)
    total_contributors = song_metadata2['song']['stats']['contributors']
    search_lyrics = genius.lyrics(song_id)

    lyrics = search_lyrics.split(f"{total_contributors} Contributors")[1]
    lyrics = lyrics.split(f"{embed_count}Embed")[0]
    
    return artist_name, title, lyrics


def songFindr(artist, song, lyrics):

    # Set up the model
    generation_config = {
        "temperature": 0.8,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    prompt_parts = [
      "You are an English teacher for Spanish speakers. The student will give you the artist name, the name of the song and the lyrics of the song you will explain the meaning of the songs in Spanish and get the main characters or entities within the song short.",
      "Artist: The Killers\n",
      "Song: Human\n",
      "Lyrics English: [Verse 1]\nI did my best to notice\nWhen the call came down the line\nUp to the platform of surrender\nI was brought, but I was kind\nAnd sometimes I get nervous\nWhen I see an open door\nClose your eyes, clear your heart\n\n[Pre-Chorus 1]\nCut the cord\n\n[Chorus]\nAre we human\nOr are we dancer?\nMy sign is vital\nMy hands are cold\nAnd I'm on my knees\nLooking for the answer\nAre we human\nOr are we dancer?\n\n[Verse 2]\nPay my respects to grace and virtue\nSend my condolences to good\nGive my regards to soul and romance\nThey always did the best they could\nAnd so long to devotion\nYou taught me everything I know\nWave goodbye, wish me well\nYou might also like[Pre-Chorus 2]\nYou've got to let me go\n\n[Chorus]\nAre we human\nOr are we dancer?\nMy sign is vital\nMy hands are cold\nAnd I'm on my knees\nLooking for the answer\nAre we human\nOr are we dancer?\n\n[Bridge]\nWill your system be alright\nWhen you dream of home tonight?\nThere is no message we're receiving\nLet me know, is your heart still beating?\n\n[Chorus]\nAre we human\nOr are we dancer?\nMy sign is vital\nMy hands are cold\nAnd I'm on my knees\nLooking for the answer\n[Pre-Chorus 3]\nYou've got to let me know\n\n[Chorus]\nAre we human\nOr are we dancer?\nMy sign is vital\nMy hands are cold\nAnd I'm on my knees\nLooking for the answer\nAre we human\nOr are we dancer?\n\n[Outro]\nAre we human\nOr are we dancer?\nAre we human\nOr are we dancer?\n",
      "Meaning: The song is a reflection on the human condition, both the insecurities and anxieties associated with a life of freedom and the challenges of negotiating life in a complex world. It questions whether we, as people, are truly in control of our own destiny or whether we are blindly following the routines and expectations that have been set for us. The speaker wonders if, in the end, we are truly living an authentic life or if we are simply automated 'dancers' following a script laid out by someone else. Ultimately, the song suggests that no one has a real answer and that each person must decide for themselves what it means to be human.\n",
      "Characters: The Speaker: Our traveler, struggling with loss, uncertainty and the question \"human vs. dancer\".\n Lost Values: Saying goodbye to \"grace, kindness, soul\" and more, meaning internal changes or disconnection.\nThe System: A possible external force questioned or escaped in \"Will your system be okay?\n\nHuman vs. Dancer: The central question, which represents individuality vs. conformity, free will vs. external control.",
      f"Artist: {artist}\n",
      f"Song: {song}\n",
      f"Lyrics English: {lyrics}",  
      "Meaning:",
      "Characters:",
    ]

    response = model.generate_content(prompt_parts)
    # return print(response.text)

    # Let's split the result
    splitted_res = response.text.split("Characters:")
    meaning_content = splitted_res[0].split("Meaning:")[1].replace("Meaning:", "").replace("**", "")
    characters_content = splitted_res[1].replace("Characters:", "").replace("**", "")

    return meaning_content, characters_content

def main():
    # We call the sidebar
    song_title, song_artist, button = inputs()

    if button:
        artist_name, title, lyrics = lyricFindr(song_title, song_artist)
        meaning, characters = songFindr(artist_name, title, lyrics)


        st.title(title+" By "+ artist_name)

        col1, col2 = st.columns(2, )

        with col1:
            st.subheader("Meaning ", divider='green')
            with st.container():
                st.markdown(meaning)
                
                st.subheader("Characters ", divider='green')           
                st.markdown(characters)

        with col2:
            st.subheader('Lyrics', divider='green')
            with st.container():
                st.text(lyrics)
 

if __name__ == "__main__":
    main()
