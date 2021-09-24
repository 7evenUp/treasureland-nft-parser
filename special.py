import requests
import time
import pprint

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "accept": "application/json, text/plain, */*"
}

nft_names = { "Lucky", "Lottie", "Cakeston Easter ‘21", "Flipsie Easter ‘21" }

def load_data(headers, nft_name):
    page_no = 1
    is_ended = False
    price_list = []
    result_list = []

    while not is_ended:
        url = f"https://api.treasureland.market/v2/v1/nft/items?chain_id=0&page_no={page_no}&page_size=100&contract=0xdf7952b35f24acf7fc0487d01c8d5690a60dba07&sort_type=1&"

        response = requests.get(url=url, headers=headers)
        # print(f"[#] LOADIND {nft_name} FROM PAGE № {page_no}")
        try:
            data = response.json()["data"]
            list = data["list"]

            if list == None:
                is_ended = True
                break

            for item in list:
                item_name = item["name"]

                if item_name == nft_name:
                    item_price = int(item["price"]) / 10**18
                    item_id = item["order_id"]
                    item_nft_id = item["token_id"]
                    # print(item_name, item_price, item_nft_id, item_id)
                    price_list.append(
                        {
                            "item_price": item_price,
                            "url": f"https://www.treasureland.market/assets/0xdf7952b35f24acf7fc0487d01c8d5690a60dba07/{item_nft_id}/{item_id}?chain_id=56"
                        }
                    )

            page_no = page_no + 1

        except Exception as _ex:
            print(_ex)
        
        
    
    print(f"[#] NFT CALLED {nft_name} IS DOWNLOADED")
    newlist = sorted(price_list, key=lambda k: k['item_price'])
    pprint.pprint(newlist[:5])

    result_list.append(
        {
            "nft_name": nft_name,
            "prices": newlist,
            "total_nfts": len(price_list)
        }
    )

    return result_list

def main():
    start_time = time.time()

    for nft_name in nft_names:
        load_data(headers, nft_name)

    

    finished_time = time.time() - start_time

    print(f"Work has been done for {finished_time}")

if __name__ == "__main__":
    main()