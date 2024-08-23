
def main():
    menu_options = {
        "Load an adventure":lambda: play(load_adventure(input("Enter the file name: ")))
    }
    menu_options[get_input_from_menu(["Load an adventure"])]()


def load_adventure(name):
    adventure = {}

    with open(name + ".adv", "r") as map_file:
        node_name = ""
        node_body = ""
        goto = ""
        links = {}
        for line in map_file.read().splitlines():
            if line.startswith("> node "):
                if node_name != "":
                    adventure[node_name] = [node_body, links, goto]
                    node_body = ""
                    links = {}
                    goto = ""
                node_name = line[7:]
            elif line.startswith("> linkto "):
                link_name = line[line.find(" > ") + 3:]
                link_target = line[9:line.find(" > ")]
                links[link_name] = link_target
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
        if goto == "":
            current_node = links[get_input_from_menu(sorted(links))]
        else:
            current_node = goto
        if current_node == "END":
            game_running = False


def get_input_from_menu(menu_options):
    for i in range(0, len(menu_options)):
        print(f"    {i}) {menu_options[i]}")
    choice = input("Choose an option: ")
    if choice.isdigit() and int(choice) < len(menu_options):
        return menu_options[int(choice)]
    return get_input_from_menu(menu_options)


main()