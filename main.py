import requests
import time
import os
import json
import shutil

nft_names = {
    "Baller", "Lucky", "Lottie", "Claire", "Syrup Soak",
    "Easter '21 Champions", "Cakeston Easter ‘21", "Flipsie Easter ‘21", "Stormy Easter ‘21", 
    "Bullish", "Hiccup", "Swapsies", "Drizzle",
    "Blueberries", "Circular", "Sparkle", "Panurai"
}

def load_data():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "accept": "application/json, text/plain, */*"
    }
    page_no = 1
    is_ended = False
    result_dict = {}

    while not is_ended:
        url = f"https://api.treasureland.market/v2/v1/nft/items?chain_id=0&page_no={page_no}&page_size=50&contract=0xdf7952b35f24acf7fc0487d01c8d5690a60dba07&sort_type=1&"

        response = requests.get(url=url, headers=headers)
        print(f"[#] LOADIND FROM PAGE № {page_no}")
        try:
            data = response.json()["data"]
            list = data["list"]

            if list == None:
                is_ended = True
                break

            for item in list:
                if item["name"] in nft_names:
                    item_price = int(item["price"]) / 10**18

                    if result_dict.get(item["name"]):
                        prices_list = result_dict[str(item["name"])]
                        prices_list.append(item_price)
                    else:
                        result_dict[item["name"]] = [item_price]
                    
                    
                    # print(item["name"], item_price)

            page_no = page_no + 1

        except Exception as _ex:
            print(_ex)
        
    print(f"[#] NFTs ARE DOWNLOADED")

    return result_dict

def load_data_into_folders(nfts_list):
    date = time.strftime("%x", time.localtime(time.time())).replace("/", ".")

    for nft_name in nfts_list:
        result_list = [{
            "nft_name": nft_name,
            "prices": nfts_list[nft_name],
            "total_nfts": len(nfts_list[nft_name])
        }]

        if not os.path.exists(f"data/{nft_name}"):
            os.mkdir(f"data/{nft_name}")

        if os.path.exists(f"data/{nft_name}/{date}"):
            shutil.rmtree(f"data/{nft_name}/{date}")
            print("[#] Folder was deleted")

        os.mkdir(f"data/{nft_name}/{date}")

        print(f"[#] Folder called ./data/{nft_name}/{date}/ was created")

        with open(f"data/{nft_name}/{date}/result_list.json", "a") as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)
            print("[#] JSON was added into folder")

def main():
    start_time = time.time()

    result = load_data()

    for key in result.keys():
        result[key].sort()

    load_data_into_folders(result)

    finished_time = time.time() - start_time

    print(f"Work has been done for {finished_time}")

if __name__ == "__main__":
    main()
