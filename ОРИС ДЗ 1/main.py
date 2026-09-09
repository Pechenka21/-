class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, name, duration):
        self.songs.append({"name": name, "duration": duration})

    def remove_song(self, name):
        for i in range(len(self.songs)):
            if self.songs[i]["name"] == name:
                del self.songs[i]
                break

    def total_duration(self):
        total = 0
        for song in self.songs:
            total += song["duration"]
        return total

    def __len__(self):
        return len(self.songs)

    def display(self):
        if len(self.songs) == 0:
            print("Плейлист пуст.")
        else:
            print("Список песен:")
            for i in range(len(self.songs)):
                song = self.songs[i]
                print(str(i+1)+ '. ' + song['name'] + " – " + str(song['duration']) + " сек")




print("=== Создаём плейлист и добавляем песни ===")
my_playlist = Playlist()
my_playlist.add_song("Bohemian Rhapsody", 354)
my_playlist.add_song("Stairway to Heaven", 482)
my_playlist.add_song("Hotel California", 390)
my_playlist.display()

print(f"\nКоличество песен: {len(my_playlist)}")
print(f"Общая длительность: {my_playlist.total_duration()} сек")

print("\n=== Удаляем песню Stairway to Heaven ===")
my_playlist.remove_song("Stairway to Heaven")
my_playlist.display()

print("\n=== Пытаемся удалить несуществующую песню ===")
my_playlist.remove_song("Imagine")
my_playlist.display()

print("\n=== Создаём пустой плейлист ===")
empty = Playlist()
empty.display()
print(f"Песен: {len(empty)}, длительность: {empty.total_duration()} сек")


