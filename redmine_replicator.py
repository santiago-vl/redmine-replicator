import click
from redminelib import Redmine
from datetime import datetime

def filter_time_entries_by_date(time_entries, date):
  filtered_time_entries = []
  for time_entry in time_entries:
    created_on = datetime.fromtimestamp(time_entry.created_on.timestamp()).strftime("%Y/%m/%d")
    if (created_on == date):
      filtered_time_entries.append(time_entry)
  return filtered_time_entries

def filter_time_entries_by_keywords(time_entries, keywords):
  filtered_time_entries = []
  for time_entry in time_entries:
    for keyword in keywords:
      if (keyword.upper() in time_entry.comments.upper()):
        filtered_time_entries.append(time_entry)
  return filtered_time_entries

def replicate_time_entries(time_entries_to_replicate, redmine):
  current_user_id = redmine.user.get('current').id;
  for time_entry in time_entries_to_replicate:
    redmine.time_entry.create(
      issue_id=time_entry.issue.id,
      hours=time_entry.hours,
      activity_id=time_entry.activity.id,
      user_id=current_user_id,
      comments=time_entry.comments
    )
  print_time_entries_table(
    time_entries_to_replicate,
    '\n============================= Replicated times entries successfully =============================='
  )

def print_time_entries_to_replicate(time_entries_to_replicate):
  print_time_entries_table(
    time_entries_to_replicate,
    '\n=================================== Time entries to replicate ===================================='
  )


def print_time_entries_table(time_entries, header):
  print(header)
  print("{:<8} {:<25} {:<15} {:<20} {:<6} {:<10}".format('Issue','Username','Activity','Created on','Hours','Comments'))
  for time_entry in time_entries:
    print("{:<8} {:<25} {:<15} {:<20} {:<6} {:<10}".format(time_entry.issue.id, time_entry.user.name,
      str(time_entry.activity), str(time_entry.created_on), time_entry.hours, time_entry.comments))

@click.command()
@click.option('--apikey', '-a', prompt='Redmine API key', help="Redmine API key")
@click.option('--url', '-u', prompt='Redmine Url. Example: https://redmine.company.com', help='Redmine Url. Example: https://redmine.company.com')
@click.option('--project', '-p', prompt='Proyect name from which to replicate time entries', help='Proyect name from which to replicate time entries')
@click.option('--teammate', '-t', prompt='Team mate from which to replicate time entries', help='Team mate from which to replicate time entries')
@click.option('--date', '-d', is_flag=False, default=datetime.today().strftime("%Y/%m/%d"), help='Date from which to replicate time entries. Format:YYYY/MM/DD. By default is today') #callback=validateDate
@click.option('--keywords', '-k', multiple=True, is_flag=False, default=["Refinement", "Daily", "Demo", "Planning", "Retrospective"], help='Keywords contained in the time entries comments')
def main(apikey, url, project, teammate, date, keywords):
  redmine = Redmine(url, key=apikey)    
  project = redmine.project.get(project)
  time_entries = project.time_entries[:100]

  time_entries_by_user = list(time_entries.filter(user__name=teammate))
  time_entries_by_date = filter_time_entries_by_date(time_entries_by_user, date)
  time_entries_to_replicate = filter_time_entries_by_keywords(time_entries_by_date, keywords)

  print_time_entries_to_replicate(time_entries_to_replicate)

  if (click.confirm('\nDo you want replicate time entries?')):
    replicate_time_entries(time_entries_to_replicate, redmine)

if __name__ == '__main__':
    main()
