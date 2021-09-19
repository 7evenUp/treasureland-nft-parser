import os
import json

def main():
    for dirname in os.listdir('./data'):
        # if dirname == "Claire" or dirname == "Stormy Easter ‘21" or dirname == "Syrup Soak":
            print('- - - - - - - - - - - - - - - - - - - - - - - - - - - -')
            print(dirname)
            for date_dirname in os.listdir(f"./data/{dirname}"):
                f = open(f"./data/{dirname}/{date_dirname}/result_list.json")
                data = json.load(f)

                first_five_prices = data[0]["prices"][:5]

                print(date_dirname, ' | ', first_five_prices)
                
        

if __name__ == "__main__":
    main()