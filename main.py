import urllib.request
from bs4 import BeautifulSoup
import pandas as pd



def scrape_brown_dwarf_data():

    url = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'
    
    with urllib.request.urlopen(url) as response:
        html_content = response.read()

    soup = BeautifulSoup(html_content, 'html.parser')    
    table = soup.find_all('table', class_='wikitable')[2]  # Get the third table (Field brown dwarfs)
    brown_dwarf_data = []
    rows = table.find('tbody').find_all('tr')
    
    for row in rows[1:]:  
        cells = row.find_all('td')
        
        if len(cells) >= 5:
            
            name = cells[0].text.strip()
            distance = cells[1].text.strip()
            mass = cells[2].text.strip()
            radius = cells[3].text.strip()
            luminosity = cells[4].text.strip()

            brown_dwarf_data.append([name, distance, mass, radius, luminosity])

    return brown_dwarf_data

def main():
    data = scrape_brown_dwarf_data()
    df = pd.DataFrame(data, columns=['Name', 'Distance', 'Mass', 'Radius', 'Luminosity'])
    df.to_csv('dwarf_stars.csv', index=False)

if __name__ == "__main__":
    main()



bright_stars_df = pd.read_csv('stars_data.csv')
brown_dwarf_stars_df = pd.read_csv('dwarf_stars.csv')

brown_dwarf_stars_df['Radius'] *= 0.102763
brown_dwarf_stars_df['Mass'] *= 0.000954588

merged_df = pd.merge(bright_stars_df, brown_dwarf_stars_df, on='Name', how='inner')

merged_df.to_csv('merged_stars_data.csv', index=False)
