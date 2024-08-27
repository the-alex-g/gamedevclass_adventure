# Functions

### main
This function displays a menu that allows the user to play or edit an adventure.

### load_adventure(name)
This function reads the file "name.adv" into a string and feeds it into `eval_commands`, which populates a dictionary with the nodes of the game. The function returns this dictionary.

### load_default_adventure()
Loads a predetermined string into an adventure dictionary with `eval_commands`.

### eval_commands(string, root)
This function interprets the adventure code and calls the appropriate python functions using `run_command`. These functions modify the `root` object.
The string is parsed by going through it character-by-character, collecting function arguments at spaces, newlines, and right brackets.

### run_command(name, root, args)
Reads the function name and args into a string, which it passes to `eval`.

### separate(array, spacer)
Utility function that returns a string that is the elements of the array, separated by `spacer`.

### _advfunc_node(adventure, name, *rest)
Creates a node, populates its fields using `eval_commands`, and puts it into the `adventure` dictionary. This function can be called by `eval_commands`.

### _advfunc_text(node, *text)
Adds the `*text` to the node's `description` field. This function can be called by `eval_commands`.

### _advfunc_link(node, link_target, *link_text)
Adds the link to the node's `links` field. The node's links are printed out as a menu when the node is entered. This function can be called by `eval_commands`.

### _advfunc_goto(node, target)
Sets the node's `goto` field. Instead of giving a list of links when entered, this node immediately transitions to the node specified by `target`. This function can be called by `eval_commands`.

### _advfunc_on_exit(node, *contents)
This function sets the node's `on_exited` field to a string form of `contents`, which is parsed using `eval_commands` and run when the node is exited. This function can be called by `eval_commands`.

### _advfunc_become(node, new_name)
This function makes it so that all links to the node are redirected to the node corresponding to `new_name`, by setting the node's `replace-with` field to `new_name`. This function can be called by `eval_commands`.

### _advfunc_rm_link(node, *link_text)
Removes the link with the matching text from the node's link list. This function can be called by `eval_commands`.

### _advfunc_rm_text(node, *text)
Removes the line of text from the node's description list. This function can be called by `eval_commands`.

### play(adventure)
Accepts a dictionary of the form `{node_name : node}`, which it uses to run the game.

### edit(file)
Accepts a file name, which is used to load the corresponding adventure (if it exists), and then edit the node using a series of menus. The modified adventure is saved to the file it was loaded from when the function is exited.

### edit_node(node, node_name)
Prints the current state of the node, then provides menus to edit the node's name, description, goto, and links. The function returns the node's name, so that it can be used to update the adventure dictionary.

### edit_link(node, link_text)
Function that edits the link in `node` that matches `link_text`.

### edit_field(current, field_name)
Gets and returns user input, or the value of `current` if input was empty.

### get_input_from_menu(menu_options)
Accepts a list, opens a menu that allows the user to choose between the items, and returns the chosen item.

# Classes

## Node

### description
An array that holds all of the node's description strings.

### links
A dictionary that is of the form `{link_text:target_node}`.

### goto
A string (which should be a node name). When the node is entered, it immediately goes to the node specified by this variable.

### replace_with
Whenever this node is entered, it automatically redirects to the node specified by this variable.

### on_exited
Contains a string of custom code which is run by `eval_commands` when the node is exited.

### __init__(self)
Makes sure that `links` and `description` contain unique objects.

### add_link(self, target, text)
Adds the link to the `links` dictionary.

### remove_link(self, text)
Removes the link from the `links` dictionary, if it exists.

### add_description(self, text)
Adds the text to the `description` list.

### get_description(self)
Returns the `description` list as a string.

### remove_description(self, text)
Removes the `text` string from the `description` list, if it exists.

### exit(self)
Runs the code in `on_exited`.

### print_for_display(self)
Displays node description, links, and goto in a nice, human-readable format.

### get_string(self, node_name)
Returns a string containing the node in a form that can be understood by `eval_commands`. Used for saving the node to a file.

# Writing an Adventure Program

Functions are written in the format `[function_name and all the arguments]`, with each argument separated by a space. The available functions are the ones in the python program preceded by \_advfunc\_. For example, typing `[node START]` would call the `_advfunc_node` function with the argument "START" (which would line up with the "name" parameter).

The adventure starts at the node named START. If a link goes to END, the adventure ends. See the dungeon.adv file or the string in the `load_default_adventure` function for an example of an adventure program.

# Running the Game
Download the adventure.py file and run it. I use `python3 adventure.py` in my command line, but your milage may vary. You could also open it in IDLE and run it that way. Or any other way you can run python v3.12 files.