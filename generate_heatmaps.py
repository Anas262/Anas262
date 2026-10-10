import urllib.request
import re
from datetime import datetime

username = 'Anas262'
years = [2023, 2024, 2025, 2026]

COLORS = {
    '0': '#101C1B',
    '1': '#0b4d3c',
    '2': '#009f75',
    '3': '#00D9A3',
    '4': '#65E5BD'
}

def generate_svg(year, data_levels):
    # data_levels is a list of integers/strings 0-4 representing each day's contribution level
    # We will lay it out just like github: 53 columns, 7 rows
    
    # SVG Settings
    box_size = 10
    gap = 3
    svg_width = 53 * (box_size + gap) + 20
    svg_height = 7 * (box_size + gap) + 30
    
    svg = f'<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">\n'
    svg += f'  <rect width="100%" height="100%" fill="#080D12" rx="5" />\n'
    svg += f'  <text x="10" y="20" fill="#D7DEE2" font-family="sans-serif" font-size="12" font-weight="bold">{year} Contributions</text>\n'
    svg += f'  <g transform="translate(10, 30)">\n'
    
    for i, level in enumerate(data_levels):
        col = i // 7
        row = i % 7
        x = col * (box_size + gap)
        y = row * (box_size + gap)
        color = COLORS.get(str(level), COLORS['0'])
        svg += f'    <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" rx="2" />\n'
        
    svg += '  </g>\n'
    svg += '</svg>'
    return svg

import os
os.makedirs('assets/heatmaps', exist_ok=True)

for year in years:
    url = f'https://github.com/users/{username}/contributions?from={year}-01-01&to={year}-12-31'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Find all data-level attributes in order
            levels = re.findall(r'data-level="(\d+)"', html)
            
            if levels:
                svg_content = generate_svg(year, levels)
                with open(f'assets/heatmaps/{year}.svg', 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                print(f'Generated assets/heatmaps/{year}.svg with {len(levels)} days.')
            else:
                print(f'No data found for {year}.')
    except Exception as e:
        print(f'Error fetching {year}: {e}')
