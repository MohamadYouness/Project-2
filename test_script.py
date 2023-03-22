import requests
import sys
import re

def make_request(url):
    try:
        return requests.get("http://" + url, timeout=5)
    except:
        pass
    try:
        return requests.get("https://" + url, timeout=5)
    except:
        pass

def get_subdomains(url):
    with open("subdomains.txt") as sub_file, open("subdomains_output.txt", "w") as out_file:
        for line in sub_file:
            word = line.strip()
            target = word + "." + url
            sub_response = make_request(target)
            if sub_response:
                out_file.write(target + "\n")

def get_directories(url):
    with open("directories.txt") as dir_file, open("directories_output.txt", "w") as out_file:
        for line in dir_file:
            word = line.strip()
            target = url + "/" + word
            dir_response = make_request(target)
            if dir_response:
                out_file.write(target + "\n")

def get_files(url):
    with open("files_output.txt", "a") as out_file:
        response = make_request(url)
        if not response:
            return
        html_content = response.content.decode("latin-1")
        files_links = re.findall('(?:href=")(.*?)"', html_content)
        for file_link in files_links:
            testing_response = make_request(file_link)
            if testing_response and testing_response.status_code == 200:
                if check_domain(url, file_link):
                    get_files(file_link)
            else:
                try:
                    testing_response = requests.get(file_link)
                    if not testing_response:
                        link = url + "/" + file_link
                        out_file.write(link + "\n")
                except:
                    link = url + "/" + file_link
                    out_file.write(link + "\n")

def check_domain(main_domain, url):
    return main_domain in url

if __name__ == "__main__":
    target_url = sys.argv[1]
    response = make_request(target_url)
    if not response:
        print("Invalid URL!")
        sys.exit(0)

    with open("files_output.txt", "w"):
        pass  # clear file
    get_files(target_url)
    get_subdomains(target_url)
    get_directories(target_url)
    
    print("Scan completed successfully!")
