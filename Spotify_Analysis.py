import json
from datetime import datetime
import matplotlib.pyplot as plt

#{"ts":"2022-11-30T18:51:01Z","username":"floxxiy","platform":"ios",
#"ms_played":0,"conn_country":"US","ip_addr_decrypted":"140.232.174.71",
#"user_agent_decrypted":"unknown",
#"master_metadata_track_name":"God’s Menu",
#"master_metadata_album_artist_name":"Stray Kids",
#"master_metadata_album_album_name":"GO LIVE",
#"spotify_track_uri":"spotify:track:4XPXrcpyNr30Km6aPiflJy",
#"episode_name":null,"episode_show_name":null,
#"spotify_episode_uri":null,"reason_start":"unknown",
#"reason_end":"endplay","shuffle":false,"skipped":true,
#"offline":null,"offline_timestamp":0,"incognito_mode":false}

class Song:
    '''create a class called Song that stores as songs: \
        title, artist, playdate, reason for ending playback, and duration'''
    def __init__(self, title, artist, date, reason_end, ms_played):
        self.title = title
        self.artist = artist
        self.time = date[11:19]
        self.hour = int(self.time[:2]) - 6
        if self.hour < 0:
            self.hour = 24 + self.hour
        self.date = date[:10]
        if reason_end == "fwdbtn":
            self.skipped = True
        else:
            self.skipped = False
        self.miliseconds = ms_played
    
    def __repr__(self):
        return f'{self.title} by {self.artist} was played on {self.date}'

def import_data(filename):
    '''given a filename, this function opens the file and reads from it to create a \
        new lists of Song objects '''
    songs = []
    with open(filename, mode='r', encoding='utf-8') as file:
        data = json.load(file)
        for record in data:
            date, username, platform, ms_played, country, ip, user, title, artist, album, url, epi_name, epi_show, epi_url, start, reason_end, shuffle, skipped, offline, offline_time, incog = record
            songs.append(Song(record[title], record[artist], record[date], record[reason_end], record[ms_played]))
    return songs

def create_song_list(start_date, end_date):
    '''given a start and end date, this function sends each file\
        to the import_data function, \
        then with the new list, filters out songs not within the given date \
        range and returns a new list'''
    
    song_list = []

    all_song_lists = [
        "Streaming_History_Audio_2019-2021_0.json", 
        "Streaming_History_Audio_2021-2022_1.json",
        "Streaming_History_Audio_2022_2.json",
        "Streaming_History_Audio_2022-2023_3.json",
        "Streaming_History_Audio_2023_4.json"
    ]

    start_date = datetime.strptime(start_date, "%Y-%m-%d") #figure out this
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    for filename in all_song_lists:
        single_song_list = import_data(filename)
        filtered_songs = [song for song in single_song_list if start_date <= datetime.strptime(song.date, "%Y-%m-%d") <= end_date]
        song_list.extend(filtered_songs)
    
    return song_list

def find_most_common_songs(song_list, k):
    '''Creates an empty dictionary and then interates through each \
        song in the given list, and if the title matches a song already\
        in the dicitonary, it increases the “times listended” counter by 1, \
        if not it adds that song to the dictionary.''' 
    
    same_songs = {}
    z = k
    for record in song_list:
        if record.title is not None:
            if record.title in same_songs:
                same_songs[record.title]  += 1
            else:
                same_songs[record.title] = 1
    
    sorted_list = dict(sorted(same_songs.items(), key=lambda item: item[1], reverse=True)) # figure out how this works

    top_k_songs = {}

    for song, count in sorted_list.items():
        if k >0:
            top_k_songs[song] = count
            k -= 1
        else:
            break
    
    max_title_length = max(len(song) for song in top_k_songs.keys())
    song_column_width = max(max_title_length, len("Song"))

    print(f'Your top {z} most commonly played songs are:''\n') 
    print(f'{"Song":<{song_column_width}} {"Times Played":>20}')

    for song, count in top_k_songs.items():
        print(f'{song:<{song_column_width}} {count:>20}')
    
    '''Prints out the most listended to songs (amount determined by the user) \
        in a tabular format.'''

def total_time(song_list):
    '''For each song in the lists, add up the total amount of milliseconds, \
        and then divides it into days, hours, minutes, and seconds.'''
    total_ms = 0
    
    for song in song_list:
        total_ms += song.miliseconds

    total_sec = total_ms//1000
    total_ms = total_ms % 1000

    total_min = total_sec//60
    total_sec = total_sec % 60

    total_hours = total_min//60
    total_min = total_hours % 60

    total_days = total_hours//24

    return f'{total_hours} hours, {total_min} minutes, and {total_sec} seconds! Or {total_days} days straight!'

def find_most_common_dates(song_list, k):
    '''Creates an empty dictionary and then iterates through \
        each song in the given list, and if the date matches a \
        date already in the dictionary, it increases the date \
        counter by 1, if not it adds that song's date to the dictionary'''
    
    song_dates = {}
    z = k
    for record in song_list:
        if record.title is not None:
            if record.date in song_dates:
                song_dates[record.date]  += 1
            else:
                song_dates[record.date] = 1
    
    sorted_list = dict(sorted(song_dates.items(), key=lambda item: item[1], reverse=True)) # figure out how this works

    top_k_dates = {}
    for date, count in sorted_list.items():
        if k >0:
            top_k_dates[date] = count
            k -= 1
        else:
            break
    
    max_title_length = max(len(date) for date in top_k_dates.keys())
    date_column_width = max(max_title_length, len("Date"))

    print(f'Your top {z} dates, when you listened to music the most are:''\n') 
    print(f'{"Date":<{date_column_width}} {"Songs Played":>20}')

    for date, count in top_k_dates.items():
        print(f'{date:<{date_column_width}} {count:>20}')

    '''Prints out the dates that songs are listened \
        to on the most (amount determined by the user) in a tabular'''
 
