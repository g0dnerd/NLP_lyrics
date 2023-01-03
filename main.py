import genius_parser
import nltk_generation
import markov_generation
import argparse

if __name__ == "__main__":

    # Parse artist name and generation mode
    parser = argparse.ArgumentParser(
        description='Download song lyrics by an artist and generate more.')
    parser.add_argument(
        'artist', type=str, help='The artist name to generate lyrics for. Please input this in quotation marks using spaces if necessary.')
    parser.add_argument(
        "--mode", help="The chosen generation mode. nltk and markov currently exist.")
    args = parser.parse_args()

    geniusParser = genius_parser._GeniusParser()
    artist_id = geniusParser.get_artist_id({args.artist})
    songs = geniusParser.get_songs(artist_id)
    print("Parsed %d songs by %d" %(len(songs), str(args.artist)))
    lyrics = ""

    song_counter = 1
    for song in songs:
        url = geniusParser.get_song_url(
            song['primary_artist']['name'], song['title'])
        lyrics += geniusParser.get_lyrics(url)
        print("Scraping lyrics for song %d out of %d" %(song_counter, len(songs)), end='\r')
        song_counter += 1

    if args.mode == "nltk":

        nltkGenerator = nltk_generation.NltkGenerator()
        new_lyrics = nltkGenerator.generate_lyrics(lyrics)

    elif args.mode == "markov":
        markovGenerator = markov_generation.MarkovGenerator()
        new_lyrics = markovGenerator.generate_lyrics(lyrics, 10, 10)

print(new_lyrics)
