#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
from shlex import split
from models import storage
from sqlalchemy.ext.declarative import declarative_base

class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = [
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    ]

    def emptyline(self):
        """Ignore empty spaces."""
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Create a new class instance with given keys/values and print its id.

        Usage: create <class> <key1>=<value1> <key2>=<value2> ...
        """
        try:
            if not line:
                raise SyntaxError()

            args = split(line)
            class_name = args[0]

            if class_name not in self.__classes:
                raise NameError()

            kwargs = {}
            for arg in args[1:]:
                key, value = arg.split("=")
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            obj = storage.create(class_name, **kwargs)
            print(obj.id)

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Print the string representation of an instance.

        Usage: show <class> <id>
        """
        try:
            if not line:
                raise SyntaxError()

            args = split(line)
            class_name = args[0]

            if class_name not in self.__classes:
                raise NameError()

            obj_id = args[1]
            obj = storage.get(class_name, obj_id)

            if obj:
                print(obj)
            else:
                raise KeyError()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.

        Usage: destroy <class> <id>
        """
        try:
            if not line:
                raise SyntaxError()

            args = split(line)
            class_name = args[0]

            if class_name not in self.__classes:
                raise NameError()

            obj_id = args[1]
            obj = storage.get(class_name, obj_id)

            if obj:
                obj.delete()
                storage.save()
            else:
                raise KeyError()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """Display string representations of all instances of a given class.

        Usage: all [<class>]
        """
        args = split(line)
        if args and args[0] not in self.__classes:
            print("** class doesn't exist **")
            return

        objects = []
        if args:
            class_name = args[0]
            objects = storage.all(class_name)
        else:
            objects = storage.all()

        print([str(obj) for obj in objects])

    def do_update(self, line):
        """Updates an instance by adding or updating an attribute.

        Usage: update <class> <id> <attribute name> "<attribute value>"
        """
        try:
            if not line:
                raise SyntaxError()

            args = split(line)
            class_name = args[0]

            if class_name not in self.__classes:
                raise NameError()

            obj_id = args[1]
            attribute_name = args[2]
            attribute_value = args[3]

            obj = storage.get(class_name, obj_id)

            if obj:
                setattr(obj, attribute_name, attribute_value)
                storage.save()
            else:
                raise KeyError()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_count(self, line):
        """Count the number of instances of a class.

        Usage: count <class>
        """
        try:
            if not line:
                raise SyntaxError()

            class_name = line

            if class_name not in self.__classes:
                raise NameError()

            count = storage.count(class_name)
            print(count)

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
