import argparse
import requests
import re

def banner():
    print(r"""
                                                                    
                                                  .--,-``-.     
    ,----..                    ,----,            /   /     '.   
   /   /   \                 .'   .' \     ,---,/ ../        ;  
  /   .     :              ,----,'    |  ,---.'|\ ``\  .`-    ' 
 .   /   ;.  \,--,  ,--,   |    :  .  ;  |   | : \___\/   \   : 
.   ;   /  ` ;|'. \/ .`|   ;    |.'  /   |   | |      \   :   | 
;   |  ; \ ; |'  \/  / ;   `----'/  ;  ,--.__| |      /  /   /  
|   :  | ; | ' \  \.' /      /  ;  /  /   ,'   |      \  \   \  
.   |  ' ' ' :  \  ;  ;     ;  /  /-,.   '  /  |  ___ /   :   | 
'   ;  \; /  | / \  \  \   /  /  /.`|'   ; |:  | /   /\   /   : 
 \   \  ',  /./__;   ;  \./__;      :|   | '/  '/ ,,/  ',-    . 
  ;   :    / |   :/\  \ ;|   :    .' |   :    :|\ ''\        ;  
   \   \ .'  `---'  `--` ;   | .'     \   \  /   \   \     .'   
    `---`                `---'         `----'     `--`-,,-'     
                                                                
    """)
def fetch_subdomains(domain):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list?limit=100&page=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        urls = [item['url'] for item in data.get('url_list', [])]
        return urls
    except requests.RequestException as e:
        print(f"Request Failed: {e}")
        return []

def extract_subdomains(urls, mode):
    subdomains = set()
    for url in urls:
        match = re.search(r"https?://([a-zA-Z0-9.-]+)", url)
        if match:
            full_domain = match.group(1)
            if mode == 1:
                subdomains.add(f"http://{full_domain}")
            elif mode == 2:
                parts = full_domain.split('.')
                if len(parts) > 2:
                    subdomains.add(parts[0])
    return subdomains

def save_to_file(subdomains, output_file):
    with open(output_file, "w") as f:
        for subdomain in subdomains:
            f.write(subdomain + "\n")
    print(f"save to : {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Subdomain find through AlienVault OTX API",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--domain", required=True, help="Specify the domain to query, e.g., baidu.com")
    parser.add_argument("-m", type=int, choices=[1, 2], required=True, help=(
        "Choose extraction mode：\n"
        "  1 - Return the full URL, e.g., http://example.example.com\n"
        "  2 - Return the subdomain prefix, e.g., example"
    ))
    parser.add_argument("-o", help="(Optional) Specify the output file path to save the results to a text file")

    args = parser.parse_args()

    urls = fetch_subdomains(args.domain)
    if not urls:
        print("Get Nothing，Please Check it")
        return

    subdomains = extract_subdomains(urls, args.m)
    for subdomain in subdomains:
        print(subdomain)

    if args.o:
        save_to_file(subdomains, args.o)

if __name__ == "__main__":
    banner()
    main()