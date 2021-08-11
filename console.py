#!/usr/bin/python3
"""
    Contains the entry point of the command interpreter
"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv as env


class HBNBCommand(cmd.Cmd):
    """
    class HBNBCommand that contains entry point of command interpreter
    """
    prompt = '(hbnb) '
    classes = {'BaseModel': BaseModel,
               'User': User,
               'State': State,
               'City': City,
               'Amenity': Amenity,
               'Place': Place,
               'Review': Review}

    def emptyline(self):
        """This function shouldn’t execute anything
        """
        pass

    def do_EOF(self, line):
        """End of file to exit the program
        """
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        raise SystemExit

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        else:
            args = args.split(' ')
            if args[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

        new_instance = HBNBCommand.classes[args[0]]()

        # For setting attributes of the new instance.
        for attributes in args[1:]:
            pair = attributes.split('=')
            # Check if its a string.
            if pair[1][0] == '"':
                pair[1] = pair[1][1:-1].replace('"', '\"')
                pair[1] = pair[1].replace('_', ' ')

            # Check if its an integer.
            elif pair[1].isdigit():
                pair[1] = int(pair[1])

            # Check if its a float.
            else:
                try:
                    pair[1] = float(pair[1])
                except:
                    continue

            setattr(new_instance, pair[0], pair[1])

        print(new_instance.id)

        if env("HBNB_TYPE_STORAGE") == "db":
            storage.new(new_instance)
            storage.save()
        else:
            new_instance.save()

    """def do_create(self, line):"""
    """Creates a new instance of BaseModel, saves it and prints the id
        Usage: create <class name>
        """
    """    args = str.split(line)

        if len(args) < 1:
            print("** class name missing **")
            return False

        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        else:
            new_instance = self.classes[args[0]]()
            print(new_instance.id)
            new_instance.save()
            return False"""

    def do_show(self, line):
        """Prints the string representation of an instance based on the class and id
        Usage: show <class name> <id>
        """
        args = str.split(line)
        if len(args) < 1:
            print("** class name missing **")
            return False

        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        all_objects = storage.all()
        obj = args[0] + "." + args[1]

        if obj not in all_objects.keys():
            print("** no instance found **")
        else:
            obj_id = all_objects[obj]
            print(obj_id)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        Usage: destroy <class name> <id>
        """
        args = str.split(line)
        if len(args) < 1:
            print("** class name missing **")
            return False

        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        all_objects = storage.all()
        obj = args[0] + "." + args[1]

        if obj not in all_objects:
            print("** no instance found **")
        else:
            all_objects.pop(obj)
            storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances
        based or not on the class name
        Usage: all
               all <class name>
        """
        args = str.split(line)
        all_objects = storage.all()

        new_list = []
        if len(args) < 1:
            for key, value in all_objects.items():
                new_list.append(str(all_objects[key]))
            print(new_list)

        else:
            if args[0] not in self.classes:
                print("** class doesn't exist **")
                return False

            else:
                for key in all_objects.keys():
                    if args[0] in key:
                        new_list.append(str(all_objects[key]))
                print(new_list)

    def do_update(self, line):
        """Updates an instance based on the class name and
        id by adding or updating attribute
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = line.split()
        all_objects = storage.all()

        if len(args) < 1:
            print("** class name missing **")
            return False

        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        obj = args[0] + "." + args[1]
        if obj not in all_objects:
            print("** no instance found **")
            return False

        if len(args) < 3:
            print("** attribute name missing **")
            return False

        if len(args) < 4:
            print("** value missing **")
            return False

        else:
            new_string = args[3].replace('"', '')
            update_file = all_objects[obj]
            storage.__objects = update_file.__dict__
            storage.__objects[args[2]] = new_string
            print(storage.__objects[args[2]])
            storage.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
