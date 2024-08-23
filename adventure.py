adventure_map = {}


def main():
    load_map("dungeon")
    play_adventure()


def load_map(name):
    global adventure_map
    adventure_map.clear()

    with open(name + ".map", "r") as map_file:
        node_name = ""
        node_body = ""
        for line in map_file.read().splitlines():
            if line.startswith("> node "):
                if node_name != "":
                    adventure_map[node_name] = node_body
                    node_body = ""
                node_name = line[7:]
            elif line != "":
                node_body += line + "\n"
        adventure_map[node_name] = node_body


def play_adventure():
    current_node = "START"    
    game_running = True
    while game_running:
        links = []
        for line in adventure_map[current_node].splitlines():
            if line.startswith("> linkto "):
                link_target = line[9:line.find(" > ")]
                link_name = line[line.find(" > ") + 3:]
                links.append([link_target, link_name])
            else:
                print("\n" + line)
        for i in range(0, len(links)):
            print(f"    {i}) {links[i][1]}")
        choice = input("Choose an option: ")
        if choice.isdigit() and int(choice) < len(links):
            current_node = links[int(choice)][0]
            if current_node == "END":
                game_running = False


main()