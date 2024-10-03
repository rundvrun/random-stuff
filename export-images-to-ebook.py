import os
import asyncio

num_chapter = 7

export_ext = ['azw3']
#export_ext = ['mobi', 'azw3', 'pdf', 'kfx']

W = 1648
H = 1236

color = False
color_export_ext = ['mobi', 'azw3', 'pdf']

output_profile = 'kindle_oasis'

dir_name = 'encomics'
epub_name = 'En'

async def create_epub(chapter):
    os.system(f'py Images_To_ePub.py -d {dir_name}\pictures\chapter{chapter} -f {dir_name}\exports\{dir_name}-chapter{chapter}.epub -n {epub_name}_{chapter} -g -H {H} -W {W} -c -p')
    for ext in export_ext:
        os.system(f'ebook-convert {dir_name}\exports\{dir_name}-chapter{chapter}.epub {dir_name}\exports\{dir_name}-chapter{chapter}.{ext} --output-profile {output_profile}')
        
    if color:
        os.system(f'py Images_To_ePub.py -d {dir_name}\pictures\chapter{chapter} -f {dir_name}\exports\{dir_name}-color-chapter{chapter}.epub -n {epub_name}_{chapter} -H {H} -W {W} -c -p')
        for ext in color_export_ext:
            os.system(f'ebook-convert {dir_name}\exports\{dir_name}-color-chapter{chapter}.epub {dir_name}\exports\{dir_name}-color-chapter{chapter}.{ext} --output-profile {output_profile}')
    
    await asyncio.sleep(1)
   
async def main():
    tasks = [asyncio.create_task(create_epub(chapter)) for chapter in range(1, num_chapter + 1)]
    await asyncio.gather(*tasks)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
