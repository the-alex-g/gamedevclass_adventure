
def main():
    play(load_adventure("dungeon"))


def load_adventure(name):
    adventure = {}

    with open(name + ".adv", "r") as map_file:
        node_name = ""
        node_body = ""
        goto = ""
        links = []
        for line in map_file.read().splitlines():
            if line.startswith("> node "):
                if node_name != "":
                    adventure[node_name] = [node_body, links, goto]
                    node_body = ""
                    links = []
                    goto = ""
                node_name = line[7:]
            elif line.startswith("> linkto "):
                links.append([
                    line[9:line.find(" > ")], # link target
                    line[line.find(" > ") + 3:] # link name
                ])
            elif line.startswith("> goto "):
                goto = line[7:]
            elif line != "":
                node_body += line + "\n"
        adventure[node_name] = [node_body, links, goto]
    return adventure


def play(adventure):
    current_node = "START"    
    game_running = True
    while game_running:
        (text, links, goto) = adventure[current_node]
        print(f"\n{text}")
        if goto != "":
            current_node = goto
        else:
            for i in range(0, len(links)):
                print(f"    {i}) {links[i][1]}")
            choice = input("Choose an option: ")
            if choice.isdigit() and int(choice) < len(links):
                current_node = links[int(choice)][0]
        if current_node == "END":
            game_running = False


main()