from math import sqrt
from random import random
from random import randint
from random import randrange
from random import choice




# обьект лабаринта
class DungeonSqr:
    def __init__(self, sqr):
        self.sqr = sqr

    def get_ch(self):
        return self.sqr


# комната
class Room:
    def __init__(self, r, c, h, w):
        self.row = r
        self.col = c
        self.height = h
        self.width = w
        self.map = []
        print(self.height, self.width)

        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append(DungeonSqr('#'))
            row[0] = DungeonSqr(' ')
            row[-1] = DungeonSqr(' ')
            self.map.append(row)

        self.map[0] = [DungeonSqr(' ') for x in range(self.width)]
        self.map[-1] = [DungeonSqr(' ') for x in range(self.width)]
        self.generate()

    # кастомный random walk для случайной генерации внутри каждой комнаты
    def generate(self):
        floor_x, floor_y = 1, 1  # randint(1, self.width - 1), randint(1, self.height - 1)
        required_floor = (self.height * self.width) * random()  # - 2 * (self.height + self.width ) - 4) * 0.9
        print(required_floor, self.height * self.width)
        self.map[floor_y][floor_x] = DungeonSqr(' ')

        for floor_count in range(round(required_floor - 0.5)):
            counter = 0
            while counter < 100:
                direction = randint(1, 4)
                if direction == 1:
                    if floor_y + 1 < self.height - 1:
                        floor_y += 1
                        if (self.map[floor_y][floor_x].get_ch() == '#'):
                            self.map[floor_y][floor_x] = DungeonSqr(' ')
                            break
                        else:
                            counter += 1
                    else:
                        counter += 1
                elif direction == 2:
                    if floor_y - 1 > 1:
                        floor_y -= 1
                        if (self.map[floor_y][floor_x].get_ch() == '#'):
                            self.map[floor_y][floor_x] = DungeonSqr(' ')
                            break
                        else:
                            counter += 1
                    else:
                        counter += 1
                elif direction == 3:
                    if floor_x + 1 < self.width - 1:
                        floor_x += 1
                        if (self.map[floor_y][floor_x].get_ch() == '#'):
                            self.map[floor_y][floor_x] = DungeonSqr(' ')
                            break
                        else:
                            counter += 1
                    else:
                        counter += 1
                else:
                    if floor_x - 1 > 1:
                        floor_x -= 1
                        if (self.map[floor_y][floor_x].get_ch() == '#'):
                            self.map[floor_y][floor_x] = DungeonSqr(' ')
                            break
                        else:
                            counter += 1
                    else:
                        counter += 1

"""
This example procedurally develops a random cave based on
Binary Space Partitioning (BSP)

For more information, see:
http://roguebasin.roguelikedevelopment.org/index.php?title=Basic_BSP_Dungeon_generation
https://github.com/DanaL/RLDungeonGenerator

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.procedural_caves_bsp
"""


