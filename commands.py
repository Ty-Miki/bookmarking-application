from abc import ABC, abstractmethod
from datetime import datetime, timezone
from database import DatabaseManager
import sys
import requests

db = DatabaseManager('bookmark.db')

class Command(ABC):
    @abstractmethod
    def execute(self, data): pass
        
class CreateBookmarksTableCommand(Command):
    def execute(self, data=None):
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null',
        })
        return True, None
        
class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.now(timezone.utc).isoformat()
        db.add('bookmarks', data)
        return True, None

class ImportGithubStarsCommand(Command):
    @staticmethod
    def _extract_bookmark_info(repo):
        """Given a repository dictionary extract the needed pieces to create a bookmark"""
        
        return {'title': repo['name'],
                'url': repo['html_url'],
                'notes': repo['description'],}
        
    @staticmethod
    def _fetch_github_stars(github_username):
        # The URL for the first of results.
        next_page_of_results = f'https://api.github.com/users/{github_username}/starred'
        # Continue getting start results while more pages of results exist.
        while next_page_of_results:
            
            # Get the next page of results, using the right header to tell the API to return /
            # timestamps.
            stars_response = requests.get(next_page_of_results,
                                          headers={'Accept': 'application/vnd.github.v3.star+json'},)
            # The Link header with rel = next contains the link to the next page if available.
            next_page_of_results = stars_response.links.get('next', {}).get('url')
            
            yield from stars_response.json()
    
    def process_github_stars(self, data, repo_info):
        repo = repo_info['repo']
        if data['preserve_timestamp']:
            # The timestamp where the stamp was created.
            timestamp = datetime.strptime(repo_info['starred_at'], '%Y-%m-%dT%H:%M:%SZ')
        else:
            timestamp = None
        # Execute an AddBookmarkCommand populating database with repository data.
        AddBookmarkCommand().execute(self._extract_bookmark_info(repo), timestamp=timestamp)
        
        
    def execute(self, data):
        bookmarks_imported = 0
        for repo_info in self._fetch_github_stars(data['github_username']):
            self.process_github_stars(data, repo_info)
            bookmarks_imported += 1
        return True, bookmarks_imported 
                

class ListBookmarksCommand(Command):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by
    def execute(self, data=None):
        return True, db.select('bookmarks', order_by=self.order_by).fetchall()
    
class EditBookmarkCommand(Command):
    def execute(self, data):
        db.update(data['id'], data['update'])
        return True, None
     
   
class DeleteBookmarkCommand(Command):
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return  True, None
    

        
class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()
        return True, None
        

