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
    

    def print_for_display(self):
        print(self.get_description())
        for link_text in self.links:
            print(f'Linked to {self.links[link_text]} by "{link_text}"')
        if self.goto:
            print(f"Immediately transition to {self.goto}")
    

    def get_string(self, node_name):
        links = ""
        for link_text in self.links:
            links += f"\n[link {self.links[link_text]} {link_text}]"
        goto = ""
        if self.goto:
            goto = f"\n[goto {self.goto}]"
        on_exited = ""
        if self.on_exited:
            on_exited = f"\n[on_exit {self.on_exited}]"
        return f"[node {node_name}\n[text {self.get_description()}]{links}{goto}{on_exited}]"


def main():
    keep_going = True
    while keep_going:
        menu_options = {
            "Load an adventure":"load",
            "Load default adventure":"load default",
            "Edit an adventure":"edit",
            "Quit":"quit"
        }
        choice = menu_options[get_input_from_menu(sorted(menu_options))]
        if choice == "load":
            play(load_adventure(input("Enter the file name: ")))
        elif choice == "load default":
            play(load_adventure("dungeon"))
        elif choice == "edit":
            edit(input("Enter the file name: "))
        elif choice == "quit":
            keep_going = False
        


def load_adventure(name):
    adventure = {}

    try:
        map_file = open(f"{name}.adv", "r")
        eval_commands(map_file.read(), adventure)
        map_file.close()
    except FileNotFoundError:
        return {}

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
        if node.goto in ["", "NONE"]:
            current_node = node.links[get_input_from_menu(sorted(node.links))]
        else:
            current_node = node.goto
        node.exit()
        if current_node == "END":
            game_running = False


def edit(file):
    adventure = load_adventure(file)
    options = {
            "Edit an existing node":"edit",
            "Create a new node":"create",
            "Save and quit":"quit",
            "Delete a node":"delete"
        }
    keep_going = True
    while keep_going:
        print("Current Nodes:")
        for node_name in adventure:
            print(node_name)
        action = options[get_input_from_menu(sorted(options))]
        if action == "edit":
            node_name = get_input_from_menu(sorted(adventure))
            node = adventure[node_name]
            new_node_name = edit_node(node, node_name)
            del adventure[node_name]
            adventure[new_node_name] = node
        elif action == "create":
            node = Node()
            node_name = edit_node(node, "new-node")
            adventure[node_name] = node
        elif action == "delete":
            node_name = input("Node to delete: ")
            if node_name != "":
                del adventure[node_name]
        elif action == "quit":
            keep_going = False
    
    with open(file + ".adv", "w+") as adv_file:
        for node_name in adventure:
           adv_file.write(adventure[node_name].get_string(node_name) + "\n\n")
        adv_file.close()


def edit_node(node, node_name):
    node.print_for_display()
    node_name = edit_field(node_name, "Node name")
    node.description = [edit_field(node.get_description(), "Description")]
    linking = True
    while linking:
        link_type = get_input_from_menu(["Edit link", "Delete a link", "Add link", "Set transition", "Finish"])
        if link_type == "Edit link":
            edit_link(node, get_input_from_menu(sorted(node.links)))
        elif link_type == "Add link":
            node.add_link("", "")
            edit_link(node, "")
        elif link_type == "Set transition":
            node.goto = edit_field(node.goto, "Node to go to")
        elif link_type == "Finish":
            linking = False
        elif link_type == "Delete a link":
            node.remove_link(get_input_from_menu(sorted(node.links)))
    return node_name


def edit_link(node, link_text):
    link_target = node.links[link_text]
    link_target = edit_field(link_target, "Node to link to")
    node.remove_link(link_text)
    link_text = edit_field(link_text, "Link text")
    node.add_link(link_target, link_text)


def edit_field(current, field_name):
    content = input(f"{field_name} ({current}) ")
    if content == "":
        content = current
    return content


def get_input_from_menu(menu_options):
    if len(menu_options) > 0:
        for i in range(0, len(menu_options)):
            print(f"    {i}) {menu_options[i]}")
        choice = input("Choose an option: ")
        if choice.isdigit() and int(choice) < len(menu_options):
            return menu_options[int(choice)]
        return get_input_from_menu(menu_options)
    return ""


main()