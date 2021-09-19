import requests
import time
import os
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "accept": "application/json, text/plain, */*"
}

nft_names = {
    "Baller", "Lucky", "Lottie", "Claire", "Syrup Soak",
    "Easter '21 Champions", "Cakeston Easter ‘21", "Flipsie Easter ‘21", "Stormy Easter ‘21", 
    "Bullish", "Hiccup", "Sleepy", "Sunny", "Churro", "Dollop", "Twinkle", "Swapsies", "Drizzle",
    "Blueberries", "Circular", "Sparkle"
}

def load_data(headers, nft_name):
    page_no = 1
    is_ended = False
    price_list = []
    result_list = []

    while not is_ended:
        url = f"https://api.treasureland.market/v2/v1/nft/items?chain_id=0&page_no={page_no}&page_size=40&contract=0xdf7952b35f24acf7fc0487d01c8d5690a60dba07&sort_type=1&"

        response = requests.get(url=url, headers=headers)
        print(f"[#] LOADIND {nft_name} FROM PAGE № {page_no}")
        try:
            data = response.json()["data"]
            list = data["list"]

            if list == None:
                is_ended = True
                break

            for item in list:
                item_name = item["name"]
                item_price = int(item["price"]) / 10**18

                if item_name == nft_name:
                    print(item_name, item_price)
                    price_list.append(item_price)

            page_no = page_no + 1

        except Exception as _ex:
            print(_ex)
        
        
    
    print(f"[#] NFT CALLED {nft_name} IS DOWNLOADED")
    price_list.sort()
    print(price_list)

    result_list.append(
        {
            "nft_name": nft_name,
            "prices": price_list,
            "total_nfts": len(price_list)
        }
    )

    return result_list

def load_data_into_folders(headers):
    date = time.strftime("%x", time.localtime(time.time())).replace("/", ".")

    for nft_name in nft_names:
        result_list = load_data(headers, nft_name)
        if not os.path.exists(f"data/{nft_name}"):
            os.mkdir(f"data/{nft_name}")

        os.mkdir(f"data/{nft_name}/{date}")

        print(f"[#] Folder called ./data/{nft_name}/{date}/ was created")

        with open(f"data/{nft_name}/{date}/result_list.json", "a") as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)
            print("[#] JSON was added into folder")

def main():
    start_time = time.time()

    load_data_into_folders(headers)

    finished_time = time.time() - start_time

    print(f"Work has been done for {finished_time}")

if __name__ == "__main__":
    main()