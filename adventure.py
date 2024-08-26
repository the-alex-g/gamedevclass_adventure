class Node:
    description = []
    links = {}
    goto = ""
    replace_with = ""
    on_exited = ""

    def __init__(self):
        # Without this, all the nodes share the same dictionaries and arrays
        self.links = {}
        self.description = []

    def add_link(self, target, text):
        if not text in self.links:
            self.links[text] = target
    

    def remove_link(self, text):
        if text in self.links:
            del self.links[text]
    
    
    def add_description(self, text):
        if not text in self.description:
            self.description.append(text)
    

    def get_description(self):
        return separate(self.description, " ")


    def remove_description(self, text):
        new_description = []
        for old_description in self.description:
            if not old_description == text:
                new_description.append(old_description)
        self.description = new_description
    

    def exit(self):
        # Runs code when this node is exited
        eval_commands(self.on_exited, self)


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


def _advfunc_node(adventure, name, *rest):
    # creates a node and adds it to the adventure
    node = Node()
    eval_commands(separate(rest, " "), node)
    adventure[name] = node


def _advfunc_text(node, *text):
    node.add_description(separate(text, " "))


def _advfunc_link(node, link_target, *link_text):
    node.add_link(link_target, separate(link_text, " "))


def _advfunc_goto(node, target):
    node.goto = target


def _advfunc_on_exit(node, *contents):
    node.on_exited = separate(contents, " ")


def _advfunc_become(node, new_name):
    node.replace_with = new_name


def _advfunc_rm_link(node, *link_text):
    node.remove_link(separate(link_text, " "))


def _advfunc_rm_text(node, *text):
    node.remove_description(separate(text, " "))


def play(adventure):
    current_node = "START"    
    game_running = True
    while game_running:
        node = adventure[current_node]
        while node.replace_with != "":
            node = adventure[node.replace_with]
        print(f"\n{node.get_description()}")
        if node.goto:
            current_node = node.goto
        else:
            current_node = node.links[get_input_from_menu(sorted(node.links))]
        node.exit()
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