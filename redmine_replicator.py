import click
from redminelib import Redmine
from datetime import datetime

def filter_time_entries_by_date(time_entries, date):
  filtered_time_entry = []
  for time_entry in time_entries:
    created_on = datetime.fromtimestamp(time_entry.created_on.timestamp()).strftime("%Y/%m/%d")
    if (created_on == date):
      filtered_time_entry.append(time_entry)
  return filtered_time_entry

def filter_time_entries_by_keywords(time_entries, keywords):
  filtered_time_entry = []
  for time_entry in time_entries:
    for comment_keyword in keywords:
      if (comment_keyword in time_entry.comments):
        filtered_time_entry.append(time_entry)
  return filtered_time_entry

@click.command()
@click.option('--apikey', '-a', prompt='Redmine API key', help="Redmine API key")
@click.option('--url', '-u', prompt='Redmine Url. Example: https://redmine.company.com', help='Redmine Url. Example: https://redmine.company.com')
@click.option('--project', '-p', prompt='Proyect name from which to replicate time entries', help='Proyect name from which to replicate time entries')
@click.option('--teammate', '-t', prompt='Team mate from which to replicate time entries', help='Team mate from which to replicate time entries')
@click.option('--date', '-d', prompt='Date from which to replicate time entries. Format:YYYY/MM/DD', help='Date from which to replicate time entries. Format:YYYY/MM/DD') #callback=validateDate
@click.option('--keywords', '-k', multiple=True, default=["Refinement", "Daily", "Demo", "Planning", "Retrospective"], prompt='Keywords contained in the time entries comments', help='Keywords contained in the time entries comments')
@click.option('--input', '-i', is_flag=True, default=False, prompt='Replicate time entries [y] or only read them [n]', help='Flag which indicates if you want to replicate time entries or only read them')
def main(apikey, url, project, teammate, date, keywords, input):
  redmine = Redmine(url, key=apikey)    
  project = redmine.project.get(project)
  time_entries = project.time_entries[:100]

  time_entries_by_user = list(time_entries.filter(user__name=teammate))
  time_entries_by_date = filter_time_entries_by_date(time_entries_by_user, date)
  time_entries_by_keywords = filter_time_entries_by_keywords(time_entries_by_date, keywords)

  for time_entry in time_entries_by_keywords:
    print('{} - {} - {} - {} - {} - {}'.format(
      time_entry.created_on,
      time_entry.user.name,
      time_entry.activity,
      time_entry.issue,
      time_entry.comments,
      time_entry.hours
    ))
    
  if (input):
    print("Input option implementation WIP")

if __name__ == '__main__':
    main()
