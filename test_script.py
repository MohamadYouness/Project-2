import requests
import sys
import re


# the project was done using several functions. According to chatgpt, writing the code as functions is more efficient since it breaks the code into smaller and managebale pieces 
def make_request(url):
    # it is a function that enables us to make request to get acces to the URL
    try:
        return requests.get("http://" + url, timeout=5)
    except:
        pass
    try:
        return requests.get("https://" + url, timeout=5)
    except:
        pass


def get_subdomains(url):
    # a method that makes a dictionary for the subdomaines 
    # if the url is valid, it is written in the output.txt file
    with open("subdomains.txt") as file, open("subdomains_output.txt", "w") as output_file: 
        for line in file:
            word = line.strip()
            target = word + "." + url
            subdomains_response = make_request(target)
            if subdomains_response:
                output_file.write(target + "\n")


def get_directories(url):
    # same as get_subdomains but for directories
    with open("dirs.txt") as file, open("directories_output.txt", "w") as output_file:
        for line in file:
            word = line.strip()
            target = url + "/" + word
            directories_response = make_request(target)
            if directories_response:
                output_file.write(target + "\n")


def get_files(url):
    # a method that makes a dictionary for the files 
    # if the url is valid, it is written in the output.txt file    
    with open("files_output.txt", "a") as output_file:
        response = make_request(url)
        if not response:
            return
        html_content = response.content.decode("latin-1")
        files_links = re.findall('(?:href=")(.*?)"', html_content)
        for file in files_links:
            testing_response = make_request(file)
            if testing_response and testing_response.status_code == 200:
                if check_domain(url, file):
                    get_files(file)
            else:
                try:
                    testing_response = requests.get(file)
                    if not testing_response:
                        link = url + "/" + file
                        output_file.write(link + "\n")
                except:
                    link = url + "/" + file
                    output_file.write(link + "\n")


def check_domain(main_domain, url):
    # method that checks if the main domain is in the given URL
    return main_domain in url


if __name__ == "__main__":
    # getting the url from command line arguments and check if it is aa valid one
    url = sys.argv[1]
    response = make_request(url)
    if not response:
        print("Invalid URL!")
        sys.exit(0)

    # checking files and subdirectories on the URL after clearing the file
    with open("files_output.txt", "w"):
        pass
    get_files(url)
