'''
    J.
    November 29th, 2019
'''
from room import *
import pickle

def main():
    game = Game()
    game.play_game()

class Game():
    def __init__(self):
        '''
            Function: __init__
            Parameter: none
            Return: none
            Purpose: constructing the Game class
        '''
        self.room_dict = self.read_rooms()
        self.item_dict = self.read_items()
        self.pm_dict = self.read_puzzles_n_monsters()
        self.inventory = {}
        self.starting_room = 1
     
    def play_game(self):
        '''
            Function: play_game
            Parameter: none
            Return: none
            Purpose: play the main game
        '''
        # game opening message
        print("Welcome to the old-school adventure game - Room!")
        print("1. Start a new game\n2. Load saved game and continue")
        choice = input("> ")
        while choice != "1" and choice != "2":
            print("Sorry what was that???")
            choice = input("Please correctly enter 1 or 2 > ")

        # player chooses to start a new game
        if choice == "1":
            self.walk_around()

        # player opts to continue from a saved game
        else:
            game_loaded = self.load_game_data()
            self.walk_around()

    def read_rooms(self, filename = "aquest_rooms.txt"):
        '''
            Function: read_room
            Parameter: name of the room file (str)
            Return: the room data (dict)
            Purpose: read the room file and store them as Room objects
                in a dictionary 
        '''
        room_object_dict = dict()
        try:
            infile = open(filename, "r")
            line = infile.readline()
            line = line.strip("\n")
            line = infile.readline()

            while line != "":
                line = line.strip("\n")
                lst = line.split("|")

                number = lst[0]
                number = int(number)
                name = lst[1]
                description = lst[2]
                
                adjacent_temp = lst[3]
                adjacent_list = adjacent_temp.split(" ")
                adjacent = []
                for i in range(len(adjacent_list)):
                    num = int(adjacent_list[i])
                    adjacent.append(num)
                
                picture = lst[-1]

                # instantiate the room
                room = Room(number, name, description, adjacent, picture)
                
                puzzles = lst[4].upper()
                if puzzles != "NONE":
                    if "," in puzzles:
                        puzzles = puzzles.split(",")
                        for p in puzzles:
                            room.add_puzzle(p.upper())
                    else:
                        room.add_puzzle(puzzles.upper())

                monsters = lst[5].upper()
                if monsters != "NONE":
                    if "," in monsters:
                        monsters = monsters.split(",")
                        for m in monsters:
                            room.add_monster(m.upper())
                    else:
                        room.add_monster(monsters.upper())
                
                items = lst[6].upper()
                if items != "NONE":
                    if "," in items:
                        items = items.split(",")
                        for i in items:
                            room.add_item(i.upper())
                    else:
                        room.add_item(items.upper())

                # add the room object to the dictionary
                room_object_dict[number] = room

                # read the next line
                line = infile.readline()  
            infile.close()
        except FileNotFoundError:
            print(filename, "cannot be found!")
        except:
            print(filename, "cannot be read!")
        finally:
            return room_object_dict
        
    def read_items(self, filename = "aquest_items.txt"):
        '''
            Function: read_items
            Parameter: the name of the file
            Return: item data read from the file (dict)
            Purpose: read the item file and store them as Item objects
                in a dictionary 
        '''
        item_object_dict = dict()
        try:
            infile = open(filename, "r")
            line = infile.readline()
            line = line.strip("\n")
            line = infile.readline()

            while line != "":
                line = line.strip("\n")
                lst = line.split("|")

                number = int(lst[0])
                name = lst[1]
                description = lst[2]
                weight = int(lst[3])
                value = int(lst[4])
                use_remaining = int(lst[5])

                # instantiate the item object              
                item = Item(number, name, description, weight, value,
                            use_remaining)

                # add the item object to the dictionary
                item_object_dict[name.upper()] = item

                # read the next line
                line = infile.readline()
            infile.close()
        except FileNotFoundError:
            print(filename, "cannot be found!")
        except:
            print(filename, "cannot be read!")
        finally:
            return item_object_dict

    def read_puzzles_n_monsters(self, filename = "puzzles_n_monsters.txt"):
        '''
            Function: read_puzzles_n_monsters
            Parameter: the name of the file
            Return: puzzle and monster data read from the file (dict)
            Purpose: read the puzzle and monster data from the file, and
                store them as Monster objects in a dictionary
        '''
        pm_object_dict = dict()
        try:
            infile = open(filename, "r")
            line = infile.readline()
            line = line.strip("\n")
            line = infile.readline()

            while line != "":
                line = line.strip("\n")
                lst = line.split("|")

                name = lst[0]
                description = lst[1]
                
                active = lst[2]
                if active == "T":
                    active = True
                else:
                    active = False
                    
                affects_target = lst[3]
                if affects_target == "T":
                    affects_target = True
                else:
                    affects_target = False
                    
                solution = lst[4]
                target = lst[5] 
                effect = lst[6]
                
                can_attack = lst[7]
                if can_attack == "T":
                    can_attack = True
                else:
                    can_attack = False
                    
                attack = lst[8]

                # instantiate a monster(or puzzle) object
                pm = Monster(name, description, target, active, 
                             affects_target, solution, effect,
                             can_attack, attack)

                # add the object to the dictionary
                pm_object_dict[name.upper()] = pm

                # then read the next line
                line = infile.readline()
            infile.close()
        except FileNotFoundError:
            print(filename, "cannot be found!")
        except:
            print(filename, "cannot be read!")
        finally:
            return pm_object_dict

    def walk_if_you_can(self, current_room, rooms, choice):
        '''
            Function: walk_if_you_can
            Parameter: current room number (int), adjacent room numbers (list),
                choice from the menu (str)
            Return: updated room number (int)
            Purpose: try to walk into certain rooms
        '''
        directions = 'NSEW'
        index = directions.index(choice)
        room_number = rooms[index]

        # hit the wall
        if room_number == 0:
            print("\n--->> You cannot go in that direction! <<---\n")
            return current_room
        
        # puzzles/monsters blocking the way
        elif room_number < 0:
            print("You cannot proceed in that direction YET.")
            return current_room
        
        # can walk in this direction
        else:
            updated_room_name = (self.room_dict[room_number]).name
            print("-" * 6, "\nYou are now in the:", updated_room_name)

            # block regular rm description by monster and puzzle descriptions
            puzzle_active = False
            monster_active = False
            if self.room_dict[room_number].has_puzzles():
                p = self.room_dict[room_number].puzzles[0]
                if self.pm_dict[p].active:
                    print(self.pm_dict[p].effect)
                    puzzle_active = True
            if self.room_dict[room_number].has_monsters():
                m = self.room_dict[room_number].monsters[0]
                if self.pm_dict[m].active:
                    print(self.pm_dict[m].effect)
                    print(self.pm_dict[m].attack)
                    monster_active = True
                    
            # print regular room description if there's no puzzle or monster
            # in the room
            if not puzzle_active and not monster_active:
                print(self.room_dict[room_number].description)
        
            # display the items in the room
            self.display_room_items(room_number)
        
            return room_number
      
    def walk_around(self):
        '''
            Function: walk_around
            Parameter: none
            Return: none
            Purpose: walk around the rooms
        '''
        current_room = self.starting_room
        print("=" * 6, "\nYou are starting in the:",
              self.room_dict[current_room].name)
        print(self.room_dict[current_room].description)
        self.display_room_items(current_room)
        msg = ('\nEnter N, S, E or W to move in those directions\n'
               + "I for inventory\n"
               + "L to look at something\n"
               + "U to use an item\n"
               + "T to take an item\n"
               + "D to drop an item\n"
               + "or Q to quit and exit the game\n> ")
        choice = self.get_menu_choice(msg)
        
        # until the player quits, let them wander around
        while True:
            # OPTION 1:
            # move to a different room
            if (choice == "N" or choice == "S"
                or choice == "E" or choice == "W"):
                rooms = self.room_dict[current_room].adjacent_rooms
                current_room = self.walk_if_you_can(current_room,
                                               rooms, choice)
                
            # OPTION 2:
            # show inventory
            elif choice == "I":
                discard = self.show_inventory()
                
            # OPTION 3:
            # look at an item in the room
            elif choice == "L":
                # look at an item
                if self.room_dict[current_room].has_items():
                    self.display_room_items(current_room)
                    item = input("What do you want to examine > ")
                    while (item.upper() not in
                           self.room_dict[current_room].items):
                        print("There's nothing like that around.")
                        item = input("What do you want to examine > ")
                    print(self.item_dict[item.upper()].description)
                # if there's no item in the room
                else:
                    print("There is nothing to examine in this room.")
                
            # OPTION 4:    
            # use an item on an puzzle or monster in the room
            elif choice == "U":
                inventory_not_empty = self.show_inventory()
                if inventory_not_empty:
                    item = input("Which item would you "
                                             + "like to use > ")
                    while item.upper() not in self.inventory:
                        print("You do not have this item in your inventory.")
                        item = input("Which item would you "
                                             + "like to use > ")
                    discard, can_use = self.inventory[item.upper()].use()
                    
                    # if item can be used
                    if can_use:
                        # decresed the remaining amount by 1
                        self.inventory[item.upper()].use_remaining -= 1
                        solved = False
                        if (self.room_dict[current_room].has_puzzles()
                            or self.room_dict[current_room].has_monsters()):
                            pm_list = (self.room_dict[current_room].puzzles +
                                       self.room_dict[current_room].monsters)
                            for pm in pm_list:
                                if self.pm_dict[pm].active:
                                    solved = (self.pm_dict[pm].try_to_solve
                                              (item.upper()))
                                    # if puzzle/monster is solved
                                    if solved:
                                        (self.room_dict[current_room].
                                         reverse_effects())
                                        print("Success! You used the",
                                              item.upper(), "on the",
                                              pm)
                                        print("\nYou are still in the:",
                                              self.room_dict[current_room].name)
                                        print(self.room_dict[current_room].
                                              description)
                                        self.display_room_items(current_room)
                                        break
                                    
                        # if item did not work on the puzzle/monster
                        if not solved:
                            print("There was no effect. The item didn't work")

                    # there isn't enough of this item left to use
                    else:
                        print("You do not any of", item.upper(), "left")
                        
                # the inventory is empty
                else:
                    print("You have no item to use.")
                
            # OPTION 5:
            # take an item from the room and put it in the inventory
            elif choice == "T":
                if self.room_dict[current_room].has_items():
                    item = input("Which item would you "
                                             + "like to take > ")
                    while (item.upper() not in
                           self.room_dict[current_room].items):
                        print("The item is not availible in this room.")
                        item = input("Which item would you "
                                             + "like to take > ")
                        
                    # the maximum weight is 10 units
                    weight = 0
                    for i in self.inventory.values():
                        weight += i.weight
                    weight += self.item_dict[item.upper()].weight
                    if weight > 10:
                        print("Your bag is too full for this item!\n" +
                              "Drop an item from your bag if you want to take "
                              + item.upper())
                        
                    # add the item in the inventory
                    else:
                        self.room_dict[current_room].items.remove(item.upper())
                        value = self.item_dict.pop(item.upper())
                        self.inventory[item.upper()] = value
                        print(item.upper(), "has been added to the inventory")
                        
                # if there is no item in the room
                else:
                    print("There is no item in this room.")

            # OPTION 6:
            # drop an item in the current room
            elif choice == "D":
                inventory_not_empty = self.show_inventory()
                if inventory_not_empty:
                    item = input("Which item would you "
                                             + "like to drop > ")
                    while item.upper() not in self.inventory:
                        print("The item does not exist in your inventory.")
                        item = input("Which item would you "
                                             + "like to drop > ")
                    value = self.inventory.pop(item.upper())
                    self.item_dict[item.upper()] = value
                    self.room_dict[current_room].add_item(item.upper())
                    print(item.upper(), "has been dropped")
                    
                # there is no item in the inventory 
                else:
                    print("You have nothing to drop.")
                
            # OPTION 7:
            # quit if the player enters Q (or q)   
            else:
                # GAME ENDING
                # determine score
                score = 0
                for i in self.inventory.values():
                    score += i.value
                    
                # determine ranking
                if score <= 100:
                    rank = "Newbie"
                elif score <= 200:
                    rank = "Go-getter"
                elif score < 1000:
                    rank = "Overachiever"
                else:
                    rank = "Professional"
                    
                # display result
                print("=" * 6, "\nYou left the rooms. Here are your game results:\n")
                print("Score:", score)
                print("Ranking:", rank)
                
                # prompt the player to save the game progress
                save = input("\nWould you like save your game progress?\n" +
                             "(Y for yes, and N for no) > ")
                while save.upper() != "Y" and save.upper() != "N":
                    save = input("Please enter a valid letter > ")
                if save.upper() == "Y":
                    self.starting_room = current_room
                    self.save_game_data()
                    
                # end of the game
                print("\nThanks for playing :)")

                # break out of the while-loop (and game)
                break

            choice = self.get_menu_choice(msg)
            
    
    def get_menu_choice(self, message):
        '''
            Function: get_menu_choice
            Parameter: menu message to be displayed (str)
            Return: menu choice in uppercase (str)
            Purpose: display the menu to the player and get their choice
        '''
        choice = input(message)
        choice = choice.upper()

        while (choice != "N"
            and choice != "S"
            and choice != "E"
            and choice != "W"
            and choice != "I"
            and choice != "L"
            and choice != "U"
            and choice != "T"
            and choice != "D"
            and choice != "Q"):
            choice = input("Please enter a valid choice:\n> ")
            choice = choice.upper()

        return choice
    
    def show_inventory(self):
        '''
            Function: show_inventory
            Parameter: none
            Return: if there is item in the the inventory (boolean)
            Purpose: check there is any item in the inventory
        '''
        # empty inventory
        if self.inventory == {}:
            print("Your current inventory is empty.")
            return False

        # inventory is not empty and show the items inside
        else:
            print("Current Inventory:")
            print(" | ".join(self.inventory))
            return True
        
    def display_room_items(self, room_number):
        '''
            Function: display_room_items
            Parameter: current room number (int)
            Return: none
            Purpose: display the items in the current room (if there's any)
        '''
        if self.room_dict[room_number].has_items():
            if self.room_dict[room_number].has_items():
                item_list = self.room_dict[room_number].items
                for i in item_list:
                    print("A", i, "is here in the room")
        
    def load_game_data(self):
        '''
            Function: load_game_data
            Parameter: none
            Return: none
            Purpose: load game data from local pc txt files
        '''
        try:
            infile1 = open("savedata1_room", "rb")
            infile2 = open("savedata2_item", "rb")
            infile3 = open("savedata3_pm", "rb")
            infile4 = open("savedata4_inventory", "rb")
            infile5 = open("savedata5_starting_room", "rb")

            self.room_dict = pickle.load(infile1)
            self.item_dict = pickle.load(infile2)
            self.pm_dict = pickle.load(infile3)
            self.inventory = pickle.load(infile4)
            self.starting_room = pickle.load(infile5)

            infile1.close()
            infile2.close()
            infile3.close()
            infile4.close()
            infile5.close()
        except:
            print("Savedata cannot be loaded. Starting a new game...")
        
    def save_game_data(self):
        '''
            Function: save_game_data
            Parameter: none
            Return: none
            Purpose: save the game progress to local pc files
        '''
        outfile1 = open("savedata1_room", "wb")
        outfile2 = open("savedata2_item", "wb")
        outfile3 = open("savedata3_pm", "wb")
        outfile4 = open("savedata4_inventory", "wb")
        outfile5 = open("savedata5_starting_room", "wb")

        pickle.dump(self.room_dict, outfile1)
        pickle.dump(self.item_dict, outfile2)
        pickle.dump(self.pm_dict, outfile3)
        pickle.dump(self.inventory, outfile4)
        pickle.dump(self.starting_room, outfile5)

        outfile1.close()
        outfile2.close()
        outfile3.close()
        outfile4.close()
        outfile5.close()

        print("Saving...Your progress is saved! Hope to see you again soon!")

main()    
    
