from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

app = Flask(__name__)

# Distance data for printers
distances = {
    "KC": [11, 12, 12, 15, 11, 3, 3, 5, 6, 10, 5, 17, 7, 8, 7, 19, 12, 9, 9, 7, 2, 1, 15, 7, 15, 7, 11, 3, 10, 6, 17, 5],
    "Pollock": [14, 8, 7, 3, 15, 14, 17, 11, 18, 24, 15, 12, 16, 9, 9, 16, 24, 8, 9, 9, 15, 15, 1, 16, 3, 16, 5, 18, 15, 18, 30, 14],
    "Findlay": [10, 19, 7, 15, 9, 20, 17, 17, 24, 28, 23, 1, 25, 19, 16, 10, 30, 12, 20, 17, 16, 16, 12, 25, 15, 14, 13, 21, 10, 24, 35, 22],
}

# Printer buildings
printer_names = [
    "University Park - Ag Sciences", "University Park - Atherton", "University Park - Bank of America",
    "University Park - Beaver", "University Park - Business", "University Park - Carnegie",
    "University Park - Chambers", "University Park - Davey Lab", "University Park - Deike",
    "University Park - ECoRE", "University Park - Electrical Engineering West", "University Park - Findlay",
    "University Park - Hammond", "University Park - Henderson", "University Park - HUB",
    "University Park - Katz", "University Park - Leonhard", "University Park - Life Sciences",
    "University Park - Nursing Sciences", "University Park - Osmond", "University Park - Paterno",
    "University Park - Pattee", "University Park - Pollock", "University Park - Reber",
    "University Park - Redifer", "University Park - Stuckeman", "University Park - Thomas",
    "University Park - Waring", "University Park - Warnock", "University Park - Westgate",
    "University Park - Weston", "University Park - Willard"
]

# Fetch and filter printers needing fixing
def fetch_printers():
    url = "https://cs.wepanow.com/000PSU283University%20Park.html&filter="
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse printer rows
        printers = []
        for row in soup.find_all('tr'):
            text = row.get_text(separator=' ', strip=True)
            # Identify rows with issues
            status_match = re.search(r"Status Message:\s*(.*?)(Printer Text|$)", text)
            if status_match:
                status = status_match.group(1).strip()
                if status and "Ready" not in status and "N/A" not in status:
                    # Extract printer name
                    for name in printer_names:
                        if name in text:
                            printers.append({
                                "name": name,
                                "status": status
                            })
                            break

        return printers
    except Exception as e:
        print(f"Error fetching printers: {e}")
        return []

@app.route('/')
def index():
    printers = fetch_printers()  # Fetch printers needing fixing
    last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Last update timestamp
    return render_template(
        'index.html',
        last_updated=last_updated,
        distances=distances,
        printer_names=printer_names,
        printers=printers
    )

if __name__ == '__main__':
    app.run(debug=True)
