import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'mock')))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
import xbmc  # This will now use our mock
import xbmcaddon  # This will now use our mock
from resources.lib.rating_updater import RatingUpdater
from resources.lib.logger import Logger
from datetime import datetime, timedelta

class TestRatingUpdater(unittest.TestCase):
    """Test cases for RatingUpdater class"""
    def setUp(self):
        self.rating_updater = RatingUpdater()

    def test_fetch_imdb_rating_movie_real(self):
        """Test fetching real IMDb rating for a known movie"""
        # The Shawshank Redemption (1994)
        rating, votes = self.rating_updater._fetch_imdb_rating('tt0111161', is_movie=True)
        
        self.assertIsNotNone(rating)
        self.assertIsNotNone(votes)
        self.assertGreater(float(rating), 0.0)
        self.assertLess(float(rating), 10.0)
        self.assertGreater(votes, 1000)  # Should have many votes
        
        print(f"IMDb rating for Shawshank: {rating} from {votes} votes")

    def test_fetch_imdb_rating_tv_episode_real(self):
        """Test fetching real IMDb rating for a specific TV show episode"""
        # Breaking Bad, Season 1, Episode 1
        rating, votes = self.rating_updater._fetch_imdb_rating('tt0959621', is_movie=False)
        
        self.assertIsNotNone(rating)
        self.assertIsNotNone(votes)
        self.assertGreater(float(rating), 0.0)
        self.assertLess(float(rating), 10.0)
        self.assertGreater(votes, 1000)
        
        print(f"IMDb rating for Breaking Bad S01E01: {rating} from {votes} votes")

    def test_fetch_trakt_rating_movie_real(self):
        rating, votes = self.rating_updater._fetch_trakt_rating('tt0468569', is_movie=True)
        
        self.assertIsNotNone(rating)
        self.assertIsNotNone(votes)
        self.assertGreater(float(rating), 0.0)
        self.assertLess(float(rating), 10.0)
        self.assertGreater(votes, 100)  # Should have decent number of votes
        
        print(f"Trakt rating for Dark Knight: {rating} from {votes} votes")

    def test_fetch_trakt_rating_tv_episode_real(self):
        """Test fetching real Trakt rating for a specific TV show episode"""
        rating, votes = self.rating_updater._fetch_trakt_rating('tt0903747', is_movie=False, season=1, episode=1)
        
        self.assertIsNotNone(rating)
        self.assertIsNotNone(votes)
        self.assertGreater(float(rating), 0.0)
        self.assertLess(float(rating), 10.0)
        self.assertGreater(votes, 1000)
        
        print(f"Trakt rating for Breaking Bad S01E01: {rating} from {votes} votes")

    def test_fetch_movie_rating_combined_real(self):
        """Test fetching and combining ratings from all enabled sources"""
        # Juror #2
        rating = self.rating_updater._fetch_rating('tt27403986', is_movie=True, season=1, episode=1)
        
        self.assertIsNotNone(rating)
        if isinstance(rating, (int, float)):
            self.assertGreater(float(rating), 0.0)
            self.assertLess(float(rating), 10.0)
        print(f"Combined rating for Breaking Bad S01E01: {rating}")

    def test_fetch_tv_episode_rating_combined_real(self):
        """Test fetching and combining ratings from all enabled sources"""
        # Breaking Bad S01E01
        rating = self.rating_updater._fetch_rating({'imdbnumber': 'tt0959621', 'show_imdbnumber': 'tt0903747'}, is_movie=False, season=1, episode=1)
        
        self.assertIsNotNone(rating)
        if isinstance(rating, (int, float)):
            self.assertGreater(float(rating), 0.0)
            self.assertLess(float(rating), 10.0)
        print(f"Combined rating for Breaking Bad S01E01: {rating}")

    def test_fetch_invalid_id(self):
        """Test fetching rating for an invalid IMDb ID"""
        rating, votes = self.rating_updater._fetch_imdb_rating('tt0000000', is_movie=True)
        self.assertEqual(rating, -1)
        self.assertEqual(votes, -1)

    def test_get_enabled_sources(self):
        """Test that at least one source is enabled"""
        sources = self.rating_updater._get_enabled_sources()
        self.assertGreater(len(sources), 0)
        print(f"Enabled rating sources: {sources}")

    def test_is_recent_episode(self):
        """Test episode date filtering"""
        cutoff_date = datetime.now() - timedelta(days=180)  # 6 months
        
        # Test recent episode
        recent_episode = {
            'firstaired': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        }
        self.assertTrue(self.rating_updater._is_recent_episode(recent_episode, cutoff_date))
        
        # Test old episode
        old_episode = {
            'firstaired': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        }
        self.assertFalse(self.rating_updater._is_recent_episode(old_episode, cutoff_date))
        
        # Test invalid date
        invalid_episode = {
            'firstaired': 'invalid-date'
        }
        self.assertFalse(self.rating_updater._is_recent_episode(invalid_episode, cutoff_date))
        
        # Test missing date
        missing_date_episode = {}
        self.assertFalse(self.rating_updater._is_recent_episode(missing_date_episode, cutoff_date))


    def test_get_tvshow_episodes(self):
        """Test getting TV show episodes with mock JSON-RPC response"""
        mock_response = '''{"id":22,"jsonrpc":"2.0","result":{"episodes":[{"episode":1,"episodeid":11,"firstaired":"2024-12-26","label":"2x01. Bread and Lottery","rating":7.900000095367432,"season":2,"showtitle":"Squid Game","tvshowid":2,"uniqueid":{"imdb":"tt15939754","tmdb":"5475279","tvdb":"10617348"}},{"episode":2,"episodeid":12,"firstaired":"2024-12-26","label":"2x02. Halloween Party","rating":7.300000190734863,"season":2,"showtitle":"Squid Game","tvshowid":2,"uniqueid":{"imdb":"tt34382288","tmdb":"5508375","tvdb":"10774412"}},{"episode":3,"episodeid":13,"firstaired":"2024-12-26","label":"2x03. 001","rating":7.900000095367432,"season":2,"showtitle":"Squid Game","tvshowid":2,"uniqueid":{"imdb":"tt35149224","tmdb":"5509085","tvdb":"10774413"}},{"episode":4,"episodeid":14,"firstaired":"2024-12-26","label":"2x04. Six Legs","rating":7.599999904632568,"season":2,"showtitle":"Squid Game","tvshowid":2,"uniqueid":{"imdb":"tt35154728","tmdb":"5747916","tvdb":"10774414"}},{"episode":5,"episodeid":15,"firstaired":"2024-12-26","label":"2x05. One More Game","rating":7.300000190734863,"season":2,"showtitle":"Squid Game","tvshowid":2,"uniqueid":{"imdb":"tt35154733","tmdb":"5747917","tvdb":"10774415"}},{"episode":6,"episodeid":16,"firstaired":"2024-12-26","label":"2x06. O ﻿ X","rating":7.800000190734863,"season":2,"showtitle":"Squid Game","tvshowid":2,"uniqueid":{"imdb":"tt35149232","tmdb":"5747918","tvdb":"10774416"}},{"episode":7,"episodeid":17,"firstaired":"2024-12-26","label":"2x07. Friend or Foe","rating":6.900000095367432,"season":2,"showtitle":"Squid Game","tvshowid":2,"uniqueid":{"imdb":"tt35153959","tmdb":"5747919","tvdb":"10863921"}},{"episode":1,"episodeid":18,"firstaired":"2008-01-20","label":"1x01. Pilot","rating":8.338129997253418,"season":1,"showtitle":"Breaking Bad","tvshowid":3,"uniqueid":{"imdb":"tt0959621","tmdb":"62085","tvdb":"349232"}},{"episode":2,"episodeid":19,"firstaired":"2008-01-27","label":"1x02. Cat's in the Bag...","rating":8.110250473022461,"season":1,"showtitle":"Breaking Bad","tvshowid":3,"uniqueid":{"imdb":"tt1054724","tmdb":"62086","tvdb":"349233"}},{"episode":3,"episodeid":20,"firstaired":"2008-02-10","label":"1x03. ...And the Bag's in the River","rating":8.054129600524903,"season":1,"showtitle":"Breaking Bad","tvshowid":3,"uniqueid":{"imdb":"tt1054725","tmdb":"62087","tvdb":"349235"}},{"episode":4,"episodeid":21,"firstaired":"2008-02-17","label":"1x04. Cancer Man","rating":7.958409786224365,"season":1,"showtitle":"Breaking Bad","tvshowid":3,"uniqueid":{"imdb":"tt1054726","tmdb":"62088","tvdb":"349236"}},{"episode":5,"episodeid":22,"firstaired":"2008-02-24","label":"1x05. Gray Matter","rating":7.976749897003174,"season":1,"showtitle":"Breaking Bad","tvshowid":3,"uniqueid":{"imdb":"tt1054727","tmdb":"62089","tvdb":"349238"}},{"episode":6,"episodeid":23,"firstaired":"2008-03-02","label":"1x06. Crazy Handful of Nothin'","rating":8.535460472106934,"season":1,"showtitle":"Breaking Bad","tvshowid":3,"uniqueid":{"imdb":"tt1054728","tmdb":"62090","tvdb":"355100"}},{"episode":7,"episodeid":24,"firstaired":"2008-03-09","label":"1x07. A No Rough Stuff Type Deal","rating":8.380620002746582,"season":1,"showtitle":"Breaking Bad","tvshowid":3,"uniqueid":{"imdb":"tt1054729","tmdb":"62091","tvdb":"352534"}}],"limits":{"end":14,"start":0,"total":14}}}'''
        
        with patch('xbmc.executeJSONRPC', return_value=mock_response):
            episodes = self.rating_updater._get_tvshow_episodes()
            
            # Should only return recent episodes (Squid Game season 2)
            self.assertEqual(len(episodes), 7)
            
            # Check first episode
            episode = episodes[0]
            self.assertEqual(episode['episodeid'], 11)
            self.assertEqual(episode['showtitle'], 'Squid Game')
            self.assertEqual(episode['season'], 2)
            self.assertEqual(episode['episode'], 1)
            self.assertEqual(episode['firstaired'], '2024-12-26')
            self.assertAlmostEqual(episode['rating'], 7.9, places=1)
            self.assertEqual(episode['imdbnumber'], 'tt15939754')
            
            # Check last episode
            episode = episodes[-1]
            self.assertEqual(episode['episodeid'], 17)
            self.assertEqual(episode['showtitle'], 'Squid Game')
            self.assertEqual(episode['season'], 2)
            self.assertEqual(episode['episode'], 7)
            self.assertEqual(episode['firstaired'], '2024-12-26')
            self.assertAlmostEqual(episode['rating'], 6.9, places=1)
            self.assertEqual(episode['imdbnumber'], 'tt35153959')

    def test_get_movies(self):
        """Test getting movies with mock JSON-RPC response"""
        mock_response = '''{"id":1,"jsonrpc":"2.0","result":{"limits":{"end":2,"start":0,"total":2},"movies":[
            {"imdbnumber":"1106739","label":"Juror #2","movieid":2,"rating":6.988999843597412,"title":"Juror #2","uniqueid":{"imdb":"tt27403986","tmdb":"1106739"},"year":2024},
            {"imdbnumber":"76341","label":"Mad Max: Fury Road","movieid":5,"rating":7.618000030517578,"title":"Mad Max: Fury Road","uniqueid":{"imdb":"tt1392190","tmdb":"76341"},"year":2015}
            ]}}'''
        
        with patch('xbmc.executeJSONRPC', return_value=mock_response):
            movies = self.rating_updater._get_movies()
            
            # Should only return recent movies (from last 2 years by default)
            self.assertEqual(len(movies), 1)
            
            # Check first movie
            movie = movies[0]
            self.assertEqual(movie['imdbnumber'], 'tt27403986')

    def test_get_movies_empty_response(self):
        """Test handling of empty JSON-RPC response for movies"""
        with patch('xbmc.executeJSONRPC', return_value=''):
            movies = self.rating_updater._get_movies()
            self.assertEqual(len(movies), 0)

    def test_get_movies_no_uniqueid(self):
        """Test handling of movies without uniqueid"""
        mock_response = '''{"id":1,"jsonrpc":"2.0","result":{"limits":{"end":1,"start":0,"total":1},"movies":[
            {"movieid":1,"rating":7.9,"title":"No IMDb ID","year":2024}
        ]}}'''
        
        with patch('xbmc.executeJSONRPC', return_value=mock_response):
            movies = self.rating_updater._get_movies()
            self.assertEqual(len(movies), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2) 