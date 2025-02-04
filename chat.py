# offline_basic_chatbot.py
import json
import time

class MockBackendConnector:
    """Simulates API connections to different backends"""
    
    def __init__(self):
        # Mock database data
        self.crm_data = {
            "customers": [
                {"id": 1, "name": "John Doe", "email": "john@example.com"},
                {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
            ]
        }
        
        self.inventory_data = {
            "products": [
                {"id": 101, "name": "Laptop", "stock": 15},
                {"id": 102, "name": "Phone", "stock": 30}
            ]
        }

    def search_crm(self, keyword):
        """Mock CRM search API"""
        time.sleep(1)  # Simulate API delay
        results = [cust for cust in self.crm_data["customers"] 
                  if keyword.lower() in cust["name"].lower()]
        return json.dumps(results, indent=2)

    def check_inventory(self, product_name):
        """Mock Inventory API"""
        time.sleep(1)  # Simulate API delay
        for product in self.inventory_data["products"]:
            if product_name.lower() in product["name"].lower():
                return json.dumps(product, indent=2)
        return "Product not found"

class BasicChatBot:
    def __init__(self):
        self.api = MockBackendConnector()
        self.rules = {
            "help": self.show_help,
            "exit": lambda: "exit",
            "crm": self.handle_crm,
            "inventory": self.handle_inventory
        }
    
    def show_help(self):
        return """Available commands:
        - Search CRM: [crm/search <name>]
        - Check inventory: [inventory/check <product>]
        - Type 'exit' to quit
        """
    
    def handle_crm(self, command):
        if "search" in command:
            _, _, keyword = command.partition(' ')
            return self.api.search_crm(keyword)
        return "Invalid CRM command"
    
    def handle_inventory(self, command):
        if "check" in command:
            _, _, product = command.partition(' ')
            return self.api.check_inventory(product)
        return "Invalid inventory command"

    def process_command(self, user_input):
        user_input = user_input.lower().strip()
        
        if not user_input:
            return "Please enter a command"
        
        for keyword, handler in self.rules.items():
            if user_input.startswith(keyword):
                if keyword == "exit":
                    return "exit"
                return handler(user_input)
        
        return "Unknown command. Type 'help' for options"

def main():
    bot = BasicChatBot()
    print("=== Offline ChatBot ===")
    print(bot.show_help())
    
    while True:
        try:
            user_input = input("You: ")
            response = bot.process_command(user_input)
            
            if response == "exit":
                print("Bot: Goodbye!")
                break
                
            print(f"Bot: \n{response}")
            
        except KeyboardInterrupt:
            print("\nBot: Session ended")
            break

if __name__ == "__main__":
    main()