import requests
from bs4 import BeautifulSoup

url = "https://info.nec.go.kr/electioninfo/electionInfo_report.xhtml"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text[:3000])
