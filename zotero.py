from pyzotero import zotero
import os
from shutil import copyfile
from datetime import datetime, timedelta, timezone
import dateutil.parser as dup

LIBRARY_ID = 5302540
LIBRARY_TYPE = 'user'
API_KEY = 'vzYPkbBou9ADFvahs7ym4T6k'
TIMEFRAME = timedelta(days=7)

# Create the template Markdown file to write into.
time_now = datetime.now(timezone(timedelta(hours=0)))
YYYY_MM_DD = time_now.strftime('%Y-%m-%d')
num = int([f for f in sorted(os.listdir('_readings')) if 'weekly-readings-' in f][-1].split('.')[0].split('-')[-1]) + 1
fname = '{}-weekly-readings-{}'.format(YYYY_MM_DD, num)
with open('_readings/_TEMPLATE.md', 'r') as f_template:
    with open('_readings/{}.md'.format(fname), 'w') as f:
        for i, l in enumerate(f_template.readlines()):
            if i == 1:
                assert l[:6] == 'title:'
                l = l[:-1]+str(num)+"'\n"
            elif i == 2:
                assert l[:5] == 'date:' 
                l = l[:-1]+YYYY_MM_DD+'\n'
            elif i == 3:
                assert l[:10] == 'permalink:'
                YYYY, MM = YYYY_MM_DD.split('-')[:2]
                l = l[:-1]+YYYY+'/'+MM+'/weekly-readings-{}'.format(num)+'/\n'
            f.write(l)

# Load the library and retrieve all items.
zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
items = zot.items()

notes = []
first_author_surnames = []
for item in items:
    # Find Markdown files.
    if item['data']['itemType'] == 'attachment' and item['data']['contentType'] == 'text/plain':
        time_since_created = time_now - dup.parse(item['data']['dateAdded'])
        if time_since_created >= TIMEFRAME: break # Stop if the file is older than the timeframe.

        # Get the first author's surname from the parent item.
        parent = zot.item(item['data']['parentItem'])
        first_author_surnames.append(parent['data']['creators'][0]['lastName'])

        # Store the notes.
        notes.append(zot.file(item['key']))

# Write the notes in surname order.
order = sorted(range(len(first_author_surnames)), key=lambda ix: first_author_surnames[ix])
with open('_readings/{}.md'.format(fname), 'ab') as f:
    for i in order:
        f.write(bytes('\n', 'utf-8'))
        f.write(notes[i])

with open('_readings/{}.md'.format(fname), 'a') as f:
    # Add key insights section at the bottom.
    f.write('\n## 🗝️  Key Insights')
    for i in order: f.write('\n- ') # One bullet point per paper.