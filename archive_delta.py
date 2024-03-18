import os
import sys
import requests

years = [x for x in range(1974, 2025)]
months = [x for x in range(1, 13)]

def main():
    argv = sys.argv

    if len(argv) > 1 and argv[1].lower() == "all":
        download_all_deltas()
    elif len(argv) == 3:
        if argv[1].lower() == "-y" and int(argv[2]) in years:
            print(f"downloading all months for year {argv[2]}") 
            download_deltas([int(argv[2])])
    elif len(argv) == 5 and \
        argv[1].lower() == "-y" and int(argv[2]) in years \
        and argv[3].lower() == "-m" and int(argv[4]) in months:
            print(f"downloading delta {argv[2]}/{argv[4]}")
            download_deltas([int(argv[2])], [int(argv[4])])
    else:
        sys.exit("Proper syntax: archive_delta.py all | -y <year> -m <month>\nyear: 1974-2024, month: 1-12")
        
    

def download_all_deltas():
    urls, save_paths, pdf_names = make_params(years, months) 

    if len(urls) != len(pdf_names) or len(save_paths) != len(pdf_names):
        raise RuntimeError("3 lists are not of the same length, exiting.")

    for i in range(len(urls)):
        download_delta(urls[i], save_paths[i], pdf_names[i])

def download_deltas(year, month=months):
    urls, save_paths, pdf_names = make_params(year, month)
    for i in range(len(urls)):
        download_delta(urls[i], save_paths[i], pdf_names[i])

def download_delta(url, save_path, pdf_name):
    response = requests.get(url)
    if response.status_code == 200:
        if not os.path.exists(save_path):
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"PDF: {pdf_name} downloaded successfully.")
        else:
            print(f"File {save_path} already exists. Skipping.")
    else:
        print(f"Failed to download PDF: {pdf_name}. Status code:", response.status_code)

def make_params(year, month):
    pdf_names = [f"delta-{y}-{m:02d}.pdf" for y in year for m in month]
    urls =  [f"https://deltami.edu.pl/media/issues/{pdf_name[6:10]}/{pdf_name[11:13]}/{pdf_name}" for pdf_name in pdf_names]
    save_paths = [f"downloads/{pdf_name}" for pdf_name in pdf_names]
    return urls, save_paths, pdf_names

main()
