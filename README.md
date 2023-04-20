# Redmine Replicator CLI

## About 

Do you find tedious adding Redmine time entries manually? Now you can copy them from your team mates!

## Setup

```
$ pip install click
$ pip install python-redmine
```

## Usage
```
$ python redmine_replicator.py --help
$ python redmine_replicator.py 
    --apikey '5dX0Z1qa1cCfbZ724zaM143aZ8a7yfu2odp4W12f' 
    --url 'https://redmine.company.com' 
    --project 'project' 
    --teammate 'John Doe' 
    --date '2023/03/17' 
    --keywords 'Refinement'
    --keywords 'Daily' 
    --keywords 'Demo' 
    --keywords 'Planning' 
    --keywords 'Retrospective'
```
<img width="1265" alt="Screenshot 2023-04-20 at 23 19 11" src="https://user-images.githubusercontent.com/17875065/233492345-2b212302-24ee-4cf6-910d-3546946f7062.png">

## Contributing

- Fork the project and clone locally.
- Create a new branch for what you're going to work on.
- Push to your origin repository.
- Create a new pull request in GitHub.
