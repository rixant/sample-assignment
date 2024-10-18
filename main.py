import pandas as pd

class InvestmentPortfolio:
    def __init__(self, file_path):
        self.file_path = file_path
        self.investments = []
        self.load_data()

    def load_data(self):
        """Load investment data from a CSV file into a list of dictionaries."""
        try:
            df = pd.read_csv(self.file_path)
            for index, row in df.iterrows():
                investment = {
                    'Asset': row['Asset'],
                    'Quantity': row['Quantity'],
                    'Purchase_Price': row['Purchase_Price'],
                    'Current_Price': row['Current_Price'],
                    'Asset_Type': row['Asset_Type']
                }
                self.investments.append(investment)
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            exit()
        except pd.errors.EmptyDataError:
            print("No data found in the file.")
            exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            exit()

    def add_investment(self):
        """Add a new investment to the portfolio."""
        asset = input("Enter the asset name: ").strip()
        quantity = float(input("Enter the quantity: "))
        purchase_price = float(input("Enter the purchase price: "))
        current_price = float(input("Enter the current price: "))
        asset_type = input("Enter the asset type (e.g., Stock, Bond, ETF): ").strip()

        investment = {
            'Asset': asset,
            'Quantity': quantity,
            'Purchase_Price': purchase_price,
            'Current_Price': current_price,
            'Asset_Type': asset_type
        }
        self.investments.append(investment)
        print(f"Investment in {asset} added successfully!")

    def calculate_returns(self):
        """Calculate total and individual returns for investments."""
        total_invested = 0
        total_current_value = 0
        returns = {}

        for investment in self.investments:
            quantity = investment['Quantity']
            purchase_price = investment['Purchase_Price']
            current_price = investment['Current_Price']

            invested = quantity * purchase_price
            current_value = quantity * current_price
            percent_return = ((current_value - invested) / invested) * 100 if invested > 0 else 0

            returns[investment['Asset']] = (invested, current_value, current_value - invested, percent_return)
            total_invested += invested
            total_current_value += current_value

        return returns, total_invested, total_current_value

    def asset_allocation(self):
        """Show asset allocation by asset type."""
        allocation = {}
        for investment in self.investments:
            asset_type = investment['Asset_Type']
            current_value = investment['Quantity'] * investment['Current_Price']
            allocation[asset_type] = allocation.get(asset_type, 0) + current_value
        
        return allocation

    def visualize_portfolio(self):
        """Display portfolio details in a user-friendly format."""
        returns, total_invested, total_current_value = self.calculate_returns()
        print("\nInvestment Returns:")
        for asset, data in returns.items():
            invested, current_value, return_value, percent_return = data
            print(f"{asset}: Invested ${invested:.2f}, Current Value ${current_value:.2f}, "
                  f"Return ${return_value:.2f}, Percentage Return {percent_return:.2f}%")

        print(f"\nTotal Invested: ${total_invested:.2f}")
        print(f"Total Current Value: ${total_current_value:.2f}")
        print(f"Overall Return: ${total_current_value - total_invested:.2f}")

    def main(self):
        print("Welcome to the Enhanced Investment Portfolio Manager!")
        while True:
            print("\nOptions:")
            options = {
                "1": "View Returns",
                "2": "View Asset Allocation",
                "3": "Add New Investment",
                "4": "Visualize Portfolio",
                "5": "Exit"
            }
            for key, value in options.items():
                print(f"{key}. {value}")

            choice = input("Choose an option (1-5): ").strip()
            if choice == '1':
                self.visualize_portfolio()
            elif choice == '2':
                allocation = self.asset_allocation()
                print("\nAsset Allocation:")
                for asset_type, value in allocation.items():
                    print(f"{asset_type}: ${value:.2f}")
            elif choice == '3':
                self.add_investment()
            elif choice == '4':
                self.visualize_portfolio()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    file_path = 'investments.csv'  # Path to your CSV file
    portfolio = InvestmentPortfolio(file_path)
    portfolio.main()
