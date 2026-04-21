from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all data'))

        # Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')
        self.stdout.write(self.style.SUCCESS('Created teams'))

        # Users
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        for u in users:
            User.objects.create_user(username=u['username'], email=u['email'], password='password', team=u['team'])
        self.stdout.write(self.style.SUCCESS('Created users'))

        # Activities
        Activity.objects.create(user=User.objects.get(username='ironman'), type='run', duration=30)
        Activity.objects.create(user=User.objects.get(username='spiderman'), type='cycle', duration=45)
        Activity.objects.create(user=User.objects.get(username='batman'), type='swim', duration=60)
        Activity.objects.create(user=User.objects.get(username='superman'), type='run', duration=50)
        self.stdout.write(self.style.SUCCESS('Created activities'))

        # Leaderboard
        Leaderboard.objects.create(user=User.objects.get(username='ironman'), points=100)
        Leaderboard.objects.create(user=User.objects.get(username='spiderman'), points=80)
        Leaderboard.objects.create(user=User.objects.get(username='batman'), points=90)
        Leaderboard.objects.create(user=User.objects.get(username='superman'), points=110)
        self.stdout.write(self.style.SUCCESS('Created leaderboard'))

        # Workouts
        Workout.objects.create(name='Morning Cardio', description='Run and cycle')
        Workout.objects.create(name='Strength', description='Pushups and squats')
        self.stdout.write(self.style.SUCCESS('Created workouts'))

        # Create unique index on email for users collection
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db['octofit_tracker_user'].create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email'))