def most_common_time(song_list):
    '''Creates an empty dictionary and then iterates through \
        each song in the given list, and if the hour of the day \
        matches an hour already in the dictionary, it increases the hour \
        counter by 1, if not it adds that song's hour to the dictionary'''
    hours_of_day = {}
    
    for song in song_list:
        if song.title is not None:
            if song.hour in hours_of_day:
                hours_of_day[song.hour]  += 1
            else:
                hours_of_day[song.hour] = 1
    
    sorted_list = dict(sorted(hours_of_day.items(), key=lambda item: item[1], reverse=True))
   
    print(f'{"Hour of Day (MST)":<20}{"Songs Played":>10}')
    for hour, count in sorted_list.items():
        if hour == 0:
            print(f'{"12 AM":<20} {count:>10}')
        elif 1 <= hour <= 11:
            print(f'{str(hour) + " AM":<20} {count:>10}')
        elif hour == 12:
            print(f'{"12 PM":<20} {count:>10}')
        else:
            print(f'{str((hour - 12)) + " PM":<20}  {count:>10}')

    '''Prints out the hour that songs are listened to on the most \
        (amount determined by the user) in a tabular format.'''

def average_amounts(song_list, start_date, end_date):
    '''Transforms the start and end date into datetime \
        objects then find the total amount of days in the\
        given range, then divides that by the length of the \
        list of songs to output the average amount of songs listened to per day.'''

    total_songs = len(song_list)

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    total_days = (end_date - start_date).days + 1
    average_songs_per_day = total_songs / total_days

    print(f'Average number of songs listened per day: {average_songs_per_day:.2f}')

def most_skipped(song_list, k):
    '''Iterates through the list of songs and sees if the reason \
        the track ended was because of the forward button, if the \
        song was already in the dictionary, it increases the count \
        by one, if it was not then it adds the song to the dictionary. '''
    skipped_songs = {}

    for song in song_list:
        if song.title is not None:
            if song.title in skipped_songs:
                if song.skipped:
                    skipped_songs[song.title] += 1
            else:
                skipped_songs[song.title] = 1 if song.skipped else 0

    sorted_list = dict(sorted(skipped_songs.items(), key=lambda item: item[1], reverse=True))

    top_k_skipped_songs = {}
    for song_title, count in sorted_list.items():
        if k > 0:
            top_k_skipped_songs[song_title] = count
            k -= 1
        else:
            break

    print(f'The top {len(top_k_skipped_songs)} most skipped songs are:\n')
    print(f'{"Song":<{30}} {"Artist":>20} {"Times Skipped":>20}')

    for song_title, count in top_k_skipped_songs.items():
        song = next((song for song in song_list if song.title == song_title), None)
        if song:
            print(f'{song.title:<{30}} {song.artist:>20} {count:>20}')
    
    '''Then it prints out a list of the most skipped songs \
        (number determined by the user) in a tabular format.'''

def orphan_songs(song_list):
    '''Iterates though each song and adds it to a dictionary, \
        if the song is already in the dictionary, it increases \
        the counter by one. Then sums up the number of songs \
        that had a count of 1 in the dictionary and prints out that number.'''
    same_songs = {}
    for record in song_list:
        if record.title is not None:
            if record.title in same_songs:
                same_songs[record.title]  += 1
            else:
                same_songs[record.title] = 1

    orphan_count = sum(1 for count in same_songs.values() if count == 1)

    print(f'You listened to {orphan_count} songs that you never listened to again')

def songs_per_month_graph(song_list):
    '''Extracts the month and year from the song list for each song, \
        zips the month and year together, adds the zipped keys to the \
        dictionary and iterates through the songs to add counts to the \
        dictionary. Then zip the dates and the counts. Uses matplotlib \
        to create a graph.'''
    months = [song.date[5:7] for song in song_list]
    years = [song.date[:4] for song in song_list]
    
    
    song_count_per_month = {}
    for month, year in zip(months, years):
        key = f"{year}-{month}"
        if key in song_count_per_month:
            song_count_per_month[key] += 1
        else:
            song_count_per_month[key] = 1
    
    
    sorted_counts = sorted(song_count_per_month.items())
    months_years, counts = zip(*sorted_counts)
    
    #plotting
    plt.figure(figsize=(10, 6))
    plt.bar(months_years, counts, color='skyblue')
    plt.title('Songs Listened to per Month')
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Songs')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    start_date = input("What date do you want to start analyzing data from? (yyyy-mm-dd)")
    end_date = input("What date do you want to end data analyzation? (yyyy-mm-dd)")
    song_list = create_song_list(start_date, end_date)
    
    print(f'For {len(song_list)} songs, let us look at some intersting data:')
    print(f'In total you listened to music for {total_time(song_list)}')

    print('For the selected date range, lets look at a visual of your music habits! (close the graph to continue analysis)')
    songs_per_month_graph(song_list)
    
    k = int(input("How many top songs do you want to see? "))
    
    find_most_common_songs(song_list, k)
    print()

    k = int(input("How many top dates do you want to see? "))
    
    find_most_common_dates(song_list, k)
    print()

    orphan_songs(song_list)
    print()
    
    k = int(input("How many top skipped songs do you want to see? "))
    
    most_skipped(song_list, k)
    print()

    print('Here are the most common times of day that you listen to music:')
    most_common_time(song_list)
    print()

    average_amounts(song_list, start_date, end_date)
    print()

    