class RLDungeonGenerator:
    def __init__(self, w, h):
        self.MAX = 10  # количетство разрезов прострасчтва
        self.width = w
        self.height = h
        self.leaves = []
        self.dungeon = []
        self.rooms = []

        for h in range(self.height):
            row = []
            for w in range(self.width):
                row.append(DungeonSqr('#'))

            self.dungeon.append(row)

    # кастомный сплит чтобы работал до границ
    def random_split(self, min_row, min_col, max_row, max_col):

        seg_height = max_row - min_row
        seg_width = max_col - min_col

        if seg_height < self.MAX and seg_width < self.MAX:
            self.leaves.append((min_row, min_col, max_row, max_col))
        elif seg_height < self.MAX and seg_width >= self.MAX:
            self.split_on_vertical(min_row, min_col, max_row, max_col)
        elif seg_height >= self.MAX and seg_width < self.MAX:
            self.split_on_horizontal(min_row, min_col, max_row, max_col)
        else:
            if random() < 0.5:
                self.split_on_horizontal(min_row, min_col, max_row, max_col)
            else:
                self.split_on_vertical(min_row, min_col, max_row, max_col)

    # распределение комнат по горизонтали
    def split_on_horizontal(self, min_row, min_col, max_row, max_col):
        split = (min_row + max_row) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, split, max_col)
        self.random_split(split + 1, min_col, max_row, max_col)

    # распределение комнат по вертикали
    def split_on_vertical(self, min_row, min_col, max_row, max_col):
        split = (min_col + max_col) // 2 + choice((-2, -1, 0, 1, 2))
        self.random_split(min_row, min_col, max_row, split)
        self.random_split(min_row, split + 1, max_row, max_col)

    def permit_room(self, room):
        for r, row in enumerate(room.map):
            for c, tile in enumerate(row):
                self.dungeon[room.row + r][room.col + c] = tile

    def carve_rooms(self):
        for leaf in self.leaves:
            # наполняем листья комнатми
            if random() > 0.80: continue
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            # чтобы команты не стыковались совсем в плотную
            room_width = round(randrange(80, 100) / 100 * section_width)
            room_height = round(randrange(80, 100) / 100 * section_height)

            # проверка что комнаты не слишком далеко
            if section_height > room_height:
                room_start_row = leaf[0] + randrange(section_height - room_height)
            else:
                room_start_row = leaf[0]

            if section_width > room_width:
                room_start_col = leaf[1] + randrange(section_width - room_width)
            else:
                room_start_col = leaf[1]

            self.rooms.append(Room(room_start_row, room_start_col, room_height, room_width))
            self.permit_room(self.rooms[-1])
            # for r in range(room_start_row, room_start_row + room_height):
            #    for c in range(room_start_col, room_start_col + room_width):
            #        self.dungeon[r][c] = DungeonSqr(' ')

    def are_rooms_adjacent(self, room1, room2):
        adj_rows = []
        adj_cols = []
        for r in range(room1.row, room1.row + room1.height):
            if r >= room2.row and r < room2.row + room2.height:
                adj_rows.append(r)

        for c in range(room1.col, room1.col + room1.width):
            if c >= room2.col and c < room2.col + room2.width:
                adj_cols.append(c)

        return (adj_rows, adj_cols)

    def distance_between_rooms(self, room1, room2):
        centre1 = (room1.row + room1.height // 2, room1.col + room1.width // 2)
        centre2 = (room2.row + room2.height // 2, room2.col + room2.width // 2)
        # тупо манхэтэнское расстояние
        return sqrt((centre1[0] - centre2[0]) ** 2 + (centre1[1] - centre2[1]) ** 2) + 1
        # коррдиор между двумя комантами

    def carve_corridor_between_rooms(self, room1, room2):
        if room2[2] == 'rows':
            row = choice(room2[1])
            # Figure out which room is to the left of the other
            if room1.col + room1.width < room2[0].col:
                start_col = room1.col + room1.width
                end_col = room2[0].col
            else:
                start_col = room2[0].col + room2[0].width
                end_col = room1.col
            for c in range(start_col, end_col):
                self.dungeon[row][c] = DungeonSqr(' ')

            if end_col - start_col >= 4:
                self.dungeon[row][start_col] = DungeonSqr('1')
                self.dungeon[row][end_col - 1] = DungeonSqr('1')
            elif start_col == end_col - 1:
                self.dungeon[row][start_col] = DungeonSqr('1')
        else:
            col = choice(room2[1])
            # Figure out which room is above the other
            if room1.row + room1.height < room2[0].row:
                start_row = room1.row + room1.height
                end_row = room2[0].row
            else:
                start_row = room2[0].row + room2[0].height
                end_row = room1.row

            for r in range(start_row, end_row):
                self.dungeon[r][col] = DungeonSqr(' ')

            if end_row - start_row >= 4:
                self.dungeon[start_row][col] = DungeonSqr('1')
                self.dungeon[end_row - 1][col] = DungeonSqr('1')
            elif start_row == end_row - 1:
                self.dungeon[start_row][col] = DungeonSqr('1')

    # ищем две группы комнат и соеденяем их
    def find_closest_unconnect_groups(self, groups, room_dict):
        shortest_distance = 99999
        start = None
        start_group = None
        nearest = None

        for group in groups:
            for room in group:
                key = (room.row, room.col)
                for other in room_dict[key]:
                    if not other[0] in group and other[3] < shortest_distance:
                        shortest_distance = other[3]
                        start = room
                        nearest = other
                        start_group = group

        self.carve_corridor_between_rooms(start, nearest)

        # Merge the groups
        other_group = None
        for group in groups:
            if nearest[0] in group:
                other_group = group
                break

        start_group += other_group
        groups.remove(other_group)

    def connect_rooms(self):
        """
        собирает входы в комнаты в словарь
        """
        groups = []
        room_dict = {}
        for room in self.rooms:
            key = (room.row, room.col)
            room_dict[key] = []
            for other in self.rooms:
                other_key = (other.row, other.col)
                if key == other_key: continue
                adj = self.are_rooms_adjacent(room, other)
                if len(adj[0]) > 0:
                    room_dict[key].append((other, adj[0], 'rows', self.distance_between_rooms(room, other)))
                elif len(adj[1]) > 0:
                    room_dict[key].append((other, adj[1], 'cols', self.distance_between_rooms(room, other)))

            groups.append([room])

        while len(groups) > 1:
            self.find_closest_unconnect_groups(groups, room_dict)

    def generate_map(self):
        pass
        self.random_split(1, 1, self.height - 1, self.width - 1)
        self.carve_rooms()
        self.connect_rooms()

    def print_map(self):
        for r in range(self.height):
            row = ''
            for c in range(self.width):
                row += self.dungeon[r][c].get_ch()
            print(row)

    def getmap(self):
        map = []
        for r in range(self.height):
            st = ''
            for c in range(self.width):
                st += (self.dungeon[r][c].get_ch())
            map += [st]

        return map

    def create_spawn(self):
        x, y = 0, 0
        for row in range(self.height):
            for col in range(self.width):
                if self.dungeon[row][col].get_ch() == ' ':
                    self.dungeon[row][col] = DungeonSqr('*')
                    y, x = (row, col)
                    break
        return x, y

    def getgold(self):
        gld = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.dungeon[row][col].get_ch() == '1':
                    gld += 1
        return gld


dg = RLDungeonGenerator(30, 20)
dg.generate_map()

#print(dg.getgold())
#dg.print_map()

