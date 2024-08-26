class Node:
    description = ""
    links = {}
    goto = ""

    def add_link(self, target, text):
        self.links[text] = target


def main():
    menu_options = {
        "Load an adventure":lambda: play(load_adventure("dungeon"))#input("Enter the file name: "))
    }
    menu_options[get_input_from_menu(["Load an adventure"])]()


def load_adventure(name):
    adventure = {}

    with open(name + ".adv", "r") as map_file:
        eval_commands(map_file.read(), adventure)

    return adventure


def eval_commands(string, root):
    args = []
    arg_text = ""
    indents = 0
    for char in string:
        if char in " ]\n":
            if arg_text != "":
                args.append(arg_text)
                arg_text = ""
        elif indents > 0:
            arg_text += char
        if char == "[":
            indents += 1
        elif char == "]":
            indents -= 1
            arg_text += "]"
            if indents == 0:
                run_command(args[0], root, args[1:])
                args = []
                arg_text = ""


def run_command(name, root, args):
    eval(f'_advfunc_{name}(root, "{separate(args, '", "')}")')


def separate(array, spacer):
    string = ""
    for item in array:
        if string != "":
            string += spacer
        string += str(item)
    return string


def _advfunc_node(root, name, *rest):
    node = Node()
    eval_commands(separate(rest, " "), node)
    root[name] = node


def _advfunc_text(root, *text):
    root.description = separate(text, " ")


def _advfunc_link(root, *foo):
    root.add_link(foo[0], separate(foo[1:], " "))


def _advfunc_goto(root, target):
    root.goto = target


def play(adventure):
    current_node = "START"    
    game_running = True
    while game_running:
        node = adventure[current_node]
        print(f"\n{node.description}")
        if node.goto:
            current_node = node.goto
        else:
            current_node = node.links[get_input_from_menu(sorted(node.links))]
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