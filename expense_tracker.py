import json, numpy, math, sys, os
os.system('cls' if os.name == 'nt' else 'clear')
expensefile= os.path.join(os.path.dirname(__file__), "expenselist.json")
if __name__ == "__main__":
    print("JSON", json.__version__)
    print("NUMPY", numpy.__version__)
    print("""
ExpenseTracker/CashFlow:Prototype,0.20 ALPHA
##IN DEVELOPMENT##
##UPDATE NOTES##
-improved sort&calculate code
-more readable help console
-improved view function
          """)

class Expense:
    def __init__(self, _positivity_: bool, _kind_: str, _time_: int, _quantity_: float):
        self.__positivity__ = _positivity_
        self.__kind__ = _kind_
        self.__time__ = _time_
        self.__quantity__ = _quantity_

    def __str__(self):
        return f"{'Income' if self.__positivity__ else 'Expense'},{self.__kind__},{self.__time__}:{self.__quantity__ if self.__positivity__ else self.__quantity__ * -1}"


    @classmethod
    def packer(cls, value: dict):
        return Expense(
            _positivity_=value.get("positivity"),
            _kind_=value.get("kind"),
            _time_=value.get("time"),
            _quantity_=value.get("quantity")
        )

    def unpacker(self):
        return {
            "positivity": self.__positivity__,
            "kind": self.__kind__,
            "time": self.__time__,
            "quantity": self.__quantity__
        }

    def __eq__(self, value):
        if isinstance(value, Expense):
            return (
                self.__positivity__ == value.__positivity__ and
                self.__kind__ == value.__kind__ and
                self.__time__ == value.__time__ and
                self.__quantity__ == value.__quantity__
            )
        return False

