import asyncio
from qqmusic_api import Client

async def fetch_word_level_lyrics(song_name: str):
    print(f"--- INPUT ---")
    print(f"Searching for song: {song_name}\n")
    
    # We open the Client session here. All API modules (search, lyric, etc.) 
    # should be accessed through this 'client' object.
    async with Client() as client:
        
        # Step 1: Search for the song
        search_result = await client.search.search_by_type(keyword=song_name, num=1)
        
        # Check if the search returned any songs
        if not search_result.song:
            print("OUTPUT: No songs found matching your input.")
            return

        target_song = search_result.song[0]
        song_mid = target_song.mid
        song_title = target_song.name
        
        # Safely grab the singer's name if it exists
        singer_name = target_song.singer[0].name if target_song.singer else "Unknown Artist"
        
        print(f"Found Track: {song_title} - {singer_name} (MID: {song_mid})\n")
        
        # Step 2: Fetch the lyric data using the song_mid
        # FIXED: We now correctly use client.lyric instead of a standalone import
        lyric_data = await client.lyric.get_lyric(song_mid=song_mid)
        
        print(f"--- OUTPUT ---")
        
        # Step 3: Extract and display the lyrics safely
        # We use getattr() just in case a specific song doesn't have these fields
        standard_lyrics = getattr(lyric_data, 'lyric', None)
        translation = getattr(lyric_data, 'trans', None)
        
        if standard_lyrics:
            print("Standard Line-by-Line / Synced Lyrics Content:")
            # Printing just the first 500 characters so it doesn't flood your terminal
            print(standard_lyrics[:500] + "\n... [Truncated for display]\n")
        else:
            print("No standard lyrics found for this track.")
            
        if translation:
            print("Translation is also available for this track.")

if __name__ == "__main__":
    # Example input query
    user_query = "晴天"  # Jay Chou - Sunny Day
    asyncio.run(fetch_word_level_lyrics(user_query))