import requests
import time
import pprint

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "accept": "application/json, text/plain, */*"
}

nft_names = { "Flipsie Easter ‘21", "Stormy Easter ‘21" }
# nft_names = { "Syrup Soak" }

def load_data():
    page_no = 1
    is_ended = False
    result_dict = {}

    while not is_ended:
        url = f"https://api.treasureland.market/v2/v1/nft/items?chain_id=0&page_no={page_no}&page_size=100&contract=0xdf7952b35f24acf7fc0487d01c8d5690a60dba07&sort_type=1&"

        response = requests.get(url=url, headers=headers)
        if page_no % 5 == 0:
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
                    item_id = item["order_id"]
                    item_nft_id = item["token_id"]
                    # print(item["name"], item_price, item_nft_id, item_id)

                    if result_dict.get(item["name"]):
                        prices_list = result_dict[str(item["name"])]
                        prices_list.append(
                            {
                                "item_price": item_price,
                                "url": f"https://www.treasureland.market/assets/0xdf7952b35f24acf7fc0487d01c8d5690a60dba07/{item_nft_id}/{item_id}?chain_id=56"
                            }
                        )
                    else:
                        result_dict[item["name"]] = [
                            {
                                "item_price": item_price,
                                "url": f"https://www.treasureland.market/assets/0xdf7952b35f24acf7fc0487d01c8d5690a60dba07/{item_nft_id}/{item_id}?chain_id=56"
                            }
                        ]

            page_no = page_no + 1

        except Exception as _ex:
            print(_ex)
        
        
    
    print(f"[#] NFTs ARE DOWNLOADED")
    
    return result_dict

def main():
    count = 0
    while True:
        start_time = time.time()

        result = load_data()

        for key in result.keys():
            new_list = sorted(result[key], key=lambda k:k['item_price'])
            print(key)
            pprint.pprint(new_list[:3])

        finished_time = time.time() - start_time

        print(f"Work has been done for {finished_time}")

        count = count + 1
        print(f"Total fetchings: {count}")

if __name__ == "__main__":
    main()