class ExpenseTracker:
    def __init__(self):
        self.load(expensefile)

    def load(self, file: str):
        try:
            with open(file, mode="r") as f:
                self.expenselist = [Expense.packer(item) for item in json.load(f)]
                print("Data has been successfully loaded")
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            self.expenselist = []

    def save(self, file: str):
        try:
            with open(file, mode="w") as f:
                json.dump([Expense.unpacker(expense) for expense in self.expenselist], f, indent=4)
            print("Data successfully saved!")
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")

    def calculate(
        self, 
        positivity: bool = None, 
        kind: str = None, 
        time: int = None, 
        quantity: float = None, 
        ranged: bool = False, 
        r1: int = None, 
        r2: int = None
    ):  
        total = 0
        for item in self.filterer(positivity, kind, time, quantity, ranged, r1, r2):
            total += item.__quantity__
            print(item.unpacker())
        return round(total, 2)

    def filterer(
        self, 
        positivity: bool = None, 
        kind: str = None, 
        time: int = None, 
        quantity: float = None, 
        ranged: bool = False, 
        r1: int = None, 
        r2: int = None
    ):  
        sortedlist = self.expenselist

        if positivity is not None:
            sortedlist = [exp for exp in sortedlist if exp.__positivity__ == positivity]
        if kind is not None:
            sortedlist = [exp for exp in sortedlist if exp.__kind__ == kind]
        if time is not None:
            sortedlist = [exp for exp in sortedlist if exp.__time__ == time]
        if quantity is not None and not ranged:
            sortedlist = [exp for exp in sortedlist if exp.__quantity__ == quantity]
        if quantity is None and ranged:
            sortedlist = [exp for exp in sortedlist if r1 <= exp.__quantity__ <= r2]

        return sortedlist

    def sort(self,attribute:str,reverse=bool):
        sorted_out=[]
        sorted_out=sorted(self.expenselist,key=lambda x:getattr(x,f"__{attribute}__"),reverse=reverse)
        
        return sorted_out

    def add(self, file: str, kind: str, time: int, quantity: float, mode: bool):
        item = {
            "positivity": mode,
            "kind": kind,
            "time": time,
            "quantity": float(quantity) if mode else -1 * float(quantity)
        }
        self.expenselist.append(Expense.packer(item))
        print("Data has been stored successfully.")
        self.save(file)

    def delete(self, file: str, kind: str, time: int, quantity: float):
        item = Expense.packer({
            "positivity": True if float(quantity) > 0 else False,
            "kind": kind,
            "time": time,
            "quantity": float(quantity)
        })
        try:
            self.expenselist.remove(item)
            print("No error occurred when removing data from the storage.")
        except Exception as e:
            print(e)
        self.save(file)

    def terminal(self):
        userinput = input(
            "\nWhat would you like to do?\n"
            "Type 'help' to see a list of commands.\n"
            "Enter a command: "
        )

        def delete():
            kind = input("Enter the 'kind' of the expense or income to delete (e.g., 'Groceries', 'Salary'): ")
            time = int(input("Enter the 'time' (year): "))
            quantity = float(input("Enter the 'amount' (positive for income, negative for expense): "))
            self.delete(expensefile, kind, time, quantity)
            self.terminal()

        def add(mode: bool):
            kind = input("Enter the 'kind' of the expense or income (e.g., 'Groceries', 'Salary'): ")
            time = int(input("Enter the 'time' (year): "))
            quantity = float(input("Enter the 'amount' (positive for income, negative for expense): "))
            self.add(expensefile, kind, time, quantity, mode)
            self.terminal()

        def sortvw():
            # print("Leave empty if you don't want to filter based on a parameter.")
            # positivity_input = input("Enter 'True' for income, 'False' for expense, or leave blank: ")
            # kind_input = input("Enter the 'kind' (e.g., 'Groceries', 'Salary'), or leave blank: ")
            # time_input = input("Enter the 'time' (year), or leave blank: ")
            # quantity_input = input("Enter the 'quantity' (amount), or leave blank: ")
            
            # filtered_items = list(
            #     item.unpacker() for item in self.filterer(
            #         positivity=True if positivity_input == "True" else False if positivity_input == "False" else None,
            #         kind=kind_input if kind_input else None,
            #         time=int(time_input) if time_input else None,
            #         quantity=float(quantity_input) if quantity_input else None
            #     )
            # )
            # for item in filtered_items:
            #     print(item)
            # self.terminal()
            print("Enter the attributes to sort by, separated by commas (e.g., 'kind, quantity').")
            sort_input = input("Sort by: ")
            sorted_expenses = self.sort(attribute=sort_input, reverse=True)
            for item in sorted_expenses:
                print(str(item))
            self.terminal()

        def calculate(mode: bool):
            print(self.calculate(positivity=mode))
            self.terminal()

        def save():
            self.save(expensefile)
            self.terminal()

        def load():
            self.load(expensefile)
            self.terminal()

        def view():
            sorted_expenses = self.sort(attribute="quantity", reverse=True)
            for item in sorted_expenses:
                print(str(item))
            self.terminal()

        def clear(term:bool):
            os.system('cls' if os.name == 'nt' else 'clear')
            if term:self.terminal

        def help():
            clear(False)
            print("""
        ExpenseTracker Commands:
        ---------------------------
        - delete / dlt <kind> <time> <amount>   : Remove an expense or income entry based on 'kind', 'time', and 'amount'.
        - add+ <kind> <time> <amount>           : Add an income entry (positive amount). Example: add+ 'Salary' 2023 1500.
        - add- <kind> <time> <amount>           : Add an expense entry (negative amount). Example: add- 'Groceries' 2023 50.
        - calculate+                           : Calculate the total income (positive entries).
        - calculate-                           : Calculate the total expenses (negative entries).
        - calcrange <r1> <r2>                  : Calculate the total income or expense within a specified range of amounts.
        - sortvw                               : View expenses after applying filters (e.g., by positivity, kind, etc.).
        - load / ld                            : Load expenses from 'expenselist.json'.
        - save / sv                            : Save current expenses to 'expenselist.json'.
        - view                                 : Display all expenses and income entries (sorted).
        - clear                                : Clear the terminal screen.
        - exit / ext                           : Exit the application.
        
        Example Commands:
        - add+ 'Salary' 2023 1500
        - add- 'Rent' 2023 800
        - calculate+ (calculate total income)
        - calculate- (calculate total expenses)
            """)
            self.terminal()

        if userinput.casefold() == "clear":
            clear(True)
        elif userinput.casefold() == "save":
            save()
        elif userinput.casefold() == "load":
            load()
        elif userinput.casefold() == "sortvw":
            sortvw()
        elif userinput.casefold() == "calculate+":
            calculate(True)
        elif userinput.casefold() == "calculate-":
            calculate(False)
        elif userinput.casefold() == "calcrange":
            r1 = float(input("Enter the lower range (r1): "))
            r2 = float(input("Enter the upper range (r2): "))
            self.calculate(None, ranged=True, r1=r1, r2=r2)
            self.terminal()
        elif userinput.casefold() == "delete":
            delete()
        elif userinput.casefold() == "add-":
            add(False)
        elif userinput.casefold() == "add+":
            add(True)
        elif userinput.casefold() == "view":
            view()
        elif userinput.casefold() == "help":
            help()
        elif userinput.casefold() == "exit" or userinput.casefold() == "ext":
            print("Exiting application.")
            sys.exit()
        else:
            print("Invalid command. Type 'help' for a list of available commands.")
            self.terminal()
